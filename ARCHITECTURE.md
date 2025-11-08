# 🏗️ System Architecture & Workflow

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                        │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  Dashboard   │  │   Campaign   │  │    Brand     │           │
│  │              │  │   Creator    │  │  Settings    │           │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤           │
│  │ • Status     │  │ • Input Form │  │ • Upload     │           │
│  │ • Metrics    │  │ • Progress   │  │   Guidelines │           │
│  │ • History    │  │ • Results    │  │ • Multiple   │           │
│  │ • API Health │  │ • Download   │  │   Brands     │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│                                                                   │
│                    STREAMLIT FRONTEND (Port 8501)               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API LAYER (FastAPI)                        │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ /api/campaign/create      - Create new campaign           │ │
│  │ /api/brand/upload         - Upload brand guidelines       │ │
│  │ /api/campaign/{id}        - Get campaign details          │ │
│  │ /api/campaigns/list       - List recent campaigns         │ │
│  │ /api/health               - Health check                  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│              FASTAPI (Port 8000) - Error Handling               │
│              CORS Enabled - Request Validation                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MULTI-AGENT ORCHESTRATION                    │
│                      (CrewAI Framework)                         │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  CREW CONFIGURATION                      │  │
│  │                                                           │  │
│  │  • Agent 1: Content Creator          ────┐              │  │
│  │  • Agent 2: Brand Manager            ────┤              │  │
│  │  • Agent 3: Compliance Officer       ────├─► Task Queue │  │
│  │  • Agent 4: Design Validator         ────┤              │  │
│  │  • Agent 5: Optimizer                ────┘              │  │
│  │                                                           │  │
│  │  Memory: ✓ Shared Context                               │  │
│  │  Tools: ✓ LLM Access, Validation Tools                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │ Mistral  │    │ Llama 2  │    │DistilBERT│
        │  7B      │    │   7B     │    │           │
        └──────────┘    └──────────┘    └──────────┘
              │               │               │
              └───────────────┼───────────────┘
                              │
                              ▼
                      ┌──────────────────┐
                      │  Ollama Service  │
                      │  (Port 11434)    │
                      │                  │
                      │ Model Management │
                      │ Inference Engine │
                      └──────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
        ┌──────────────┐            ┌──────────────┐
        │  Local GPU   │            │  Local CPU   │
        │  (Optional)  │            │  (Fallback)  │
        └──────────────┘            └──────────────┘
```

---

## Agent Workflow Sequence

```
User Input: "Create blog post about sustainable living"
    │
    ▼
┌─────────────────────────────────────────┐
│  AGENT 1: CONTENT CREATOR               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Input:  Campaign brief, target audience│
│  Output: Initial content (800 words)    │
│  Score:  Initial quality ✓              │
└─────────────────────────────────────────┘
    │
    ▼ (Handoff + Feedback)
┌─────────────────────────────────────────┐
│  AGENT 2: BRAND CONSISTENCY MANAGER     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Input:  Content + Brand Guidelines    │
│  Check:  Voice, Tone, Keywords         │
│  Output: Validation score + Feedback   │
│  Action: Request revisions if needed   │
│  Score:  Brand alignment ✓             │
└─────────────────────────────────────────┘
    │
    ▼ (Handoff + Feedback)
┌─────────────────────────────────────────┐
│  AGENT 3: COMPLIANCE OFFICER            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Input:  Content + Compliance Rules    │
│  Check:  Plagiarism, Legal Issues      │
│  Check:  Ethical Compliance            │
│  Output: Pass/Fail + Issues            │
│  Action: Flag problems if found        │
│  Score:  Compliance ✓                  │
└─────────────────────────────────────────┘
    │\n    ▼ (Handoff + Feedback)
┌─────────────────────────────────────────┐
│  AGENT 4: DESIGN VALIDATOR              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Input:  Content + Visual Guidelines   │
│  Output: Design recommendations:       │
│         • 3 image types suggested      │
│         • Color palette info           │
│         • Typography tips              │
│         • Layout suggestions           │
│  Score:  Visual appeal ✓               │
└─────────────────────────────────────────┘
    │
    ▼ (Handoff + Feedback)
┌─────────────────────────────────────────┐
│  AGENT 5: OPTIMIZER                     │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  Input:  All feedback + Content        │
│  Actions:                               │
│         • Improve readability          │
│         • Enhance SEO                  │
│         • Strengthen CTAs              │
│         • Fix flagged issues           │
│  Output: Final optimized content       │
│  Scores: Readability, SEO, Quality     │
│  Status: ✓ PRODUCTION READY            │
└─────────────────────────────────────────┘
    │
    ▼
RESULT: Production-ready content with:
   ✓ Validation scores (each agent)
   ✓ Agent feedback (transparency)
   ✓ Ready to publish
   ✓ Downloadable (Text/JSON)
```

---

## Data Flow Architecture

```
┌──────────────┐
│  User Input  │
│              │
│ • Brief      │
│ • Audience   │
│ • Type       │
│ • Brand      │
└──────┬───────┘
       │
       ▼
    FastAPI
   Request
    Handler
       │
       ├─────────────────────────────────┐
       │                                 │
       ▼                                 ▼
  ┌─────────────┐              ┌──────────────────┐
  │ Validate    │              │ Load Brand       │
  │ Input       │              │ Guidelines       │
  └─────┬───────┘              └────────┬─────────┘
        │                               │
        └───────────┬───────────────────┘
                    │
                    ▼
            ┌───────────────┐
            │ Create Crew   │
            │ with Agents   │
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────────┐
            │  Execute Tasks    │
            │  in Sequence      │
            │                   │
            │  1. Generate      │
            │  2. Validate      │
            │  3. Comply        │
            │  4. Design        │
            │  5. Optimize      │
            └───────┬───────────┘
                    │
                    ▼
        ┌─────────────────────┐
        │ Collect Results:    │
        │                     │
        │ • Final Content     │
        │ • Validation Scores │
        │ • Agent Feedback    │
        │ • Metadata          │
        └────────┬────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │ Store Campaign:     │
        │                     │
        │ • JSON File         │
        │ • Database (future) │
        └────────┬────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │ Return Response     │
        │                     │
        │ • Campaign ID       │
        │ • Content           │
        │ • Scores            │
        │ • Feedback          │
        └────────┬────────────┘
                 │
                 ▼
           ┌──────────────┐
           │ Display in   │
           │ Streamlit UI │
           └──────────────┘
```

---

## Deployment Architecture Options

### Option 1: Cloud (HuggingFace Spaces)
```
User Browser
    │
    ▼ HTTPS
HuggingFace Spaces
    │
    ├─ Frontend (Streamlit)
    │    │
    │    └─ Connect to Backend
    │
    └─ Backend (FastAPI)
         │
         └─ Ollama (via API)
             │
             └─ Models (Cached)
```

### Option 2: Local Docker
```
Docker Network (copilot-network)
    │
    ├─ Frontend Container (Streamlit)
    │   Port: 8501
    │   
    ├─ Backend Container (FastAPI)
    │   Port: 8000
    │   
    └─ Ollama Container
        Port: 11434
        
Host System
    │
    ├─ Campaigns Volume (Persistent)
    ├─ Data Volume (Persistent)
    └─ Ollama Volume (Model Cache)
```

### Option 3: Local Python
```
Terminal 1: Ollama
    │
    └─ ollama serve (Port 11434)

Terminal 2: Backend
    │
    └─ python backend_main.py (Port 8000)

Terminal 3: Frontend
    │
    └─ streamlit run frontend_app.py (Port 8501)

Local System
    │
    ├─ Python venv
    ├─ Campaigns/ (Local storage)
    └─ Logs/ (Local logs)
```

---

## Data Models

### Campaign Request
```
{
  campaign_brief: string,
  target_audience: string,
  content_type: "blog_post" | "social_media" | "email" | "ad_copy",
  brand_id: string (optional)
}
```

### Campaign Response
```
{
  campaign_id: string,
  status: "completed" | "processing" | "failed",
  content: string,
  validations: {
    brand_alignment: number (0-100),
    compliance: number (0-100),
    readability: number (0-100),
    overall_quality: number (0-100)
  },
  agent_feedback: [
    "feedback1",
    "feedback2",
    ...
  ],
  timestamp: ISO8601 string
}
```

### Brand Guidelines
```
{
  brand_name: string,
  voice: string,
  tone: string,
  values: string[],
  colors: string[] (hex codes),
  prohibited_topics: string[],
  keywords: string[]
}
```

---

## Error Handling & Logging

```
Request
   │
   ├─ Invalid Input? ──► HTTP 400 (Bad Request)
   │
   ├─ API Error? ──────► HTTP 500 (Server Error)
   │
   ├─ Model Error? ────► HTTP 500 + Retry
   │
   └─ Logging:
       │
       ├─ INFO: Request received
       ├─ INFO: Agent starting
       ├─ DEBUG: Agent output
       ├─ ERROR: Exception details
       └─ SUCCESS: Campaign complete
```

---

## Scaling Paths

### Phase 1: Current (MVP)
- Single instance backend
- JSON file storage
- Ollama local

### Phase 2: Growth
- Load balancing (2-3 backend instances)
- PostgreSQL database
- Redis caching
- Model serving cluster

### Phase 3: Enterprise
- Kubernetes orchestration
- Distributed training
- Advanced monitoring
- Custom model fine-tuning
- Multi-region deployment

---

## Security Architecture

```
External Request
    │
    ▼
CORS Validation ✓
    │
    ▼
Input Validation ✓
    │
    ▼
Rate Limiting (optional) ✓
    │
    ▼
Authentication (future)
    │
    ▼
Authorization Checks
    │
    ▼
Process Request
    │
    ▼
Log Activity
    │
    ▼
Return Response
```

---

## Performance Optimization

### Caching
```
@st.cache_resource
def get_llm():
    """Cache LLM instance"""
    return Ollama(...)

@st.cache_data
def load_guidelines():
    """Cache brand guidelines"""
    return load_json(...)
```

### Model Loading
```
Models loaded once:
   • Mistral 7B (14GB)
   • Llama 2 7B (14GB)
   • DistilBERT (1GB)
   
Total RAM: 16GB recommended
(works with 8GB, slower)
```

### Request Handling
```
Frontend Request
    │
    ├─ Check Cache ──► Return if cached
    │
    ├─ Execute Agents (parallel where possible)
    │
    ├─ Collect Results
    │
    └─ Cache Result
         │
         └─ Return to Frontend
```

---

**This architecture is production-ready and scales from MVP to enterprise!**
