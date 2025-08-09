# Backend Installation Guide

This guide explains how to install all required dependencies for the Audio Captioning API backend.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd my_app/backend
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

## Package Details

### Core Web Framework
- **fastapi**: Modern web framework for building APIs
- **uvicorn[standard]**: ASGI server for running FastAPI applications
- **pydantic**: Data validation using Python type annotations

### Environment & Configuration
- **python-dotenv**: Load environment variables from .env files

### Audio Processing
- **pydub**: Audio file manipulation and processing
- **librosa**: Audio and music signal processing
- **numpy**: Numerical computing library

### Machine Learning
- **torch**: PyTorch deep learning framework
- **openai-whisper**: Speech recognition and transcription

### Google Cloud Services
- **google-cloud-speech**: Google Cloud Speech-to-Text API
- **google-cloud-storage**: Google Cloud Storage API

### Translation
- **googletrans==4.0.0rc1**: Google Translate API wrapper

### File Processing
- **python-multipart**: Handle file uploads in FastAPI

### CORS Support
- **fastapi-cors**: Cross-Origin Resource Sharing support

### Utilities
- **typing-extensions**: Extended typing support for older Python versions

## System Dependencies

### Audio Processing Dependencies

Some audio processing libraries require system-level dependencies:

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y \
    ffmpeg \
    libsndfile1 \
    libportaudio2 \
    portaudio19-dev \
    python3-dev \
    build-essential
```

#### macOS:
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install audio dependencies
brew install ffmpeg portaudio
```

#### Windows:
- Install FFmpeg from: https://ffmpeg.org/download.html
- Add FFmpeg to your system PATH

### PyTorch Installation

PyTorch installation might vary based on your system:

#### CPU Only:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

#### CUDA Support (NVIDIA GPU):
```bash
# For CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## Verification

### 1. Check Installation

```bash
# Verify Python version
python --version

# Verify pip installation
pip list

# Test imports
python -c "
import fastapi
import uvicorn
import pydub
import librosa
import torch
import whisper
import google.cloud.speech
import google.cloud.storage
import googletrans
print('All packages installed successfully!')
"
```

### 2. Test Audio Processing

```bash
# Test audio processing capabilities
python -c "
from pydub import AudioSegment
import librosa
print('Audio processing libraries working!')
"
```

## Troubleshooting

### Common Issues

1. **FFmpeg not found:**
   ```bash
   # Install FFmpeg
   # Ubuntu/Debian:
   sudo apt-get install ffmpeg
   
   # macOS:
   brew install ffmpeg
   
   # Windows: Download from https://ffmpeg.org/download.html
   ```

2. **PortAudio issues:**
   ```bash
   # Ubuntu/Debian:
   sudo apt-get install portaudio19-dev
   
   # macOS:
   brew install portaudio
   ```

3. **PyTorch installation fails:**
   ```bash
   # Try CPU-only version
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
   ```

4. **Google Cloud authentication:**
   ```bash
   # Install Google Cloud CLI
   # Follow: https://cloud.google.com/sdk/docs/install
   
   # Authenticate
   gcloud auth application-default login
   ```

5. **Memory issues with large models:**
   ```bash
   # Use smaller Whisper model
   # In your code, use: whisper.load_model("tiny") or whisper.load_model("base")
   ```

### Performance Optimization

1. **Use smaller models for development:**
   ```python
   # Instead of "large" model, use:
   model = whisper.load_model("base")  # Faster, less memory
   ```

2. **Enable GPU acceleration (if available):**
   ```python
   import torch
   device = "cuda" if torch.cuda.is_available() else "cpu"
   ```

3. **Optimize audio processing:**
   ```python
   # Use lower sample rates for faster processing
   audio, sr = librosa.load(file_path, sr=16000)  # 16kHz instead of default
   ```

## Development Setup

### 1. Install Development Dependencies

```bash
pip install -r requirements-dev.txt  # If you have development requirements
```

### 2. Set up Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

### 3. Run Tests

```bash
# Install pytest
pip install pytest pytest-asyncio

# Run tests
pytest
```

## Production Deployment

### 1. Use Production Server

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 2. Environment Variables

Create a `.env` file with production settings:

```env
# Production settings
ENVIRONMENT=production
DEBUG=false
HOST=0.0.0.0
PORT=8000

# Google Cloud credentials
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
```

### 3. Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Security Considerations

1. **Keep dependencies updated:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Use virtual environments:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Always activate before installing packages
   ```

3. **Secure Google Cloud credentials:**
   - Never commit credentials to version control
   - Use environment variables for sensitive data
   - Rotate credentials regularly

4. **Enable HTTPS in production:**
   ```bash
   # Use reverse proxy (nginx) with SSL certificates
   # Or use FastAPI with SSL directly
   ```

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all system dependencies are installed
3. Ensure you're using the correct Python version
4. Check the official documentation for each package
5. Create an issue in the repository with detailed error messages
