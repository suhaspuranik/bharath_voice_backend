# Load environment variables FIRST
from dotenv import load_dotenv
load_dotenv()

# Initialize Google Cloud credentials from environment variables BEFORE any other imports
from utils.credentials import create_google_credentials, check_credentials

try:
    check_credentials()
    create_google_credentials()
    print("✅ Google Cloud credentials initialized successfully")
except ValueError as e:
    print(f"⚠️  Warning: {e}")
    print("⚠️  Google Cloud features may not work without proper credentials.")

# Now import FastAPI and other modules
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.upload import router as upload_router
from api.live import router as live_router
from api.translate import router as translate_router
from api.caption import router as caption_router 

app = FastAPI(title="Audio Captioning with Whisper + Google STT")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(live_router)
app.include_router(translate_router)
app.include_router(caption_router)

@app.get("/health")
def health():
    return {"status": "ok"}
