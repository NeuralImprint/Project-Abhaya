"""
Project Abhaya — Pydantic Schemas
All request/response models for the API.
"""

from pydantic import BaseModel, Field
from typing import List, Dict


# ─── PCOS Risk Assessment ───────────────────────────────────

class PCOSAssessmentInput(BaseModel):
    """Input schema for the PCOS risk prediction endpoint."""
    age: int = Field(..., ge=13, le=50, description="Patient age (13–50)")
    cycle_length_days: int = Field(..., description="Average menstrual cycle length in days")
    weight_gain_sudden: bool = Field(..., description="Recent unexplained weight gain")
    hair_growth_excessive: bool = Field(..., description="Excessive facial/body hair growth")
    skin_darkening: bool = Field(..., description="Skin darkening (acanthosis nigricans)")
    mood_swings_severity: int = Field(..., ge=1, le=5, description="Mood swing severity (1=mild, 5=severe)")


class PCOSRiskOutput(BaseModel):
    """Response schema for PCOS risk prediction."""
    pcos_risk_probability: float
    risk_classification: str
    message: str


# ─── Chatbot ────────────────────────────────────────────────

class ChatMessage(BaseModel):
    """Input schema for the AI chatbot endpoint."""
    message: str = Field(..., min_length=1, description="User's question or message")


class ChatResponse(BaseModel):
    """Response schema for the AI chatbot."""
    response: str


# ─── Cycle Analytics ────────────────────────────────────────

class CycleHistoryInput(BaseModel):
    """Input schema for cycle history analysis."""
    history: List[Dict[str, str]] = Field(
        ...,
        description="List of cycle records with 'start_date' keys in YYYY-MM-DD format"
    )


# ─── Phase Recommendations ──────────────────────────────────

class RecommendationInput(BaseModel):
    """Input schema for phase-based wellness recommendations."""
    day_in_cycle: int = Field(..., ge=1, le=45, description="Current day in the menstrual cycle")


# ─── Community ──────────────────────────────────────────────

class CommunityPostInput(BaseModel):
    """Input schema for creating a new community post."""
    title: str = Field(..., min_length=1, description="Post title")
    content: str = Field(..., min_length=1, description="Post content/experience")
