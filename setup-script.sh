#!/bin/bash

# AI Vision Recipe Generator - Setup Script
# This script automates the setup process

set -e  # Exit on error

echo "🍽️  AI Vision Recipe Generator - Setup"
echo "========================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "❌ Python 3.8+ required. Found: $python_version"
    exit 1
fi
echo "✅ Python version: $python_version"
echo ""

# Create virtual environment
echo "🔧 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "ℹ️  Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip --quiet
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "📚 Installing dependencies..."
echo "   This may take several minutes..."
pip install -r requirements.txt --quiet
echo "✅ Dependencies installed"
echo ""

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p .streamlit
mkdir -p assets
mkdir -p tests
mkdir -p logs
echo "✅ Directories created"
echo ""

# Copy config file
echo "⚙️  Setting up Streamlit config..."
if [ ! -f ".streamlit/config.toml" ]; then
    cp streamlit-config.toml .streamlit/config.toml
    echo "✅ Streamlit config copied"
else
    echo "ℹ️  Streamlit config already exists"
fi
echo ""

# Check GPU availability
echo "🎮 Checking GPU availability..."
python3 -c "import torch; print('✅ CUDA available:', torch.cuda.is_available())"
if [ $? -eq 0 ]; then
    python3 -c "import torch; print('   GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"
fi
echo ""

# Download models (optional, will happen on first run)
echo "🤖 Models will be downloaded on first run"
echo "   Expected download size: ~2-3 GB"
echo ""

# Setup complete
echo "========================================"
echo "✅ Setup complete!"
echo ""
echo "🚀 To run the app:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Run app: streamlit run app.py"
echo ""
echo "📖 For more information, see README.md"
echo "========================================"