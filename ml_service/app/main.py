from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel, Field
from typing import List, Dict
from google import genai
from google.genai import types
import os
import datetime
import motor.motor_asyncio

from ml_service.app.services.analytics import CycleEngine
from ml_service.app.services.recommendations import WellnessEngine

app = FastAPI(
    title="Project Abhaya AI/ML Engine",
    description="Microservice providing predictive health and generative wellness capabilities.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any local frontend port to connect during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_client = genai.Client()

MONGO_DETAILS = os.getenv("MONGO_DETAILS")

if not MONGO_DETAILS:
    print("\n🚨 WARNING: MONGO_DETAILS environment variable is missing!")
    # Use a generic mock placeholder for production safe routing
    MONGO_DETAILS = "mongodb://localhost:27017" 

client = motor.motor_asyncio.AsyncIOMotorClient(
    MONGO_DETAILS,
    serverSelectionTimeoutMS=3000,
    connectTimeoutMS=3000
)
db = client.abhaya_database
community_collection = db.get_collection("community_posts")

# --- IN-MEMORY FALLBACK STORAGE ---
# Preserved and used to guarantee immediate data presence if MongoDB collections are blank
community_feeds = {
    "pcos": [
        {"title": "🌸 Managing Insulin Resistance", "content": "Focusing on a low-glycemic diet and strength training completely shifted my energy levels and balanced my cycles.", "author": "Anonymous User"},
        {"title": "💗 You Are Not Alone", "content": "Getting diagnosed at 19 was terrifying, but tracking my symptoms and pacing my lifestyle helped me take back control.", "author": "Anonymous User"}
    ],
    "awareness": [
        {"title": "🔬 Understanding Phase Changes", "content": "The menstrual cycle has four key phases: Menstrual, Follicular, Ovulatory, and Luteal. Estrogen peaks right before ovulation.", "author": "Abhaya Medical Team"},
        {"title": "🩸 Myth Busting: Irregular Periods", "content": "An occasional irregular cycle is normal due to temporary stress or travel, but consistent variations warrant tracking and professional insight.", "author": "Abhaya Medical Team"}
    ],
    "stories": [
        {"title": "✨ My Journey to Hormone Balance", "content": "After years of struggling with cystic acne and fatigue, lifestyle modifications helped regulate my cycles naturally.", "author": "Anonymous User"},
        {"title": "🌱 Embracing Sustainable Wellness", "content": "Switching to organic menstrual care products and stress monitoring reduced my cyclical pain and anxiety.", "author": "Anonymous User"}
    ]
}

# --- DATA MODELS ---

class EducationalArticle(BaseModel):
    title: str
    category: str  # e.g., "pcos", "awareness", "stories"
    content: str
    tags: List[str] = []
    last_updated: str = datetime.datetime.now().strftime("%Y-%m-%d")

# --- UPDATE DATA MODELS ---

class WellnessStory(BaseModel):
    title: str
    author: str = "Anonymous User"  # Allows names to be entered dynamically
    story_body: str
    likes: int = 0
    timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


# --- UPDATED EXTENDED FALLBACK ARCHIVE ---
period_awareness_data = {
    "hygiene": [
        {"title": "🧼 Essential Menstrual Hygiene Management", "content": "Change sanitary products every 4-6 hours to prevent bacterial growth. Always wash hands before and after changing. Use mild, unfragranced soap for cleaning external areas.", "last_updated": "Medical Guide"},
        {"title": "🧺 Sustainable Choices", "content": "Consider switching to menstrual cups or organic cotton pads to avoid synthetic plastics and chlorine bleach alternatives.", "last_updated": "Eco Wellness"}
    ],
    "cramps": [
        {"title": "🔥 Managing Dysmenorrhea (Period Pain)", "content": "Apply a heating pad or hot water bottle to your lower abdomen to relax uterine muscles. Light stretches, gentle yoga (like Child's Pose), and staying hydrated significantly reduce cramp severity.", "last_updated": "Physio Insights"},
        {"title": "🍵 Herbal Interventions", "content": "Ginger or chamomile tea possess natural anti-inflammatory properties that can mitigate uterine contraction pain.", "last_updated": "Holistic Health"}
    ],
    "nutrition": [
        {"title": "🥦 Micronutrient Tracking During Bleeding", "content": "Replenish iron losses by incorporating spinach, lentils, beans, and lean meats accompanied by Vitamin C for maximum absorption. Avoid excessive caffeine and high-sodium foods to prevent bloating.", "last_updated": "Nutrition Desk"}
    ]
}


# --- UPDATED OPERATIONAL API ROUTES ---

# ---- PERIOD AWARENESS ENDPOINTS ----
@app.get("/api/awareness/{category}")
async def get_awareness_articles(category: str):
    """Fetches comprehensive care guidelines matching a specific category (e.g., hygiene, cramps, nutrition)."""
    cat_lower = category.lower()
    collection = db[f"awareness_{cat_lower}"]
    articles = []
    try:
        async for doc in collection.find({}).sort("_id", -1).limit(10):
            doc["_id"] = str(doc["_id"])
            articles.append(doc)
    except Exception:
        pass
    
    # Dynamic fallback to rich, educational period health articles if MongoDB is empty
    if not articles and cat_lower in period_awareness_data:
        return period_awareness_data[cat_lower]
        
    return articles


# ---- WOMEN WELLNESS STORIES ENDPOINTS ----
@app.get("/api/stories")
async def get_wellness_stories():
    """Fetches live interactive collective tracking feed for user wellness journeys from Atlas cloud."""
    collection = db["wellness_stories"]
    stories = []
    try:
        async for doc in collection.find({}).sort("_id", -1).limit(15):
            stories.append({
                "title": doc["title"],
                "story_body": doc["story_body"],
                "author": doc.get("author", "Anonymous User"),
                "likes": doc.get("likes", 0)
            })
    except Exception:
        pass
        
    # Standard fallback if the collection hasn't accumulated live entries yet
    if not stories and "stories" in community_feeds:
        return [{"title": x["title"], "story_body": x["content"], "author": x["author"], "likes": 0} for x in community_feeds["stories"]]
        
    return stories

@app.post("/api/stories/submit")
async def submit_wellness_story(story: WellnessStory):
    """Persists a custom user wellness or recovery testimony straight to Atlas cloud arrays with author attributes."""
    collection = db["wellness_stories"]
    result = await collection.insert_one(story.model_dump())
    if result.inserted_id:
        return {"status": "success", "message": "Journey timeline synchronized successfully!"}
    raise HTTPException(status_code=500, detail="Database save operation encountered a fault.")

class PCOSAssessmentInput(BaseModel):
    age: int = Field(..., ge=13, le=50)
    cycle_length_days: int
    weight_gain_sudden: bool
    hair_growth_excessive: bool
    skin_darkening: bool
    mood_swings_severity: int = Field(..., ge=1, le=5)

class NewCommunityPost(BaseModel):
    title: str
    content: str

class ChatMessage(BaseModel):
    message: str

class CycleHistoryInput(BaseModel):
    history: List[Dict[str, str]]

class RecommendationInput(BaseModel):
    day_in_cycle: int = Field(..., ge=1, le=45)


# --- API ROUTES ---

@app.get("/")
def read_root():
    return {"status": "healthy", "service": "Project Abhaya ML Core API"}

# ---- PERIOD AWARENESS ENDPOINTS ----
@app.get("/api/awareness/{category}")
async def get_awareness_articles(category: str):
    """Fetches comprehensive care guidelines matching a specific category (e.g., hygiene, cramps, nutrition)."""
    cat_lower = category.lower()
    collection = db[f"awareness_{cat_lower}"]
    articles = []
    try:
        async for doc in collection.find({}).sort("_id", -1).limit(10):
            doc["_id"] = str(doc["_id"])
            articles.append(doc)
    except Exception:
        pass
    
    # Dynamic fallback to rich, educational period health articles if MongoDB is empty
    if not articles and cat_lower in period_awareness_data:
        return period_awareness_data[cat_lower]
        
    return articles

@app.post("/api/awareness/{category}/add")
async def add_awareness_article(category: str, article: EducationalArticle):
    """Allows updating or contributing resource parameters to the tracking repository."""
    collection = db[f"awareness_{category}"]
    result = await collection.insert_one(article.model_dump())
    return {"status": "success", "inserted_id": str(result.inserted_id)}


# ---- WOMEN WELLNESS STORIES ENDPOINTS ----
@app.get("/api/stories")
async def get_wellness_stories():
    """Fetches live interactive collective tracking feed for user wellness journeys from Atlas cloud."""
    collection = db["wellness_stories"]
    stories = []
    try:
        async for doc in collection.find({}).sort("_id", -1).limit(15):
            stories.append({
                "title": doc["title"],
                "story_body": doc["story_body"],
                "author": doc.get("author", "Anonymous User"),
                "likes": doc.get("likes", 0)
            })
    except Exception:
        pass
        
    # Standard fallback if the collection hasn't accumulated live entries yet
    if not stories and "stories" in community_feeds:
        return [{"title": x["title"], "story_body": x["content"], "author": x["author"], "likes": 0} for x in community_feeds["stories"]]
        
    return stories

@app.post("/api/stories/submit")
async def submit_wellness_story(story: WellnessStory):
    """Persists a custom user wellness or recovery testimony straight to Atlas cloud arrays with author attributes."""
    collection = db["wellness_stories"]
    result = await collection.insert_one(story.model_dump())
    if result.inserted_id:
        return {"status": "success", "message": "Journey timeline synchronized successfully!"}
    raise HTTPException(status_code=500, detail="Database save operation encountered a fault.")

# ---- DYNAMIC MONGODB COMMUNITY REGISTRY ----
@app.get("/api/community/{category}")
async def fetch_live_community_feed(category: str):
    posts = []
    cursor = community_collection.find({"category": category}).sort("_id", -1).limit(20)
    async for document in cursor:
        posts.append({
            "title": document["title"],
            "content": document["content"],
            "author": document.get("author", "Anonymous User")
        })
        
    # Fallback to local data structure if database returns nothing
    if not posts and category in community_feeds:
        return {"feed": community_feeds[category]}
        
    return {"feed": posts}

@app.post("/api/community/{category}/post")
async def save_live_community_post(category: str, data: NewCommunityPost):
    new_document = {
        "category": category,
        "title": data.title,
        "content": data.content,
        "author": "Anonymous User"
    }
    result = await community_collection.insert_one(new_document)
    if result.inserted_id:
        return {"status": "success", "message": "Experience saved securely to the global cloud!"}
    raise HTTPException(status_code=500, detail="Database write operation failed.")


# ---- CORE ML HEALTH PREDICTIONS ----
@app.post("/api/predict/pcos-risk")
async def evaluate_pcos_risk(data: PCOSAssessmentInput):
    risk_score = 0.1
    if data.weight_gain_sudden: risk_score += 0.25
    if data.hair_growth_excessive: risk_score += 0.25
    if data.skin_darkening: risk_score += 0.20
    risk_score += (data.mood_swings_severity * 0.04)
    
    risk_probability = min(round(risk_score, 2), 1.0)
    return {
        "pcos_risk_probability": risk_probability,
        "risk_classification": "High" if risk_probability > 0.6 else "Moderate" if risk_probability > 0.3 else "Low",
        "message": "AI-generated risk index. Consult a certified gynecologist for medical confirmation."
    }


@app.post("/api/chat/abhaya-bot")
async def consult_chatbot(payload: ChatMessage):
    try:
        config = types.GenerateContentConfig(
            system_instruction=(
                "You are Abhaya AI, a supportive, safe, empathetic, and professional AI companion "
                "for women's reproductive health wellness. Provide informative answers, break down period myths, "
                "and focus on stress reduction."
            ),
            temperature=0.7
        )
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=payload.message,
            config=config
        )
        return {"response": response.text}
    except Exception as e:
        return {
            "response": f"[Fallback] Received message: '{payload.message}'. Configure GEMINI_API_KEY environment variable. Error trace: {str(e)}"
        }


@app.post("/api/analytics/cycle-summary")
async def get_cycle_summary(data: CycleHistoryInput):
    try:
        metrics = CycleEngine.calculate_metrics(data.history)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Data processing error: {str(e)}")


@app.post("/api/analytics/recommendations")
async def get_phase_recommendations(data: RecommendationInput):
    try:
        return WellnessEngine.get_recommendations(data.day_in_cycle)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Recommendation pipeline error: {str(e)}")