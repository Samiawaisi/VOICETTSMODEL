import edge_tts
import asyncio
import uuid
import os
from pathlib import Path
from typing import Optional
from config import OUTPUT_DIR, DEFAULT_VOICE, DEFAULT_RATE, DEFAULT_PITCH, DEFAULT_VOLUME
from utils.text_chunker import TextChunker
from utils.audio_utils import merge_audio_files, get_audio_duration


class TTSService:
    """Service for converting text to speech using Microsoft Edge TTS."""

    def __init__(self):
        self.chunker = TextChunker()

    async def generate_speech(
        self,
        text: str,
        voice: str = DEFAULT_VOICE,
        rate: str = DEFAULT_RATE,
        pitch: str = DEFAULT_PITCH,
        volume: str = DEFAULT_VOLUME,
        output_format: str = "mp3"
    ) -> dict:
        """Generate speech from text. Handles long text by chunking."""
        if not text.strip():
            raise ValueError("Text cannot be empty")

        file_id = str(uuid.uuid4())

        # Check if text needs chunking
        chunks = self.chunker.chunk_text(text)

        if len(chunks) == 1:
            # Single chunk - direct conversion
            output_path = OUTPUT_DIR / f"{file_id}.{output_format}"
            await self._convert_chunk(chunks[0], str(output_path), voice, rate, pitch, volume)
        else:
            # Multiple chunks - convert each then merge
            chunk_files = []
            for i, chunk in enumerate(chunks):
                chunk_path = OUTPUT_DIR / f"{file_id}_chunk_{i}.mp3"
                await self._convert_chunk(chunk, str(chunk_path), voice, rate, pitch, volume)
                chunk_files.append(str(chunk_path))

            output_path = OUTPUT_DIR / f"{file_id}.{output_format}"
            await merge_audio_files(chunk_files, str(output_path))

            # Cleanup chunk files
            for f in chunk_files:
                try:
                    os.remove(f)
                except OSError:
                    pass

        duration = await get_audio_duration(str(output_path))

        return {
            "file_id": file_id,
            "filename": f"{file_id}.{output_format}",
            "path": str(output_path),
            "duration": duration,
            "chunks_used": len(chunks),
            "voice": voice,
            "format": output_format
        }

    async def _convert_chunk(
        self,
        text: str,
        output_path: str,
        voice: str,
        rate: str,
        pitch: str,
        volume: str
    ) -> None:
        """Convert a single text chunk to audio."""
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=rate,
            pitch=pitch,
            volume=volume
        )
        await communicate.save(output_path)

    async def generate_speech_stream(
        self,
        text: str,
        voice: str = DEFAULT_VOICE,
        rate: str = DEFAULT_RATE,
        pitch: str = DEFAULT_PITCH,
        volume: str = DEFAULT_VOLUME
    ):
        """Stream audio data for real-time playback."""
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=rate,
            pitch=pitch,
            volume=volume
        )
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                yield chunk["data"]

    def get_output_files(self) -> list:
        """List all generated audio files."""
        files = []
        for f in OUTPUT_DIR.iterdir():
            if f.suffix in [".mp3", ".wav"] and "_chunk_" not in f.name:
                files.append({
                    "filename": f.name,
                    "size": f.stat().st_size,
                    "created": f.stat().st_ctime
                })
        return sorted(files, key=lambda x: x["created"], reverse=True)

    def delete_output_file(self, filename: str) -> bool:
        """Delete a generated audio file."""
        file_path = OUTPUT_DIR / filename
        if file_path.exists() and file_path.parent == OUTPUT_DIR:
            file_path.unlink()
            return True
        return False
