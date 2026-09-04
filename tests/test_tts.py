import pytest
import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.tts_service import TTSService


class TestTTSService:
    """Tests for TTS Service."""

    def setup_method(self):
        self.tts = TTSService()

    def test_service_initialization(self):
        assert self.tts is not None
        assert self.tts.chunker is not None

    @pytest.mark.asyncio
    async def test_generate_short_text(self):
        result = await self.tts.generate_speech(
            text="Hello, this is a test.",
            voice="en-US-AriaNeural"
        )
        assert result["file_id"] is not None
        assert result["filename"].endswith(".mp3")
        assert result["chunks_used"] == 1
        assert os.path.exists(result["path"])
        # Cleanup
        os.remove(result["path"])

    @pytest.mark.asyncio
    async def test_empty_text_raises_error(self):
        with pytest.raises(ValueError, match="Text cannot be empty"):
            await self.tts.generate_speech(text="")

    @pytest.mark.asyncio
    async def test_generate_with_custom_settings(self):
        result = await self.tts.generate_speech(
            text="Testing custom voice settings.",
            voice="en-US-GuyNeural",
            rate="+20%",
            pitch="+5Hz"
        )
        assert result["voice"] == "en-US-GuyNeural"
        assert os.path.exists(result["path"])
        # Cleanup
        os.remove(result["path"])

    def test_get_output_files(self):
        files = self.tts.get_output_files()
        assert isinstance(files, list)
