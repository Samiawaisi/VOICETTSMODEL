from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from services.voice_service import VoiceService

router = APIRouter()
voice_service = VoiceService()


@router.get("/")
async def get_voices(
    language: Optional[str] = Query(None, description="Filter by language code (e.g., 'en', 'ur', 'hi')"),
    gender: Optional[str] = Query(None, description="Filter by gender ('Male' or 'Female')"),
    search: Optional[str] = Query(None, description="Search voices by name or locale"),
    engine: Optional[str] = Query(None, description="Filter by TTS engine ('edge' or 'google')")
):
    """Get available TTS voices with optional filters."""
    try:
        if search:
            voices = await voice_service.search_voices(search, engine=engine)
        elif language and gender:
            lang_voices = await voice_service.get_voices_by_language(language, engine=engine)
            voices = [v for v in lang_voices if v.get("Gender", "").lower() == gender.lower()]
        elif language:
            voices = await voice_service.get_voices_by_language(language, engine=engine)
        elif gender:
            voices = await voice_service.get_voices_by_gender(gender, engine=engine)
        else:
            voices = await voice_service.get_all_voices(engine=engine)

        return {
            "voices": voices,
            "total": len(voices)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch voices: {str(e)}")


@router.get("/languages")
async def get_languages(engine: Optional[str] = Query(None)):
    """Get list of available languages."""
    languages = await voice_service.get_languages(engine=engine)
    return {"languages": languages, "total": len(languages)}


@router.get("/{voice_name}")
async def get_voice_info(voice_name: str):
    """Get detailed info about a specific voice."""
    voice = await voice_service.get_voice_info(voice_name)
    if voice is None:
        raise HTTPException(status_code=404, detail=f"Voice '{voice_name}' not found")
    return voice


@router.post("/refresh")
async def refresh_voices():
    """Refresh the voices cache."""
    voices = await voice_service.refresh_cache()
    return {"message": "Cache refreshed", "total": len(voices)}
