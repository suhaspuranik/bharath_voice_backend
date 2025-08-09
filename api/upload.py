from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, Any
import os
import shutil
from pathlib import Path
from api.utils import UPLOAD_DIR
from models.langid_model import detect_language

router = APIRouter()

@router.post("/detect-language/")
async def detect_language_api(file: UploadFile = File(...)) -> Dict[str, Any]:
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")
    file_path = str(Path(UPLOAD_DIR) / file.filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run detection - now returns both language and confidence
    language, confidence = detect_language(file_path)

    return {
        "language": language,
        "confidence": confidence,
        "confidence_percentage": f"{confidence * 100:.2f}%"
    } 