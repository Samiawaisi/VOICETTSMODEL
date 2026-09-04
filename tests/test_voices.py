import pytest
import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.voice_service import VoiceService


class TestVoiceService:
    """Tests for Voice Service."""

    def setup_method(self):
        self.voice_service = VoiceService()

    @pytest.mark.asyncio
    async def test_get_all_voices(self):
        voices = await self.voice_service.get_all_voices()
        assert isinstance(voices, list)
        assert len(voices) > 0

    @pytest.mark.asyncio
    async def test_get_english_voices(self):
        voices = await self.voice_service.get_voices_by_language("en")
        assert len(voices) > 0
        for v in voices:
            assert v["Locale"].startswith("en")

    @pytest.mark.asyncio
    async def test_get_urdu_voices(self):
        voices = await self.voice_service.get_voices_by_language("ur")
        assert isinstance(voices, list)

    @pytest.mark.asyncio
    async def test_get_female_voices(self):
        voices = await self.voice_service.get_voices_by_gender("Female")
        assert len(voices) > 0
        for v in voices:
            assert v["Gender"] == "Female"

    @pytest.mark.asyncio
    async def test_search_voices(self):
        voices = await self.voice_service.search_voices("Aria")
        assert len(voices) > 0

    @pytest.mark.asyncio
    async def test_get_voice_info(self):
        voice = await self.voice_service.get_voice_info("en-US-AriaNeural")
        assert voice is not None
        assert voice["ShortName"] == "en-US-AriaNeural"

    @pytest.mark.asyncio
    async def test_get_languages(self):
        languages = await self.voice_service.get_languages()
        assert "en" in languages

    @pytest.mark.asyncio
    async def test_voice_not_found(self):
        voice = await self.voice_service.get_voice_info("nonexistent-voice")
        assert voice is None

    @pytest.mark.asyncio
    async def test_cache_refresh(self):
        voices = await self.voice_service.refresh_cache()
        assert isinstance(voices, list)
        assert len(voices) > 0
