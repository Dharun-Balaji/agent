#!/bin/bash

# Setup script for Creative Media Co-Pilot

echo "🚀 Creative Media Co-Pilot Setup"
echo "================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python3 --version || { echo "❌ Python 3 not found. Please install Python 3.9+"; exit 1; }

# Create virtual environment
echo "✓ Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "✓ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "✓ Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "✓ Creating project directories..."
mkdir -p campaigns
mkdir -p data
mkdir -p logs

# Create sample brand guidelines
echo "✓ Creating sample data..."
cat > data/sample_brand_guidelines.json << 'EOF'
{
  "brand_name": "EcoLife",
  "voice": "friendly, informative, inspiring",
  "tone": "conversational, accessible",
  "values": ["sustainability", "innovation", "community"],
  "colors": ["#2ecc71", "#27ae60", "#f39c12"],
  "prohibited_topics": ["political", "religious"],
  "keywords": ["eco-friendly", "sustainable", "green"]
}
EOF

# Create environment file
echo "✓ Creating environment configuration..."
cat > .env << 'EOF'
OLLAMA_BASE_URL=http://localhost:11434
API_PORT=8000
API_HOST=0.0.0.0
LOG_LEVEL=INFO
EOF

echo ""
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Install Ollama from https://ollama.ai"
echo "2. Pull models:"
echo "   ollama pull mistral:7b"
echo "   ollama pull llama2:7b"
echo "3. Start Ollama:"
echo "   ollama serve"
echo "4. In a new terminal, run the backend:"
echo "   source venv/bin/activate"
echo "   python backend_main.py"
echo "5. In another terminal, run the frontend:"
echo "   source venv/bin/activate"
echo "   streamlit run frontend_app.py"
echo ""
echo "Visit http://localhost:8501 to access the UI"
echo ""
