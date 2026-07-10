"""
Project Abhaya — FastAPI Application Entry Point
Mounts all route modules and configures middleware.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routes import health, chat, community


# ─── Lifespan: startup/shutdown events ──────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown tasks."""
    settings = get_settings()

    # Attempt MongoDB connection at startup
    mongo_available = False
    try:
        import motor.motor_asyncio
        mongo_client = motor.motor_asyncio.AsyncIOMotorClient(
            settings.mongo_uri,
            serverSelectionTimeoutMS=3000  # 3s timeout to avoid hanging
        )
        # Verify the connection actually works
        await mongo_client.admin.command("ping")

        db = mongo_client[settings.mongo_db_name]
        collection = db.get_collection("community_posts")

        # Inject the collection into the community router
        community.set_collection(collection)

        mongo_available = True
        print(f"[OK] MongoDB connected: {settings.mongo_uri}")
        print(f"    Database: {settings.mongo_db_name}")
    except Exception as e:
        print(f"[WARN] MongoDB unavailable ({e}). Using in-memory fallback for community features.")

    print(f"[START] Project Abhaya API v{settings.app_version} is running!")
    print(f"    Docs: http://127.0.0.1:8000/docs")
    print(f"    MongoDB: {'Connected' if mongo_available else 'In-memory fallback'}")

    yield  # App runs here

    # Cleanup on shutdown
    if mongo_available:
        mongo_client.close()
        print("[SHUTDOWN] MongoDB connection closed.")


# ─── Create FastAPI App ─────────────────────────────────────

settings = get_settings()

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan
)


# ─── CORS Middleware ────────────────────────────────────────

origins = [o.strip() for o in settings.cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Mount Route Modules ───────────────────────────────────

app.include_router(health.router)
app.include_router(chat.router)
app.include_router(community.router)


# ─── Root Health Check ──────────────────────────────────────

@app.get("/", tags=["System"])
def root_health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": "Project Abhaya ML Core API",
        "version": settings.app_version
    }
