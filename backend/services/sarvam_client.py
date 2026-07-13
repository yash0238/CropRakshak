"""
Sarvam AI client
=================
Thin async wrapper around Sarvam AI's OpenAI-compatible Chat Completions API
(https://api.sarvam.ai/v1/chat/completions).

Why Sarvam: it's built India-first and handles Hindi/Marathi/Tamil/Telugu (and
other Indian languages) more naturally than a general-purpose model — a good
fit for a farmer-facing assistant.

Design notes:
- Uses httpx (already a project dependency) — no extra SDK to install.
- Auth uses the `api-subscription-key` header (Sarvam's recommended header).
- `is_sarvam_enabled()` lets callers decide whether to use Sarvam or fall back
  to Gemini, so the app runs fine even when SARVAM_API_KEY is not set.
"""

from typing import List, Dict, Optional
import base64
import io
import wave
import httpx

from config import settings


def is_sarvam_enabled() -> bool:
    """True only when a Sarvam API key is configured."""
    return bool(settings.SARVAM_API_KEY)


class SarvamError(Exception):
    """Raised when a Sarvam API call fails."""


async def sarvam_chat(
    messages: List[Dict[str, str]],
    *,
    temperature: float = 0.7,
    max_tokens: int = 4096,
    timeout: float = 90.0,
) -> str:
    """
    Send an OpenAI-style `messages` list to Sarvam and return the assistant text.

    messages = [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."},
    ]
    """
    if not settings.SARVAM_API_KEY:
        raise SarvamError("SARVAM_API_KEY is not configured.")

    payload = {
        "model": settings.SARVAM_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    headers = {
        "api-subscription-key": settings.SARVAM_API_KEY,
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(
                settings.SARVAM_API_URL, json=payload, headers=headers
            )
    except httpx.HTTPError as exc:
        raise SarvamError(f"Could not reach Sarvam API: {exc}") from exc

    if resp.status_code != 200:
        raise SarvamError(
            f"Sarvam API returned {resp.status_code}: {resp.text[:300]}"
        )

    data = resp.json()
    try:
        message = data["choices"][0]["message"]
        content = message.get("content")
    except (KeyError, IndexError, AttributeError) as exc:
        raise SarvamError(f"Unexpected Sarvam response shape: {data}") from exc

    # Sarvam's reasoning models (e.g. sarvam-30b/105b) stream their chain of
    # thought into `reasoning_content` and the user-facing answer into
    # `content`. If the token budget is exhausted during reasoning, `content`
    # comes back null (finish_reason == "length"). Treat that as a failure so
    # the caller can fall back rather than returning an empty reply.
    if not content:
        finish = data["choices"][0].get("finish_reason")
        raise SarvamError(
            f"Sarvam returned empty content (finish_reason={finish}). "
            "Try a larger max_tokens."
        )

    return content.strip()


# Language names Sarvam/LLMs understand, keyed by the app's locale codes.
LANGUAGE_NAMES: Dict[str, str] = {
    "en": "English",
    "hi": "Hindi (हिंदी)",
    "mr": "Marathi (मराठी)",
    "ta": "Tamil (தமிழ்)",
    "te": "Telugu (తెలుగు)",
}

# BCP-47 codes Sarvam's speech APIs expect, keyed by the app's locale codes.
SPEECH_LANG_CODES: Dict[str, str] = {
    "en": "en-IN",
    "hi": "hi-IN",
    "mr": "mr-IN",
    "ta": "ta-IN",
    "te": "te-IN",
}


def language_name(code: str) -> str:
    """Map a locale code to a human language name (defaults to English)."""
    return LANGUAGE_NAMES.get(code, "English")


def speech_lang_code(code: str) -> str:
    """Map an app locale code to a Sarvam speech BCP-47 code."""
    return SPEECH_LANG_CODES.get(code, "en-IN")


# --- Speech-to-Text (Saarika ASR) -----------------------------------------

SARVAM_STT_URL = "https://api.sarvam.ai/speech-to-text"
SARVAM_STT_MODEL = "saarika:v2.5"


async def sarvam_transcribe(
    audio_bytes: bytes,
    filename: str = "audio.webm",
    content_type: str = "audio/webm",
    language: str = "unknown",
    timeout: float = 60.0,
) -> Dict[str, str]:
    """
    Transcribe speech to text using Sarvam's Saarika ASR.

    `language` is an app locale code ("hi", "en", ...) or "unknown" for
    auto-detection. Returns {"transcript": ..., "language_code": ...}.
    """
    if not settings.SARVAM_API_KEY:
        raise SarvamError("SARVAM_API_KEY is not configured.")

    lang = "unknown" if language == "unknown" else speech_lang_code(language)
    headers = {"api-subscription-key": settings.SARVAM_API_KEY}
    files = {"file": (filename, audio_bytes, content_type)}
    data = {"model": SARVAM_STT_MODEL, "language_code": lang}

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(
                SARVAM_STT_URL, headers=headers, files=files, data=data
            )
    except httpx.HTTPError as exc:
        raise SarvamError(f"Could not reach Sarvam STT API: {exc}") from exc

    if resp.status_code != 200:
        raise SarvamError(
            f"Sarvam STT returned {resp.status_code}: {resp.text[:300]}"
        )

    body = resp.json()
    return {
        "transcript": body.get("transcript", ""),
        "language_code": body.get("language_code", lang),
    }


# --- Text-to-Speech (Bulbul) ----------------------------------------------

SARVAM_TTS_URL = "https://api.sarvam.ai/text-to-speech"
SARVAM_TTS_MODEL = "bulbul:v2"
SARVAM_TTS_SPEAKER = "anushka"

# Natural Indian voices (Bulbul v2) picked per language. All are India-first
# voices; these choices sound warm and clear for a farmer assistant.
SPEAKER_BY_LANG: Dict[str, str] = {
    "en": "anushka",   # clear Indian-English female
    "hi": "manisha",   # warm natural Hindi female
    "mr": "manisha",
    "ta": "vidya",
    "te": "vidya",
}


def tts_speaker(language: str) -> str:
    """Choose a natural Indian voice for the given app locale code."""
    return SPEAKER_BY_LANG.get(language, SARVAM_TTS_SPEAKER)


async def sarvam_tts(
    text: str,
    language: str = "en",
    speaker: Optional[str] = None,
    timeout: float = 60.0,
) -> str:
    """
    Convert text to speech via Sarvam's Bulbul TTS.

    Returns a single base64-encoded WAV string (the API returns a list of
    audio chunks; we join them). `language` is an app locale code.
    """
    if not settings.SARVAM_API_KEY:
        raise SarvamError("SARVAM_API_KEY is not configured.")

    # Bulbul v2 caps text length per request; keep it safe.
    text = text[:1500]

    payload = {
        "text": text,
        "target_language_code": speech_lang_code(language),
        "speaker": speaker or tts_speaker(language),
        "model": SARVAM_TTS_MODEL,
    }
    headers = {
        "api-subscription-key": settings.SARVAM_API_KEY,
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(SARVAM_TTS_URL, json=payload, headers=headers)
    except httpx.HTTPError as exc:
        raise SarvamError(f"Could not reach Sarvam TTS API: {exc}") from exc

    if resp.status_code != 200:
        raise SarvamError(
            f"Sarvam TTS returned {resp.status_code}: {resp.text[:300]}"
        )

    audios = resp.json().get("audios") or []
    if not audios:
        raise SarvamError("Sarvam TTS returned no audio.")
    # Bulbul splits longer text into several WAV chunks. Each chunk is a
    # complete WAV file (with its own 44-byte header), so we can't just
    # string-concatenate the base64 — that yields a corrupt file the browser
    # refuses to play. Merge them into one valid WAV instead.
    if len(audios) == 1:
        return audios[0]
    return _merge_wav_base64(audios)


def _merge_wav_base64(audios: List[str]) -> str:
    """Merge multiple base64-encoded WAV chunks into a single base64 WAV."""
    frames = bytearray()
    params = None
    for b64 in audios:
        raw = base64.b64decode(b64)
        with wave.open(io.BytesIO(raw), "rb") as w:
            if params is None:
                params = w.getparams()
            frames.extend(w.readframes(w.getnframes()))

    out = io.BytesIO()
    with wave.open(out, "wb") as w:
        w.setnchannels(params.nchannels)
        w.setsampwidth(params.sampwidth)
        w.setframerate(params.framerate)
        w.writeframes(bytes(frames))
    return base64.b64encode(out.getvalue()).decode("ascii")
