import os
import json
import hashlib
from pathlib import Path
from typing import Optional
from fastapi import HTTPException
from pydub import AudioSegment
from google.cloud import storage
import whisper

UPLOAD_DIR = "static/uploads"
CACHE_DIR = "static/cache"
GCS_BUCKET_NAME = "language_buckets"

# Lazy initialization of Google Cloud Storage client
_storage_client = None
_bucket = None

def get_storage_client():
    global _storage_client
    if _storage_client is None:
        _storage_client = storage.Client()
    return _storage_client

def get_bucket():
    global _bucket
    if _bucket is None:
        _bucket = get_storage_client().bucket(GCS_BUCKET_NAME)
    return _bucket

# === Helpers ===
def get_file_hash(content: bytes) -> str:
    return hashlib.md5(content).hexdigest()

def check_cache(file_hash: str) -> Optional[dict]:
    cache_file = Path(CACHE_DIR) / f"{file_hash}.json"
    if cache_file.exists():
        with open(cache_file, "r") as f:
            return json.load(f)
    return None

def save_to_cache(file_hash: str, result: dict):
    cache_file = Path(CACHE_DIR) / f"{file_hash}.json"
    with open(cache_file, "w") as f:
        json.dump(result, f)

def preprocess_audio(input_path: str, output_path: str):
    audio = AudioSegment.from_file(input_path)
    if audio.dBFS < -45:
        raise HTTPException(400, detail="Audio too silent to transcribe.")
    audio = audio.set_channels(1).set_frame_rate(16000).normalize().high_pass_filter(50)
    audio.export(output_path, format="wav")

def get_audio_duration(audio_path: str) -> float:
    return len(AudioSegment.from_file(audio_path))

def upload_to_gcs(file_path: str, destination_blob_name: str) -> str:
    try:
        bucket = get_bucket()
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(file_path)
        return f"gs://{GCS_BUCKET_NAME}/{destination_blob_name}"
    except Exception as e:
        print(f"Warning: Google Cloud Storage upload failed: {e}")
        return f"local://{file_path}"

def detect_language_with_whisper(audio_path: str) -> str:
    model = whisper.load_model("base")
    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    probs_dict = probs[0] if isinstance(probs, list) and len(probs) > 0 else {}
    lang_code = max(probs_dict, key=lambda k: probs_dict[k]) if probs_dict else "unknown"
    return lang_code 