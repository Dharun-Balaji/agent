# ⚡ Quick Start Guide

Get Creative Media Co-Pilot running in 10 minutes!

---

## 🎯 Choose Your Path

### Path 1: Cloud (Easiest - 5 minutes)
Deploy to HuggingFace Spaces with **ZERO configuration**

### Path 2: Docker (Easy - 10 minutes)
Run locally with Docker Compose

### Path 3: Local (Full Control - 15 minutes)
Traditional Python setup

---

## ☁️ Path 1: HuggingFace Spaces (Recommended)

### Step 1: Create Account
```
1. Go to https://huggingface.co/join
2. Sign up (email or GitHub)
```

### Step 2: Fork Repository
```
1. Visit: https://github.com/yourusername/creative-media-copilot
2. Click Fork
```

### Step 3: Create Space
```
1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill:
   - Name: creative-media-copilot
   - SDK: Streamlit
   - Visibility: Public
4. Create
```

### Step 4: Connect & Deploy
```
1. Settings → Repository
2. Select your forked repo
3. Save
4. Done! Auto-deploys in 2-3 minutes
```

**Your app is live at:**
```
https://huggingface.co/spaces/YOUR_USERNAME/creative-media-copilot
```

---

## 🐳 Path 2: Docker (Production-Ready)

### Requirements
- Docker & Docker Compose installed
- 8GB RAM

### Setup (3 commands)

```bash
# 1. Clone
git clone https://github.com/yourusername/creative-media-copilot.git
cd creative-media-copilot

# 2. Build & Run
docker-compose up --build

# 3. Open browser
# Frontend: http://localhost:8501
# API: http://localhost:8000
```

**That's it!** Everything auto-configures.

### Useful Docker Commands
```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart
docker-compose restart
```

---

## 🐍 Path 3: Local Python Setup

### Requirements
- Python 3.9+
- 16GB RAM
- Ollama (https://ollama.ai)

### Step 1: Install Ollama
```
1. Download from https://ollama.ai
2. Install and run
3. In terminal:
   ollama pull mistral:7b
   ollama pull llama2:7b
```

### Step 2: Clone & Setup
```bash
git clone https://github.com/yourusername/creative-media-copilot.git
cd creative-media-copilot

chmod +x setup.sh
./setup.sh
```

### Step 3: Run Services

**Terminal 1 - Ollama:**
```bash
ollama serve
```

**Terminal 2 - Backend:**
```bash
source venv/bin/activate
python backend_main.py
```

**Terminal 3 - Frontend:**
```bash
source venv/bin/activate
streamlit run frontend_app.py
```

### Step 4: Access
```
Frontend: http://localhost:8501
API: http://localhost:8000
```

---

## 🎨 First Campaign - Try It!

### Create Your First Campaign

1. **Open Web UI**
   - Go to http://localhost:8501 (local)
   - Or your HuggingFace Spaces URL

2. **Navigate to "Create Campaign"**

3. **Fill in details:**
   - Campaign Brief: "Write a blog post about AI and creativity"
   - Target Audience: "Tech enthusiasts and content creators"
   - Content Type: "blog_post"
   - Brand: "default"

4. **Click "Generate Content"**

5. **Watch Agents Collaborate:**
   - 🤖 Content Creator → Generates content
   - 🤖 Brand Manager → Validates brand fit
   - 🤖 Compliance Officer → Checks legal issues
   - 🤖 Design Validator → Recommends visuals
   - 🤖 Optimizer → Finalizes content

6. **Review Results:**
   - See generated content
   - Check validation scores
   - Download as Text or JSON

---

## 📊 Upload Brand Guidelines

Make content generation even better!

### Step 1: Create Brand JSON

Create `my_brand.json`:
```json
{
  "brand_name": "My Brand",
  "voice": "friendly, professional",
  "tone": "conversational",
  "values": ["innovation", "quality"],
  "colors": ["#0066cc", "#ff6600"],
  "prohibited_topics": ["politics"],
  "keywords": ["quality", "innovation"]
}
```

### Step 2: Upload

1. Go to "Brand Settings" tab
2. Upload your JSON file
3. Create campaigns with your brand
4. Content now respects your guidelines!

---

## ✅ Verify Everything Works

### Test Backend API
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Creative Media Co-Pilot"
}
```

### Test Campaign Creation
```bash
curl -X POST http://localhost:8000/api/campaign/create \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_brief": "Test campaign",
    "target_audience": "Everyone",
    "content_type": "social_media",
    "brand_id": "default"
  }'
```

### Check Logs
```bash
# Docker
docker-compose logs backend

# Local
# Check console output in terminals
```

---

## 🆘 Quick Troubleshooting

### "Connection refused"
```bash
# Ensure backend is running
# Check: http://localhost:8000/api/health

# If local: Start python backend_main.py
# If Docker: Check docker-compose is up
```

### "No module named X"
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or with Docker:
docker-compose build --no-cache
```

### "Out of memory"
```bash
# Use lighter model
ollama pull mistral:7b-q4

# Or increase RAM
# Docker: docker-compose.yml → memory limit
```

### "Ollama connection error"
```bash
# Ensure Ollama is running
ollama serve

# Pull models
ollama pull mistral:7b
```

### Frontend shows "API: Disconnected"
```bash
# Backend must be running on port 8000
python backend_main.py

# Or with Docker
docker-compose up
```

---

## 📈 Next Steps

### 1. **Customize**
   - Upload your brand guidelines
   - Create multiple brand profiles
   - Fine-tune for your niche

### 2. **Integrate**
   - Connect to your CMS
   - Add to CI/CD pipeline
   - Build custom workflows

### 3. **Scale**
   - Deploy to production
   - Add database for history
   - Set up monitoring

### 4. **Extend**
   - Add more agents
   - Integrate image generation
   - Auto-publish to social media

---

## 🔗 Useful Links

- **GitHub**: https://github.com/yourusername/creative-media-copilot
- **CrewAI**: https://docs.crewai.com
- **Streamlit**: https://docs.streamlit.io
- **Ollama**: https://ollama.ai

---

## 💡 Pro Tips

### Tip 1: Use .streamlit/config.toml
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

### Tip 2: Add Custom CSS
```python
st.markdown("""
<style>
/* Your custom styles */
</style>
""", unsafe_allow_html=True)
```

### Tip 3: Cache Long Operations
```python
@st.cache_resource
def get_llm():
    return Ollama(model="mistral:7b")
```

### Tip 4: Use Secrets
```python
api_key = st.secrets.get("API_KEY")
```

---

## 🎓 Learning Path

1. ✅ Run locally or in cloud
2. ✅ Create your first campaign
3. ✅ Upload brand guidelines
4. ✅ Explore analytics
5. ✅ Read documentation
6. ✅ Extend with custom agents
7. ✅ Deploy to production

---

## 🚀 Deploy to Production

Once you're comfortable, deploy for real:

### Option A: HuggingFace Spaces (Free)
- No setup needed
- Auto-scales
- Always free

### Option B: Render (Free tier)
- 750 hours/month free
- Simple configuration
- Easy monitoring

### Option C: Your Own Server
- Full control
- Custom domain
- More expensive

See DEPLOYMENT.md for full production setup.

---

## 📞 Need Help?

- **Issues**: GitHub Issues
- **Docs**: README.md & DEPLOYMENT.md
- **Community**: Discussions

---

**Start creating! 🎨**

Your first campaign is just 3 minutes away.
