"""
Project Abhaya — Community Routes
Endpoints: Community feed (GET) and post creation (POST) with MongoDB.
Falls back to in-memory storage if MongoDB is unavailable.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import CommunityPostInput

router = APIRouter(prefix="/api", tags=["Community"])

# MongoDB collection reference — set by main.py at startup
community_collection = None


def set_collection(collection):
    """Called from main.py to inject the MongoDB collection reference."""
    global community_collection
    community_collection = collection


# ─── Fallback In-Memory Storage ─────────────────────────────
# Used when MongoDB is unavailable (local dev without Mongo)

_fallback_feeds = {
    "pcos": [
        {
            "title": "🌸 Managing Insulin Resistance",
            "content": "Focusing on a low-glycemic diet and strength training completely shifted my energy levels and balanced my cycles.",
            "author": "Anonymous"
        },
        {
            "title": "💗 You Are Not Alone",
            "content": "Getting diagnosed at 19 was terrifying, but tracking my symptoms and pacing my lifestyle helped me take back control.",
            "author": "Anonymous"
        }
    ],
    "awareness": [
        {
            "title": "🔬 Understanding Phase Changes",
            "content": "The menstrual cycle has four key phases: Menstrual, Follicular, Ovulatory, and Luteal. Estrogen peaks right before ovulation.",
            "author": "Abhaya Medical Team"
        },
        {
            "title": "🩸 Myth Busting: Irregular Periods",
            "content": "An occasional irregular cycle is normal due to temporary stress or travel, but consistent variations warrant tracking and professional insight.",
            "author": "Abhaya Medical Team"
        }
    ],
    "stories": [
        {
            "title": "✨ My Journey to Hormone Balance",
            "content": "After years of struggling with cystic acne and fatigue, lifestyle modifications helped regulate my cycles naturally.",
            "author": "Anonymous"
        },
        {
            "title": "🌱 Embracing Sustainable Wellness",
            "content": "Switching to organic menstrual care products and stress monitoring reduced my cyclical pain and anxiety.",
            "author": "Anonymous"
        }
    ]
}


# ─── GET Community Feed ─────────────────────────────────────

@router.get("/community/{category}")
async def fetch_community_feed(category: str):
    """
    Fetch the latest community posts for a given category.
    Uses MongoDB if available, otherwise returns seed data from memory.
    """
    # Try MongoDB first
    if community_collection is not None:
        try:
            posts = []
            cursor = community_collection.find(
                {"category": category}
            ).sort("_id", -1).limit(20)

            async for document in cursor:
                posts.append({
                    "title": document["title"],
                    "content": document["content"],
                    "author": document.get("author", "Anonymous User")
                })

            return {"feed": posts}

        except Exception:
            # MongoDB query failed — fall through to in-memory
            pass

    # Fallback: return seed data from memory
    return {"feed": _fallback_feeds.get(category, [])}


# ─── POST Community Entry ───────────────────────────────────

@router.post("/community/{category}/post")
async def create_community_post(category: str, data: CommunityPostInput):
    """
    Create a new community post in the specified category.
    Saves to MongoDB if available, otherwise saves to in-memory storage.
    """
    new_post = {
        "category": category,
        "title": data.title,
        "content": data.content,
        "author": "Anonymous User"
    }

    # Try MongoDB first
    if community_collection is not None:
        try:
            result = await community_collection.insert_one(new_post)
            if result.inserted_id:
                return {"status": "success", "message": "Experience shared to the community!"}
            raise HTTPException(status_code=500, detail="Database write failed.")
        except HTTPException:
            raise
        except Exception:
            pass  # Fall through to in-memory

    # Fallback: save to in-memory
    if category not in _fallback_feeds:
        _fallback_feeds[category] = []

    _fallback_feeds[category].insert(0, {
        "title": data.title,
        "content": data.content,
        "author": "Anonymous User"
    })

    return {"status": "success", "message": "Experience shared to the community!"}
