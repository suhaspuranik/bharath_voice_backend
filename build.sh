#!/bin/bash
# Build script for Render deployment

echo "🚀 Starting build process..."

# Install system dependencies for audio processing
echo "📦 Installing system dependencies..."
apt-get update
apt-get install -y ffmpeg libsndfile1 libportaudio2 portaudio19-dev python3-dev build-essential

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Build completed successfully!"
