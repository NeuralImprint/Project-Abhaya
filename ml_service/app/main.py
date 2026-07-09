# ml_service/app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
import google.generativeai as genai
import os

from ml_service.app.services.analytics import CycleEngine

app = FastAPI(
    title="Project Abhaya AI/ML Engine",
    description="Microservice providing predictive health and generative wellness capabilities.",
    version="1.0.0"
)


class PCOSAssessmentInput(BaseModel):
    age: int = Field(..., ge=13, le=50)
    cycle_length_days: int
    weight_gain_sudden: bool
    hair_growth_excessive: bool
    skin_darkening: bool
    mood_swings_severity: int = Field(..., ge=1, le=5)

class ChatMessage(BaseModel):
    message: str

class CycleHistoryInput(BaseModel):
    history: List[Dict[str, str]]

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
        system_instruction = (
            "You are Abhaya AI, a supportive, safe, empathetic, and professional AI companion "
            "for women's reproductive health wellness. Provide informative answers, break down period myths, "
            "and focus on stress reduction."
        )
        model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=system_instruction)
        response = model.generate_content(payload.message)
        return {"response": response.text}
    except Exception as e:
        return {"response": f"[Fallback] Received message: '{payload.message}'. Configure GEMINI_API_KEY to test active LLM chat."}

@app.post("/api/analytics/cycle-summary")
async def get_cycle_summary(data: CycleHistoryInput):
    try:
        metrics = CycleEngine.calculate_metrics(data.history)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Data processing error: {str(e)}")