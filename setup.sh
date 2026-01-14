#!/bin/bash

echo "================================================"
echo "Twitter to Slack Job Bot - Setup Script"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python $(python3 --version) detected"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy .env.template to .env:      cp .env.template .env"
echo "2. Edit .env with your credentials: nano .env"
echo "3. Test the bot:                    python twitter_to_slack_jobs.py"
echo ""
echo "For automation setup, see README.md"
echo "================================================"
