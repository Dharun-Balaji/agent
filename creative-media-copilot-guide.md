# Creative Media Co-Pilot: Complete Project Guide

## Project Overview

The **Creative Media Co-Pilot** is a multi-agent AI system that automates collaborative creative content generation. It features specialized AI agents that work together like a creative team to produce, review, and validate content while maintaining brand consistency, legal compliance, and ethical standards.

---

## Architecture & Agents

### 1. **Content Creator Agent**
- Role: Generates initial creative content (blog posts, social media captions, ad copy)
- Uses: Mistral 7B or Llama 2 for content generation
- Specialization: Brand-aware writing with style consistency

### 2. **Design Validator Agent**
- Role: Ensures visual consistency with brand guidelines
- Validates color schemes, typography, imagery recommendations
- Provides design feedback and alternative suggestions

### 3. **Compliance Officer Agent**
- Role: Reviews for legal, ethical, and copyright issues
- Checks for plagiarism indicators, legal compliance
- Flags potentially harmful or discriminatory content

### 4. **Brand Consistency Agent**
- Role: Ensures all content aligns with brand voice and guidelines
- Maintains tone, messaging, and visual language
- Cross-validates with brand documentation

### 5. **Optimizer Agent**
- Role: Refines and optimizes final content
- Improves SEO, readability, engagement metrics
- Ensures coherence across all agent validations

---

## Technology Stack

### Backend
- **Framework**: Python 3.9+
- **Multi-Agent Framework**: CrewAI
- **LLM Integration**: Ollama (local) + HuggingFace API (free)
- **Models**: 
  - Mistral 7B (text generation)
  - Llama 2 7B (reasoning)
  - DistilBERT (embeddings)

### Frontend
- **Web UI**: Streamlit (simple deployment) or React (advanced)
- **Real-time Updates**: WebSocket support
- **File Upload**: Support for brand guidelines, style sheets

### Deployment
- **Free Hosting**: HuggingFace Spaces, Replit, or Render
- **Local Option**: Docker containerization

---

## Project Structure

```
creative-media-copilot/
├── backend/
│   ├── agents/
│   │   ├── content_creator.py
│   │   ├── design_validator.py
│   │   ├── compliance_officer.py
│   │   ├── brand_consistency.py
│   │   └── optimizer.py
│   ├── models/
│   │   ├── llm_config.py
│   │   ├── embeddings.py
│   │   └── model_loader.py
│   ├── crew_config.py
│   ├── memory.py
│   └── main.py
├── frontend/
│   ├── streamlit_app.py
│   ├── pages/
│   │   ├── 01_dashboard.py
│   │   ├── 02_campaign_creator.py
│   │   ├── 03_brand_settings.py
│   │   └── 04_analytics.py
│   └── utils.py
├── data/
│   ├── sample_brand_guidelines.json
│   ├── compliance_rules.json
│   └── style_guides.json
├── requirements.txt
├── setup.sh
├── docker-compose.yml
├── README.md
└── DEPLOYMENT.md
```

---

## Installation & Setup

### Option 1: Local Setup with Ollama

```bash
# 1. Clone repository
git clone https://github.com/yourusername/creative-media-copilot.git
cd creative-media-copilot

# 2. Install Ollama
# Visit: https://ollama.ai

# 3. Pull models
ollama pull mistral:7b
ollama pull llama2:7b

# 4. Install Python dependencies
pip install -r requirements.txt

# 5. Set environment variables
export OLLAMA_BASE_URL="http://localhost:11434"
export HF_TOKEN="your_huggingface_token"

# 6. Run backend
python backend/main.py

# 7. Run frontend (in another terminal)
streamlit run frontend/streamlit_app.py
```

### Option 2: Docker Deployment

```bash
docker-compose up --build
```

### Option 3: Free Cloud Hosting (HuggingFace Spaces)

1. Fork this repository
2. Create a new Space on HuggingFace
3. Connect your GitHub repo
4. Deploy with one click
5. Set environment secrets for API keys

---

## Key Features

### 1. **Multi-Agent Collaboration**
- Agents communicate through CrewAI task framework
- Memory persistence for context awareness
- Role-based specialization and expertise

### 2. **Content Generation Pipeline**
- Input: Campaign brief, brand guidelines, target audience
- Processing: 5-agent collaborative workflow
- Output: Validated, optimized, branded content

### 3. **Real-time Validation**
- Agents provide feedback at each stage
- Transparency: Users see agent interactions
- Refinement loop until brand standards met

### 4. **Brand Consistency Engine**
- Upload brand guidelines (PDF/JSON)
- Extract brand voice, tone, colors, fonts
- Validate all content against guidelines

### 5. **Analytics Dashboard**
- Content performance metrics
- Agent decision transparency
- Workflow efficiency tracking

---

## API Endpoints

```
POST /api/campaign/create
  - Input: campaign_brief, brand_id, content_type
  - Output: generated_content, validation_scores, agent_feedback

GET /api/campaign/{campaign_id}
  - Returns: full campaign details, agent validations

POST /api/brand/upload-guidelines
  - Upload brand guidelines file

GET /api/analytics/performance
  - Returns: workflow metrics, success rates

WebSocket /ws/campaign/{campaign_id}
  - Real-time agent collaboration updates
```

---

## Usage Example

```python
from backend.crew_config import create_creative_crew

# Initialize crew with brand context
crew = create_creative_crew(
    brand_guidelines="brand_voice.json",
    compliance_rules="legal_rules.json"
)

# Run campaign creation
result = crew.kickoff(
    inputs={
        "campaign_brief": "Launch new eco-friendly product line",
        "target_audience": "Millennials, eco-conscious consumers",
        "content_types": ["blog_post", "social_media", "email"]
    }
)

print(result)
```

---

## Agent Communication Example

```
User Input: "Create a blog post about sustainable living"
    ↓
[Content Creator Agent]
→ Generates: 800-word blog post on sustainable living
    ↓
[Brand Consistency Agent]
→ Validates: Tone matches brand voice ✓
→ Feedback: Add more personal anecdotes
    ↓
[Compliance Officer Agent]
→ Checks: No copyright issues ✓
→ Flags: Add sustainability sources
    ↓
[Design Validator Agent]
→ Suggests: 3 image recommendations
→ Metadata: SEO keywords for header images
    ↓
[Optimizer Agent]
→ Final Pass: Improves readability score from 65→85
→ Output: Production-ready content
```

---

## Deployment Instructions

### Deploy to HuggingFace Spaces (Recommended - FREE)

1. **Create Account**: https://huggingface.co
2. **Create Space**:
   - Click "New Space"
   - Choose "Streamlit" as SDK
   - Set visibility to "Public"
3. **Connect Repository**:
   - Link your GitHub repo
   - Add secrets (HF_TOKEN, API keys)
4. **Done**: Space auto-deploys on push

### Deploy to Render (Alternative - FREE tier)

1. Create Render account
2. Create new "Web Service"
3. Connect GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `streamlit run frontend/streamlit_app.py`

### Deploy to Replit (Quick Start)

1. Import GitHub repo to Replit
2. Add secrets to `.replit` file
3. Click "Run" to start

---

## Model Selection & Rationale

| Model | Purpose | Size | Speed | Accuracy |
|-------|---------|------|-------|----------|
| Mistral 7B | Content Generation | 14GB RAM | Fast | High |
| Llama 2 7B | Reasoning & Planning | 14GB RAM | Medium | High |
| DistilBERT | Embeddings & Similarity | 1GB RAM | Very Fast | Good |
| mT5 Small | Summarization | 2GB RAM | Fast | Good |

**Free Options**:
- Run locally with Ollama
- Use HuggingFace Inference API (free tier: 30 calls/minute)
- Use Replicate API (free tier available)

---

## Configuration Files

### brand_guidelines.json
```json
{
  "brand_name": "EcoLife",
  "voice": "friendly, informative, inspiring",
  "tone": "conversational, accessible",
  "values": ["sustainability", "innovation", "community"],
  "colors": ["#2ecc71", "#27ae60", "#f39c12"],
  "fonts": ["Inter", "Georgia"],
  "prohibited_topics": ["political", "religious"],
  "keywords": ["eco-friendly", "sustainable", "green"]
}
```

### compliance_rules.json
```json
{
  "copyright_check": true,
  "plagiarism_threshold": 0.15,
  "required_disclaimers": ["affiliate", "sponsored"],
  "prohibited_claims": ["cure", "guarantee"],
  "age_rating": "general_audience"
}
```

---

## Performance Metrics

### Expected Outcomes
- **Content Quality**: 85-95% brand consistency
- **Processing Time**: 2-5 minutes per campaign
- **Error Detection**: 92% accuracy
- **Rework Reduction**: From 45% to 12%

### Monitoring
- Agent decision logs
- Validation success rates
- User feedback scores
- Content performance tracking

---

## Troubleshooting

### Issue: Models loading slowly
**Solution**: Pre-download models with `ollama pull` before running

### Issue: Memory errors
**Solution**: Use quantized models (Q4, Q5) or cloud inference APIs

### Issue: Frontend not connecting to backend
**Solution**: Check CORS settings, ensure backend port exposed

### Issue: HuggingFace Space timeout
**Solution**: Use lightweight Streamlit, cache agent responses

---

## Future Enhancements

1. **Fine-tuning**: Custom models trained on brand content
2. **Multimedia Support**: Image generation with Stable Diffusion
3. **A/B Testing**: Auto-generate content variants
4. **Scheduling**: Auto-publish to social media platforms
5. **Team Collaboration**: Multi-user editing and comments
6. **Feedback Loop**: Continuous model improvement

---

## Open-Source Models Used

- Mistral 7B: https://huggingface.co/mistralai/Mistral-7B
- Llama 2: https://huggingface.co/meta-llama/Llama-2-7b
- DistilBERT: https://huggingface.co/distilbert-base-uncased
- mT5: https://huggingface.co/google/mt5-small

---

## License

MIT License - Feel free to use, modify, and deploy

## Contact & Support

GitHub: https://github.com/yourusername/creative-media-copilot
Email: support@creativecopilot.ai

---

*Build smarter, faster, better creative campaigns with AI agents working together like your ideal creative team.*
