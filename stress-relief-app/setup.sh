#!/bin/bash

# Setup script for Stress Relief Companion App

echo "🧠 Setting up Stress Relief Companion App..."
echo ""

# Check Python version
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the app:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run: streamlit run app.py"
echo ""

