"""
Project Abhaya — Chat Routes
Endpoint: Gemini AI-powered chatbot for women's health queries.
"""

from fastapi import APIRouter
from google import genai
from google.genai import types

from app.config import get_settings
from app.models.schemas import ChatMessage


router = APIRouter(prefix="/api", tags=["AI Chatbot"])

# System persona for Abhaya AI
ABHAYA_SYSTEM_PROMPT = (
    "You are Abhaya AI, a supportive, safe, empathetic, and professional AI companion "
    "for women's reproductive health wellness. You specialize in:\n"
    "- Menstrual cycle education and myth-busting\n"
    "- PCOS/PCOD awareness and lifestyle guidance\n"
    "- Mental wellness and stress reduction techniques\n"
    "- Nutrition and exercise aligned with cycle phases\n\n"
    "Rules:\n"
    "- Always be warm, encouraging, and non-judgmental\n"
    "- Never provide medical diagnoses — recommend consulting a doctor for specific conditions\n"
    "- Keep responses concise (2-4 paragraphs max) and easy to understand\n"
    "- Use emojis sparingly for warmth 🌸\n"
    "- If unsure, say so honestly and suggest professional consultation"
)


@router.post("/chat/abhaya-bot")
async def consult_chatbot(payload: ChatMessage):
    """
    Send a user message to Gemini AI with the Abhaya health persona.
    Falls back gracefully if the API key is missing or invalid.
    """
    settings = get_settings()

    try:
        # Initialize client with the configured API key
        ai_client = genai.Client(api_key=settings.gemini_api_key)

        # Configure generation parameters
        config = types.GenerateContentConfig(
            system_instruction=ABHAYA_SYSTEM_PROMPT,
            temperature=0.7
        )

        # Generate response using Gemini
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=payload.message,
            config=config
        )

        return {"response": response.text}

    except Exception as e:
        # Graceful fallback when API key is missing or request fails
        error_msg = str(e)

        if "api_key" in error_msg.lower() or "invalid" in error_msg.lower():
            return {
                "response": (
                    "🌸 I'm currently unable to connect to my AI engine. "
                    "Please ensure the GEMINI_API_KEY is configured in the backend .env file. "
                    "Visit https://aistudio.google.com/apikey to get a free API key."
                )
            }

        return {
            "response": (
                f"🌸 I encountered an issue processing your question. "
                f"Please try again in a moment. (Debug: {error_msg})"
            )
        }
