from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
import logging
from pathlib import Path
from api.utils import UPLOAD_DIR, get_file_hash, check_cache, preprocess_audio, get_audio_duration, save_to_cache, detect_language_with_whisper
from googletrans import Translator
import whisper
from google.cloud import speech_v1p1beta1 as speech

router = APIRouter()
translator = Translator()

MAX_INLINE_DURATION_MS = 60 * 1000  # 1 minute

async def process_short_audio(audio_path: str, file_hash: str, language: str):
    # Preprocess audio to ensure it's in the correct format for Google Speech-to-Text
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        try:
            preprocess_audio(audio_path, tmp_wav.name)
            processed_audio_path = tmp_wav.name
        except Exception as e:
            logging.warning(f"Audio preprocessing failed, using original: {e}")
            processed_audio_path = audio_path
    
    try:
        client = speech.SpeechClient()
        with open(processed_audio_path, "rb") as f:
            byte_data = f.read()

        audio = speech.RecognitionAudio(content=byte_data)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language if language != "unknown" else "en-US",
            enable_automatic_punctuation=True,
        )

        response = client.recognize(config=config, audio=audio)
        if not response.results:
            return {"caption": "", "language": language}
        full_text = " ".join([r.alternatives[0].transcript for r in response.results if r.alternatives]).strip()
        detected_lang = language
        return {
            "caption": full_text,
            "language": detected_lang
        }
    finally:
        # Clean up temporary file if it was created
        if processed_audio_path != audio_path and os.path.exists(processed_audio_path):
            os.remove(processed_audio_path)

async def process_long_audio(audio_path: str, file_hash: str, language: str):
    # For simplicity, use the same as short audio
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return {
        "caption": result["text"],
        "language": result.get("language", language)
    }

async def transcribe_audio_file(audio_path: str, file_ext: str):
    with open(audio_path, "rb") as f:
        contents = f.read()

    file_hash = get_file_hash(contents)

    if cached := check_cache(file_hash):
        cached["cached"] = True
        return cached

    detected_lang = detect_language_with_whisper(audio_path)
    print(f"[Whisper] Detected language: {detected_lang}")

    duration = get_audio_duration(audio_path)
    if duration > MAX_INLINE_DURATION_MS:
        result = await process_long_audio(audio_path, file_hash, detected_lang)
    else:
        result = await process_short_audio(audio_path, file_hash, detected_lang)

    return result if isinstance(result, dict) else result.body

@router.post("/translate/audio/")
async def translate_audio(tgt_lang: str, file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")
    
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ['.mp3', '.wav', '.m4a', '.flac']:
        raise HTTPException(status_code=400, detail=f"Unsupported file format: {file_ext}. Supported formats: mp3, wav, m4a, flac")
    
    tmp_path = f"temp_{file.filename}"
    try:
        with open(tmp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        transcript_result = await transcribe_audio_file(tmp_path, file_ext)
        original_text = str(transcript_result["caption"])
        detected_lang = transcript_result.get("language", "unknown")
        
        # Check if we have text to translate
        if not original_text.strip():
            return {
                "original_text": "",
                "translated_text": "",
                "language": detected_lang,
                "message": "No speech detected in audio"
            }
        
        translated_text = translator.translate(original_text, tgt_lang).text
        return {
            "original_text": original_text,
            "translated_text": translated_text,
            "language": detected_lang
        }
    except Exception as e:
        logging.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path) 