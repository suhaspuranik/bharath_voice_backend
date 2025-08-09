from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import tempfile
import logging
from api.utils import UPLOAD_DIR, get_file_hash, check_cache, preprocess_audio, get_audio_duration, save_to_cache, detect_language_with_whisper
from models.langid_model import detect_language

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

ALLOWED_LANGUAGES = {
    "hi": "Hindi",
    "kn": "Kannada",
    "ta": "Tamil",
    "ml": "Malayalam",
    "mr": "Marathi",
    "pa": "Punjabi",
    "ur": "Urdu",
    "bn": "Bengali",
    "gu": "Gujarati",
    "te": "Telugu",
    "en": "English",
    # Additional common languages that Whisper might detect
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
    "ar": "Arabic",
    # Handle unknown language detection
    "unknown": "Unknown"
}

@router.post("/detect/live-audio")
async def detect_live_audio(file: UploadFile = File(...)):
    tmp_path = None
    try:
        # Save uploaded file to a temporary .wav file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Detect language
        detected_lang_code = detect_language_with_whisper(tmp_path)
        logger.info(f"Detected language code: {detected_lang_code}")
        
        if detected_lang_code in ALLOWED_LANGUAGES:
            logger.info(f"Language supported: {ALLOWED_LANGUAGES[detected_lang_code]}")
            return JSONResponse({"language": detected_lang_code, "language_name": ALLOWED_LANGUAGES[detected_lang_code]})
        elif detected_lang_code == "unknown":
            logger.warning("Language detection failed - audio may be unclear or too short")
            return JSONResponse({"error": "Audio is unclear or too short for language detection. Please try with clearer audio."}, status_code=400)
        else:
            logger.warning(f"Unsupported language detected: {detected_lang_code}")
            return JSONResponse({"error": f"Language not supported. Detected: {detected_lang_code}"}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

