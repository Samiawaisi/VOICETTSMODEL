from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional
from services.tts_service import TTSService
from config import OUTPUT_DIR

router = APIRouter()
tts_service = TTSService()


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=100000, description="Text to convert to speech")
    voice: str = Field(default="en-US-AriaNeural", description="Voice name")
    rate: str = Field(default="+0%", description="Speech rate (e.g., '+50%', '-25%')")
    pitch: str = Field(default="+0Hz", description="Speech pitch (e.g., '+10Hz', '-5Hz')")
    volume: str = Field(default="+0%", description="Speech volume (e.g., '+50%', '-25%')")
    output_format: str = Field(default="mp3", description="Output format: mp3 or wav")


class TTSResponse(BaseModel):
    file_id: str
    filename: str
    duration: Optional[float]
    chunks_used: int
    voice: str
    format: str
    download_url: str


@router.post("/generate", response_model=TTSResponse)
async def generate_speech(request: TTSRequest):
    """Generate speech from text."""
    try:
        result = await tts_service.generate_speech(
            text=request.text,
            voice=request.voice,
            rate=request.rate,
            pitch=request.pitch,
            volume=request.volume,
            output_format=request.output_format
        )
        return TTSResponse(
            file_id=result["file_id"],
            filename=result["filename"],
            duration=result["duration"],
            chunks_used=result["chunks_used"],
            voice=result["voice"],
            format=result["format"],
            download_url=f"/output/{result['filename']}"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")


@router.get("/download/{filename}")
async def download_file(filename: str):
    """Download a generated audio file."""
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(
        str(file_path),
        media_type="audio/mpeg",
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.post("/stream")
async def stream_speech(request: TTSRequest):
    """Stream generated speech audio."""
    try:
        return StreamingResponse(
            tts_service.generate_speech_stream(
                text=request.text,
                voice=request.voice,
                rate=request.rate,
                pitch=request.pitch,
                volume=request.volume
            ),
            media_type="audio/mpeg"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Streaming failed: {str(e)}")


@router.get("/history")
async def get_history():
    """Get list of generated audio files."""
    files = tts_service.get_output_files()
    return {"files": files, "total": len(files)}


@router.delete("/history/{filename}")
async def delete_file(filename: str):
    """Delete a generated audio file."""
    if tts_service.delete_output_file(filename):
        return {"message": "File deleted successfully"}
    raise HTTPException(status_code=404, detail="File not found")
