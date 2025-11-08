# 🚀 Deployment Guide: Creative Media Co-Pilot

Complete guide for deploying the Creative Media Co-Pilot to various platforms.

---

## Table of Contents

1. [Local Development](#local-development)
2. [HuggingFace Spaces (Recommended - FREE)](#huggingface-spaces)
3. [Render (FREE)](#render)
4. [Replit (Quick Start)](#replit)
5. [AWS](#aws)
6. [Production Checklist](#production-checklist)

---

## Local Development

### Prerequisites
- Python 3.9+
- 16GB RAM
- Git

### Setup Steps

```bash
# 1. Clone repository
git clone https://github.com/yourusername/creative-media-copilot.git
cd creative-media-copilot

# 2. Run setup
chmod +x setup.sh
./setup.sh

# 3. Install Ollama (https://ollama.ai)
# Then pull models
ollama pull mistral:7b
ollama pull llama2:7b

# 4. Terminal 1: Start Ollama
ollama serve

# 5. Terminal 2: Start Backend
source venv/bin/activate
python backend_main.py

# 6. Terminal 3: Start Frontend
source venv/bin/activate
streamlit run frontend_app.py
```

**Access:**
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000

---

## HuggingFace Spaces (Recommended - FREE)

**Why HuggingFace Spaces?**
- ✅ Completely FREE (no credit card needed)
- ✅ Auto-deploys from GitHub
- ✅ Free GPU access (optional)
- ✅ Easy environment management
- ✅ Perfect for demos and portfolios

### Step-by-Step

#### 1. Create HuggingFace Account
```
Visit: https://huggingface.co/join
Sign up with email or GitHub
```

#### 2. Fork Repository
```
https://github.com/yourusername/creative-media-copilot
Click "Fork" button
```

#### 3. Create New Space
```
1. Visit https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in:
   - Space name: "creative-media-copilot"
   - License: MIT
   - SDK: Streamlit
   - Visibility: Public (for portfolio)
4. Click "Create space"
```

#### 4. Connect GitHub Repository
```
1. In Space Settings → Repository
2. Select "Connect a Git repository"
3. Choose your forked repo
4. Select "Persistent Dockerfile-based spaces"
5. Save
```

#### 5. Create Dockerfile for Space

Create `Dockerfile` in your repo:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY frontend_app.py .
COPY data/ ./data/

RUN mkdir -p campaigns logs

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8501 || exit 1

CMD ["streamlit", "run", "frontend_app.py", \
     "--server.port=8501", "--server.address=0.0.0.0"]
```

#### 6. Add Secrets (Optional - For API Integration)
```
1. Space Settings → Repository secrets
2. Add:
   - HF_TOKEN: your_huggingface_token
   - API_BASE_URL: your_api_endpoint
```

#### 7. Deploy
```
Push code to GitHub:
git add .
git commit -m "Deploy to HuggingFace Spaces"
git push origin main

HuggingFace auto-deploys!
```

**Result:**
- Live URL: `https://huggingface.co/spaces/yourusername/creative-media-copilot`
- Auto-deploys on every push
- Free hosting with no credit card

---

## Render (Alternative - FREE)

**Why Render?**
- ✅ Free tier: 750 hours/month
- ✅ Auto-deploys from GitHub
- ✅ Simple configuration
- ✅ Good for small-medium projects

### Step-by-Step

#### 1. Create Render Account
```
Visit: https://render.com
Sign up with GitHub
```

#### 2. Deploy Backend

```
1. New → Web Service
2. Connect GitHub repository
3. Configuration:
   - Name: creative-copilot-backend
   - Runtime: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: python backend_main.py
   - Plan: Free
4. Create Web Service
```

**Environment Variables** (in Render dashboard):
```
OLLAMA_BASE_URL=http://localhost:11434
API_HOST=0.0.0.0
API_PORT=8000
```

#### 3. Deploy Frontend

```
1. New → Web Service
2. Connect same repository
3. Configuration:
   - Name: creative-copilot-frontend
   - Runtime: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: streamlit run frontend_app.py --server.port=8501
   - Plan: Free
4. Create Web Service
```

**Environment Variables**:
```
API_BASE_URL=https://creative-copilot-backend.onrender.com
STREAMLIT_SERVER_PORT=8501
```

#### 4. Access
- Frontend: `https://creative-copilot-frontend.onrender.com`
- Backend API: `https://creative-copilot-backend.onrender.com`

---

## Replit (Quick Start - FREE)

**Why Replit?**
- ✅ Instant setup (3 minutes)
- ✅ In-browser development
- ✅ Great for learning
- ✅ Built-in terminal

### Step-by-Step

```
1. Visit https://replit.com
2. Click "New Repl"
3. Import from GitHub:
   https://github.com/yourusername/creative-media-copilot
4. Language: Python
5. Click "Import from GitHub"
6. Add to .replit:
```

```toml
run = "streamlit run frontend_app.py"

[env]
OLLAMA_BASE_URL = "http://localhost:11434"
API_BASE_URL = "http://localhost:8000"
```

```
7. Click Run
8. Access at replit.dev URL
```

---

## AWS (Production Grade)

**Architecture:**
```
Route 53 (DNS)
    ↓
CloudFront (CDN)
    ↓
Application Load Balancer
    ↓
ECS Cluster
├── Backend Service (Fargate)
├── Frontend Service (Fargate)
└── Ollama Service (EC2)
    ↓
RDS PostgreSQL (Database)
ElastiCache Redis (Cache)
S3 (Storage)
```

### Step-by-Step

#### 1. ECR - Push Docker Image

```bash
# Create ECR repository
aws ecr create-repository --repository-name creative-copilot

# Login
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t creative-copilot:latest .
docker tag creative-copilot:latest ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/creative-copilot:latest
docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/creative-copilot:latest
```

#### 2. ECS - Deploy Container

```
1. Create ECS Cluster
2. Create Task Definition:
   - Image: ECR image URL
   - Memory: 4096
   - CPU: 2048
   - Environment variables: Add API config
3. Create Service:
   - Launch type: Fargate
   - Task definition: previous one
   - Desired count: 2 (for HA)
4. Configure Load Balancer: Application Load Balancer
```

#### 3. RDS - Database

```
1. Create RDS instance (PostgreSQL)
2. Enable automated backups
3. Create read replicas for HA
4. Update connection string in backend
```

#### 4. CloudFront - CDN

```
1. Create distribution
2. Origin: ALB endpoint
3. Enable caching
4. Enable HTTPS
```

---

## Production Checklist

### Security
- [ ] HTTPS/SSL enabled
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Input validation implemented
- [ ] No hardcoded secrets
- [ ] Environment variables for all config
- [ ] Database encryption enabled

### Performance
- [ ] Caching implemented (Redis)
- [ ] Database indexes created
- [ ] CDN enabled
- [ ] Models cached locally
- [ ] Async task processing setup

### Monitoring
- [ ] Error tracking (Sentry)
- [ ] Performance monitoring (DataDog)
- [ ] Uptime monitoring (UptimeRobot)
- [ ] Logs centralized (ELK)
- [ ] Alerts configured

### Reliability
- [ ] Database backups automated
- [ ] Disaster recovery plan
- [ ] Load balancing enabled
- [ ] Auto-scaling configured
- [ ] Health checks set up

### Code Quality
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documentation complete
- [ ] CI/CD pipeline working
- [ ] Version control organized

---

## Environment Variables Reference

### Backend
```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO

# LLM Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b

# Database (Production)
DATABASE_URL=postgresql://user:pass@host:5432/db

# Cache (Production)
REDIS_URL=redis://localhost:6379

# External Services
HF_TOKEN=your_huggingface_token
```

### Frontend
```env
# API Connection
API_BASE_URL=http://localhost:8000

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_CLIENT_TOOLBARPOSITION=top
```

---

## Scaling to 100K+ Users

### Architecture Improvements

1. **Database Sharding**
   - Partition campaigns by user_id
   - Separate read/write databases

2. **Model Serving**
   - Use vLLM for faster inference
   - Model quantization (Q4, Q5)
   - Distributed model serving

3. **Queue System**
   ```python
   # Celery + Redis setup
   from celery import Celery
   app = Celery('creative_copilot')
   app.config_from_object('celery_config.py')
   ```

4. **Caching Strategy**
   ```python
   # Cache frequently used responses
   @app.get("/api/campaigns/{campaign_id}")
   @cache(expire=3600)
   def get_campaign(campaign_id: str):
       # ...
   ```

---

## Troubleshooting Deployments

### HuggingFace Spaces Issue: "Space is sleeping"
**Solution:** Upgrade to paid plan or add GitHub Action to keep active

### Render Issue: Free tier timeout
**Solution:** Add Keep-alive ping every 5 minutes or upgrade plan

### AWS Issue: High costs
**Solution:** 
- Use spot instances
- Enable auto-scaling
- Set up spending alerts

### All Platforms Issue: Memory errors
**Solution:**
- Use quantized models (Q4)
- Increase allocated memory
- Use external model API

---

## Next Steps

1. Choose deployment platform
2. Follow specific setup guide
3. Test thoroughly
4. Monitor performance
5. Collect user feedback
6. Iterate and improve

---

**Happy deploying! 🚀**
