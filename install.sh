#!/bin/bash

# Backend Installation Script
# This script automates the installation of all required dependencies

set -e  # Exit on any error

echo "🚀 Starting Backend Installation..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    print_status "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        print_success "Python $PYTHON_VERSION found"
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
        print_success "Python $PYTHON_VERSION found"
        PYTHON_CMD="python"
    else
        print_error "Python is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    print_status "Checking pip installation..."
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        PIP_CMD="pip"
    else
        print_error "pip is not installed. Please install pip."
        exit 1
    fi
    print_success "pip found"
}

# Create virtual environment
create_venv() {
    print_status "Creating virtual environment..."
    if [ ! -d "venv" ]; then
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
}

# Activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        source venv/Scripts/activate
    else
        # Unix/Linux/macOS
        source venv/bin/activate
    fi
    print_success "Virtual environment activated"
}

# Install system dependencies
install_system_deps() {
    print_status "Installing system dependencies..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            # Ubuntu/Debian
            print_status "Installing Ubuntu/Debian dependencies..."
            sudo apt-get update
            sudo apt-get install -y ffmpeg libsndfile1 libportaudio2 portaudio19-dev python3-dev build-essential
        elif command -v yum &> /dev/null; then
            # CentOS/RHEL
            print_status "Installing CentOS/RHEL dependencies..."
            sudo yum install -y ffmpeg libsndfile portaudio-devel python3-devel gcc
        elif command -v dnf &> /dev/null; then
            # Fedora
            print_status "Installing Fedora dependencies..."
            sudo dnf install -y ffmpeg libsndfile portaudio-devel python3-devel gcc
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        print_status "Installing macOS dependencies..."
        if command -v brew &> /dev/null; then
            brew install ffmpeg portaudio
        else
            print_warning "Homebrew not found. Please install Homebrew first: https://brew.sh/"
            print_warning "Then run: brew install ffmpeg portaudio"
        fi
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        print_warning "On Windows, please install FFmpeg manually:"
        print_warning "1. Download from: https://ffmpeg.org/download.html"
        print_warning "2. Add to your system PATH"
    fi
}

# Install Python dependencies
install_python_deps() {
    print_status "Installing Python dependencies..."
    
    # Upgrade pip
    $PIP_CMD install --upgrade pip
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        $PIP_CMD install -r requirements.txt
        print_success "Python dependencies installed"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Test installation
test_installation() {
    print_status "Testing installation..."
    
    # Test basic imports
    python -c "
import sys
print('Python version:', sys.version)

try:
    import fastapi
    print('✓ FastAPI installed')
except ImportError as e:
    print('✗ FastAPI not installed:', e)

try:
    import uvicorn
    print('✓ Uvicorn installed')
except ImportError as e:
    print('✗ Uvicorn not installed:', e)

try:
    import pydub
    print('✓ Pydub installed')
except ImportError as e:
    print('✗ Pydub not installed:', e)

try:
    import librosa
    print('✓ Librosa installed')
except ImportError as e:
    print('✗ Librosa not installed:', e)

try:
    import torch
    print('✓ PyTorch installed')
except ImportError as e:
    print('✗ PyTorch not installed:', e)

try:
    import whisper
    print('✓ Whisper installed')
except ImportError as e:
    print('✗ Whisper not installed:', e)

try:
    import google.cloud.speech
    print('✓ Google Cloud Speech installed')
except ImportError as e:
    print('✗ Google Cloud Speech not installed:', e)

try:
    import googletrans
    print('✓ Googletrans installed')
except ImportError as e:
    print('✗ Googletrans not installed:', e)

print('\\nInstallation test completed!')
"
}

# Setup environment file
setup_env() {
    print_status "Setting up environment configuration..."
    
    if [ ! -f ".env" ]; then
        if [ -f "env.example" ]; then
            cp env.example .env
            print_success "Created .env file from template"
            print_warning "Please edit .env file with your actual credentials"
        else
            print_warning "No env.example found. Please create .env file manually"
        fi
    else
        print_warning ".env file already exists"
    fi
}

# Main installation process
main() {
    echo "🎯 Audio Captioning API - Backend Installation"
    echo "=============================================="
    
    check_python
    check_pip
    create_venv
    activate_venv
    install_system_deps
    install_python_deps
    test_installation
    setup_env
    
    echo ""
    echo "🎉 Installation completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Edit .env file with your Google Cloud credentials"
    echo "2. Run the server: uvicorn main:app --reload"
    echo "3. Visit: http://localhost:8000/docs for API documentation"
    echo ""
    echo "For more information, see README_INSTALLATION.md"
}

# Run main function
main "$@"
