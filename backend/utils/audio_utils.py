import os
import asyncio
from pathlib import Path
from typing import List, Optional


async def merge_audio_files(file_paths: List[str], output_path: str) -> str:
    """Merge multiple audio files into one."""
    try:
        from pydub import AudioSegment

        combined = AudioSegment.empty()
        for file_path in file_paths:
            if os.path.exists(file_path):
                audio = AudioSegment.from_mp3(file_path)
                combined += audio

        # Export based on file extension
        output_format = Path(output_path).suffix.lstrip(".")
        if output_format == "wav":
            combined.export(output_path, format="wav")
        else:
            combined.export(output_path, format="mp3")

        return output_path
    except ImportError:
        # Fallback: simple binary concatenation for MP3
        with open(output_path, "wb") as outfile:
            for file_path in file_paths:
                if os.path.exists(file_path):
                    with open(file_path, "rb") as infile:
                        outfile.write(infile.read())
        return output_path


async def get_audio_duration(file_path: str) -> Optional[float]:
    """Get the duration of an audio file in seconds."""
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(file_path)
        return len(audio) / 1000.0  # Convert ms to seconds
    except Exception:
        return None


async def convert_format(input_path: str, output_format: str) -> str:
    """Convert audio file to a different format."""
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(input_path)
        output_path = str(Path(input_path).with_suffix(f".{output_format}"))
        audio.export(output_path, format=output_format)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Audio conversion failed: {str(e)}")


def get_file_size_mb(file_path: str) -> float:
    """Get file size in megabytes."""
    return os.path.getsize(file_path) / (1024 * 1024)
