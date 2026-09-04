import edge_tts
import asyncio
from typing import Optional


class VoiceService:
    """Service for managing Microsoft Edge TTS voices."""

    def __init__(self):
        self._voices_cache = None

    async def get_all_voices(self) -> list:
        """Fetch all available voices from Edge TTS."""
        if self._voices_cache is None:
            voices = await edge_tts.list_voices()
            self._voices_cache = voices
        return self._voices_cache

    async def get_voices_by_language(self, language: str) -> list:
        """Filter voices by language code (e.g., 'en', 'ur', 'hi')."""
        all_voices = await self.get_all_voices()
        return [
            v for v in all_voices
            if v["Locale"].lower().startswith(language.lower())
        ]

    async def get_voices_by_gender(self, gender: str) -> list:
        """Filter voices by gender ('Male' or 'Female')."""
        all_voices = await self.get_all_voices()
        return [
            v for v in all_voices
            if v.get("Gender", "").lower() == gender.lower()
        ]

    async def search_voices(self, query: str) -> list:
        """Search voices by name, language, or locale."""
        all_voices = await self.get_all_voices()
        query_lower = query.lower()
        return [
            v for v in all_voices
            if query_lower in v["ShortName"].lower()
            or query_lower in v.get("Locale", "").lower()
            or query_lower in v.get("FriendlyName", "").lower()
        ]

    async def get_voice_info(self, voice_name: str) -> Optional[dict]:
        """Get detailed info about a specific voice."""
        all_voices = await self.get_all_voices()
        for v in all_voices:
            if v["ShortName"] == voice_name:
                return v
        return None

    async def get_languages(self) -> list:
        """Get list of available languages."""
        all_voices = await self.get_all_voices()
        languages = set()
        for v in all_voices:
            locale = v.get("Locale", "")
            if locale:
                lang = locale.split("-")[0]
                languages.add(lang)
        return sorted(list(languages))

    async def refresh_cache(self) -> list:
        """Force refresh the voices cache."""
        self._voices_cache = None
        return await self.get_all_voices()
