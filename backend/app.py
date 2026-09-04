import os
import sys
from pathlib import Path

# Add backend directory to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from config import HOST, PORT, DEBUG, ALLOWED_ORIGINS, OUTPUT_DIR
from api.tts_routes import router as tts_router
from api.voice_routes import router as voice_router

# Load environment variables
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

app = FastAPI(
    title="Edge TTS Studio",
    description="A powerful Text-to-Speech tool using Microsoft Edge TTS",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(tts_router, prefix="/api/tts", tags=["Text-to-Speech"])
app.include_router(voice_router, prefix="/api/voices", tags=["Voices"])

# Serve output files
app.mount("/output", StaticFiles(directory=str(OUTPUT_DIR)), name="output")

# Serve frontend
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dir / "assets")), name="assets")
    app.mount("/css", StaticFiles(directory=str(frontend_dir / "css")), name="css")
    app.mount("/js", StaticFiles(directory=str(frontend_dir / "js")), name="js")

    @app.get("/")
    async def serve_frontend():
        return FileResponse(str(frontend_dir / "index.html"))


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Edge TTS Studio is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host=HOST, port=PORT, reload=DEBUG)
