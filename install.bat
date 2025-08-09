@echo off
REM Backend Installation Script for Windows
REM This script automates the installation of all required dependencies

echo 🚀 Starting Backend Installation...

REM Check if Python is installed
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [SUCCESS] Python found

REM Check if pip is installed
echo [INFO] Checking pip installation...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip is not installed. Please install pip.
    pause
    exit /b 1
)
echo [SUCCESS] pip found

REM Create virtual environment
echo [INFO] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo [SUCCESS] Virtual environment created
) else (
    echo [WARNING] Virtual environment already exists
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
echo [SUCCESS] Virtual environment activated

REM Install Python dependencies
echo [INFO] Installing Python dependencies...
pip install --upgrade pip
if exist "requirements.txt" (
    pip install -r requirements.txt
    echo [SUCCESS] Python dependencies installed
) else (
    echo [ERROR] requirements.txt not found
    pause
    exit /b 1
)

REM Test installation
echo [INFO] Testing installation...
python -c "import sys; print('Python version:', sys.version)"
python -c "import fastapi; print('✓ FastAPI installed')" 2>nul || echo "✗ FastAPI not installed"
python -c "import uvicorn; print('✓ Uvicorn installed')" 2>nul || echo "✗ Uvicorn not installed"
python -c "import pydub; print('✓ Pydub installed')" 2>nul || echo "✗ Pydub not installed"
python -c "import librosa; print('✓ Librosa installed')" 2>nul || echo "✗ Librosa not installed"
python -c "import torch; print('✓ PyTorch installed')" 2>nul || echo "✗ PyTorch not installed"
python -c "import whisper; print('✓ Whisper installed')" 2>nul || echo "✗ Whisper not installed"
python -c "import google.cloud.speech; print('✓ Google Cloud Speech installed')" 2>nul || echo "✗ Google Cloud Speech not installed"
python -c "import googletrans; print('✓ Googletrans installed')" 2>nul || echo "✗ Googletrans not installed"

REM Setup environment file
echo [INFO] Setting up environment configuration...
if not exist ".env" (
    if exist "env.example" (
        copy env.example .env >nul
        echo [SUCCESS] Created .env file from template
        echo [WARNING] Please edit .env file with your actual credentials
    ) else (
        echo [WARNING] No env.example found. Please create .env file manually
    )
) else (
    echo [WARNING] .env file already exists
)

echo.
echo 🎉 Installation completed successfully!
echo.
echo Next steps:
echo 1. Install FFmpeg manually from: https://ffmpeg.org/download.html
echo 2. Add FFmpeg to your system PATH
echo 3. Edit .env file with your Google Cloud credentials
echo 4. Run the server: uvicorn main:app --reload
echo 5. Visit: http://localhost:8000/docs for API documentation
echo.
echo For more information, see README_INSTALLATION.md
pause
