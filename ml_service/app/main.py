
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel, Field
from typing import List, Dict
from google import genai
from google.genai import types
import os

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

import motor.motor_asyncio

# Replace the connection string below with your real cluster string from MongoDB Atlas
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
db = client.abhaya_database
community_collection = db.get_collection("community_posts")


# --- DATA SCHEMAS ---

class PCOSAssessmentInput(BaseModel):
    age: int = Field(..., ge=13, le=50)
    cycle_length_days: int
    weight_gain_sudden: bool
    hair_growth_excessive: bool
    skin_darkening: bool
    mood_swings_severity: int = Field(..., ge=1, le=5)

# --- IN-MEMORY COMMUNITY STORAGE ---
community_feeds = {
    "pcos": [
        {"title": "🌸 Managing Insulin Resistance", "content": "Focusing on a low-glycemic diet and strength training completely shifted my energy levels and balanced my cycles.", "author": "Anonymous"},
        {"title": "💗 You Are Not Alone", "content": "Getting diagnosed at 19 was terrifying, but tracking my symptoms and pacing my lifestyle helped me take back control.", "author": "Anonymous"}
    ],
    "awareness": [
        {"title": "🔬 Understanding Phase Changes", "content": "The menstrual cycle has four key phases: Menstrual, Follicular, Ovulatory, and Luteal. Estrogen peaks right before ovulation.", "author": "Abhaya Medical Team"},
        {"title": "🩸 Myth Busting: Irregular Periods", "content": "An occasional irregular cycle is normal due to temporary stress or travel, but consistent variations warrant tracking and professional insight.", "author": "Abhaya Medical Team"}
    ],
    "stories": [
        {"title": "✨ My Journey to Hormone Balance", "content": "After years of struggling with cystic acne and fatigue, lifestyle modifications helped regulate my cycles naturally.", "author": "Anonymous"},
        {"title": "🌱 Embracing Sustainable Wellness", "content": "Switching to organic menstrual care products and stress monitoring reduced my cyclical pain and anxiety.", "author": "Anonymous"}
    ]
}

class CommunityPostInput(BaseModel):
    title: str
    content: str


class NewCommunityPost(BaseModel):
    title: str
    content: str

@app.get("/api/community/{category}")
async def fetch_live_community_feed(category: str):
    posts = []
    # Query MongoDB for the last 20 posts matching the selected category
    cursor = community_collection.find({"category": category}).sort("_id", -1).limit(20)
    async for document in cursor:
        posts.append({
            "title": document["title"],
            "content": document["content"],
            "author": document.get("author", "Anonymous User")
        })
    return {"feed": posts}

@app.post("/api/community/{category}/post")
async def save_live_community_post(category: str, data: NewCommunityPost):
    new_document = {
        "category": category,
        "title": data.title,
        "content": data.content,
        "author": "Anonymous User"
    }
    # Insert the document directly into your online cluster collection
    result = await community_collection.insert_one(new_document)
    if result.inserted_id:
        return {"status": "success", "message": "Experience saved securely to the global cloud!"}
    raise HTTPException(status_code=500, detail="Database write operation failed.")

class ChatMessage(BaseModel):
    message: str

class CycleHistoryInput(BaseModel):
    history: List[Dict[str, str]]

class RecommendationInput(BaseModel):
    day_in_cycle: int = Field(..., ge=1, le=45)


# --- ROUTE ENDPOINTS ---

@app.get("/")
def read_root():
    return {"status": "healthy", "service": "Project Abhaya ML Core API"}


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
        # Define persona constraints using the new SDK's config structure
        config = types.GenerateContentConfig(
            system_instruction=(
                "You are Abhaya AI, a supportive, safe, empathetic, and professional AI companion "
                "for women's reproductive health wellness. Provide informative answers, break down period myths, "
                "and focus on stress reduction."
            ),
            temperature=0.7
        )
        
        # Request generation using the modern Gemini model index
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=payload.message,
            config=config
        )
        
        return {"response": response.text}
        
    except Exception as e:
        # Fallback safeguard prints the raw exception if environmental API keys are missing
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
