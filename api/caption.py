from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import tempfile
from api.utils import UPLOAD_DIR, get_file_hash, check_cache, preprocess_audio, get_audio_duration, save_to_cache, detect_language_with_whisper
from models.langid_model import detect_language

router = APIRouter()



@router.post("/caption/live-audio/")
async def caption_audio(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided.")
        file_ext = os.path.splitext(file.filename)[1]
        if file_ext not in [".mp3", ".wav"]:
            raise HTTPException(400, detail="Only MP3 and WAV files are supported")
        file_hash = get_file_hash(contents)
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(413, detail="File size exceeds 10MB")
        if cached := check_cache(file_hash):
            cached["cached"] = True
            return JSONResponse(content=cached)
        temp_path = f"{UPLOAD_DIR}/{file_hash}{file_ext}"
        with open(temp_path, "wb") as f:
            f.write(contents)
        detected_lang = detect_language_with_whisper(temp_path)
        duration = get_audio_duration(temp_path)
        # For simplicity, just return detected language and duration
        result = {
            "language": detected_lang,
            "duration_ms": duration
        }
        save_to_cache(file_hash, result)
        return JSONResponse(content=result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=f"Audio processing error: {str(e)}") 
    
    
    
@router.get("/caption/health")
def caption_health():
    return {"status": "caption module ready"} 