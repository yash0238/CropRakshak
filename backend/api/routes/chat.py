"""
Chat API Routes
Multilingual AI chat assistant.

Primary engine: Sarvam AI (India-first LLM — better Indian-language answers).
Fallback engine: Google Gemini (used automatically if SARVAM_API_KEY is unset
or a Sarvam call fails), so the assistant always responds.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import google.generativeai as genai
from config import settings
from services.sarvam_client import (
    sarvam_chat,
    sarvam_transcribe,
    sarvam_tts,
    is_sarvam_enabled,
    language_name,
    SarvamError,
)

genai.configure(api_key=settings.GOOGLE_API_KEY)

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    language: str = "en"
    context: dict = {}
    sessionId: str = None


def _build_system_prompt(request: "ChatRequest") -> str:
    """Shared system prompt used by both Sarvam and Gemini."""
    return f"""You are Krishivaani, a helpful agricultural assistant for farmers.

Respond in {language_name(request.language)}.

Context:
- Farmer's location: {request.context.get('location', 'Unknown')}
- Current crop: {request.context.get('crop', 'Unknown')}
- Farm size: {request.context.get('farmSize', 'Unknown')} acres

Guidelines:
- Be friendly, simple, and farmer-friendly
- Provide practical, actionable advice
- If you don't know, say so
- For complex questions, break down the answer
- Use local context when available"""


async def _gemini_reply(system_prompt: str, user_message: str) -> str:
    """Fallback path: Google Gemini."""
    model = genai.GenerativeModel(settings.GEMINI_MODEL_FLASH)
    full_prompt = f"{system_prompt}\n\nFarmer's Question: {user_message}"
    response = model.generate_content(full_prompt)
    return response.text


@router.post("/message")
async def send_chat_message(request: ChatRequest):
    """Send chat message to Krishivaani Assistant."""

    system_prompt = _build_system_prompt(request)
    engine = "gemini"
    reply_text = None

    # 1) Try Sarvam first when configured.
    if is_sarvam_enabled():
        try:
            reply_text = await sarvam_chat(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": request.message},
                ],
                temperature=settings.GEMINI_TEMPERATURE,
            )
            engine = "sarvam"
        except SarvamError:
            reply_text = None  # fall through to Gemini

    # 2) Fallback to Gemini.
    if reply_text is None:
        try:
            reply_text = await _gemini_reply(system_prompt, request.message)
            engine = "gemini"
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(content={
        "success": True,
        "data": {
            "response": reply_text,
            "language": request.language,
            "engine": engine,
            "sessionId": request.sessionId,
        }
    })


class SpeakRequest(BaseModel):
    text: str
    language: str = "en"


@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = Form("unknown"),
):
    """
    Speech-to-Text: farmer records a question, we return the transcript.
    Uses Sarvam Saarika ASR. Requires SARVAM_API_KEY (voice has no Gemini
    fallback, since Gemini here is text-only in this app).
    """
    if not is_sarvam_enabled():
        raise HTTPException(
            status_code=503,
            detail="Voice input needs SARVAM_API_KEY to be configured.",
        )

    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty audio upload.")

    try:
        result = await sarvam_transcribe(
            audio_bytes,
            filename=file.filename or "audio.webm",
            content_type=file.content_type or "audio/webm",
            language=language or "unknown",
        )
    except SarvamError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return JSONResponse(content={
        "success": True,
        "data": {
            "transcript": result["transcript"],
            "language_code": result["language_code"],
        },
    })


@router.post("/speak")
async def speak_text(request: SpeakRequest):
    """
    Text-to-Speech: read an answer aloud in the farmer's language.
    Returns base64-encoded WAV audio. Uses Sarvam Bulbul TTS.
    """
    if not is_sarvam_enabled():
        raise HTTPException(
            status_code=503,
            detail="Voice output needs SARVAM_API_KEY to be configured.",
        )

    if not request.text.strip():
        raise HTTPException(status_code=400, detail="No text to speak.")

    try:
        audio_b64 = await sarvam_tts(request.text, language=request.language)
    except SarvamError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return JSONResponse(content={
        "success": True,
        "data": {"audio": audio_b64, "format": "wav"},
    })


@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "chat"}
