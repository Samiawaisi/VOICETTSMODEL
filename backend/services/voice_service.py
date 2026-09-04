import edge_tts
import asyncio
from typing import Optional
from gtts import lang as gtts_lang


class VoiceService:
    """Service for managing Microsoft Edge TTS and Google TTS voices."""

    def __init__(self):
        self._edge_voices_cache = None
        self._google_voices_cache = None

    def _extract_character_name(self, short_name: str, friendly_name: str) -> str:
        """Extract a clean character/person name from voice metadata."""
        # e.g., "ur-PK-UzmaNeural" -> "Uzma"
        # e.g., "en-US-AriaNeural" -> "Aria"
        parts = short_name.split("-")
        if len(parts) >= 3:
            name_part = parts[-1]  # e.g. "UzmaNeural" or "AriaNeural"
            if name_part.endswith("Neural"):
                return name_part[:-6]
            elif name_part.endswith("Standard"):
                return name_part[:-8]
            return name_part

        # Fallback to FriendlyName
        if "Online" in friendly_name:
            sub = friendly_name.split("Online")[0].replace("Microsoft", "").strip()
            if sub:
                return sub
        return short_name

    async def get_all_voices(self, engine: Optional[str] = None) -> list:
        """Fetch available voices for Edge, Google, or both engines."""
        edge_voices = await self._get_edge_voices()
        google_voices = self._get_google_voices()

        if engine == "edge":
            return edge_voices
        elif engine == "google":
            return google_voices

        return edge_voices + google_voices

    async def _get_edge_voices(self) -> list:
        """Fetch and format all available voices from Edge TTS."""
        if self._edge_voices_cache is None:
            raw_voices = await edge_tts.list_voices()
            formatted = []
            for v in raw_voices:
                short_name = v.get("ShortName", "")
                friendly_name = v.get("FriendlyName", "")
                gender = v.get("Gender", "Unknown")
                locale = v.get("Locale", "")

                char_name = self._extract_character_name(short_name, friendly_name)
                icon = "👩" if gender.lower() == "female" else ("👨" if gender.lower() == "male" else "🎙️")

                display_name = f"{icon} {char_name} - {locale} ({gender})"

                formatted.append({
                    "ShortName": short_name,
                    "FriendlyName": friendly_name,
                    "CharacterName": char_name,
                    "DisplayName": display_name,
                    "Gender": gender,
                    "Locale": locale,
                    "Engine": "edge"
                })
            self._edge_voices_cache = formatted
        return self._edge_voices_cache

    def _get_google_voices(self) -> list:
        """Get formatted list of Google TTS supported languages/voices."""
        if self._google_voices_cache is None:
            langs = gtts_lang.tts_langs()
            formatted = []
            for code, name in sorted(langs.items(), key=lambda x: x[1]):
                formatted.append({
                    "ShortName": f"google-{code}",
                    "FriendlyName": f"Google TTS - {name} ({code})",
                    "CharacterName": f"Google {name}",
                    "DisplayName": f"🌐 Google {name} ({code})",
                    "Gender": "Neutral",
                    "Locale": code,
                    "Engine": "google",
                    "LangCode": code
                })
            self._google_voices_cache = formatted
        return self._google_voices_cache

    async def get_voices_by_language(self, language: str, engine: Optional[str] = None) -> list:
        """Filter voices by language code (e.g., 'en', 'ur', 'hi')."""
        all_voices = await self.get_all_voices(engine)
        lang_lower = language.lower()
        return [
            v for v in all_voices
            if v["Locale"].lower().startswith(lang_lower) or v["Locale"].lower() == lang_lower
        ]

    async def get_voices_by_gender(self, gender: str, engine: Optional[str] = None) -> list:
        """Filter voices by gender ('Male' or 'Female')."""
        all_voices = await self.get_all_voices(engine)
        return [
            v for v in all_voices
            if v.get("Gender", "").lower() == gender.lower()
        ]

    async def search_voices(self, query: str, engine: Optional[str] = None) -> list:
        """Search voices by name, character name, language, or locale."""
        all_voices = await self.get_all_voices(engine)
        query_lower = query.lower()
        return [
            v for v in all_voices
            if query_lower in v["ShortName"].lower()
            or query_lower in v.get("CharacterName", "").lower()
            or query_lower in v.get("Locale", "").lower()
            or query_lower in v.get("FriendlyName", "").lower()
            or query_lower in v.get("DisplayName", "").lower()
        ]

    async def get_voice_info(self, voice_name: str) -> Optional[dict]:
        """Get detailed info about a specific voice."""
        all_voices = await self.get_all_voices()
        for v in all_voices:
            if v["ShortName"] == voice_name:
                return v
        return None

    async def get_languages(self, engine: Optional[str] = None) -> list:
        """Get list of available languages."""
        all_voices = await self.get_all_voices(engine)
        languages = set()
        for v in all_voices:
            locale = v.get("Locale", "")
            if locale:
                lang = locale.split("-")[0]
                languages.add(lang)
        return sorted(list(languages))

    async def refresh_cache(self) -> list:
        """Force refresh the voices cache."""
        self._edge_voices_cache = None
        self._google_voices_cache = None
        return await self.get_all_voices()
