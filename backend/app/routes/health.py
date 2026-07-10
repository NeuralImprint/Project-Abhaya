"""
Project Abhaya — Health Routes
Endpoints: PCOS risk prediction, cycle analytics, phase recommendations.
"""

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    PCOSAssessmentInput,
    CycleHistoryInput,
    RecommendationInput,
)
from app.services.analytics import CycleEngine
from app.services.recommendations import WellnessEngine


router = APIRouter(prefix="/api", tags=["Health & Analytics"])


# ─── PCOS Risk Assessment ───────────────────────────────────

@router.post("/predict/pcos-risk")
async def evaluate_pcos_risk(data: PCOSAssessmentInput):
    """
    AI-powered PCOS risk estimation based on symptom profile.
    Returns a probability score and risk classification.
    """
    risk_score = 0.1

    # Weight symptom contributions
    if data.weight_gain_sudden:
        risk_score += 0.25
    if data.hair_growth_excessive:
        risk_score += 0.25
    if data.skin_darkening:
        risk_score += 0.20

    # Mood severity adds incremental risk
    risk_score += (data.mood_swings_severity * 0.04)

    # Irregular cycles (>35 or <21 days) contribute additional risk
    if data.cycle_length_days > 35 or data.cycle_length_days < 21:
        risk_score += 0.15

    risk_probability = min(round(risk_score, 2), 1.0)

    # Classify risk tier
    if risk_probability > 0.6:
        classification = "High"
    elif risk_probability > 0.3:
        classification = "Moderate"
    else:
        classification = "Low"

    return {
        "pcos_risk_probability": risk_probability,
        "risk_classification": classification,
        "message": "AI-generated risk index. Consult a certified gynecologist for medical confirmation."
    }


# ─── Cycle Analytics ────────────────────────────────────────

@router.post("/analytics/cycle-summary")
async def get_cycle_summary(data: CycleHistoryInput):
    """
    Analyze menstrual cycle history to compute average length,
    predict next period date, and flag anomalies.
    """
    try:
        metrics = CycleEngine.calculate_metrics(data.history)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Data processing error: {str(e)}")


# ─── Phase-Based Recommendations ────────────────────────────

@router.post("/analytics/recommendations")
async def get_phase_recommendations(data: RecommendationInput):
    """
    Return personalized diet, activity, and wellness recommendations
    based on the current day in the menstrual cycle.
    """
    try:
        return WellnessEngine.get_recommendations(data.day_in_cycle)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Recommendation pipeline error: {str(e)}")
