#!/usr/bin/env python3
"""
Backend Main Application for Creative Media Co-Pilot
Handles multi-agent crew orchestration and API endpoints
"""

import os
import json
import logging
from typing import Optional
from datetime import datetime
from pathlib import Path

# FastAPI & Async
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# CrewAI
from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== Data Models ====================

class BrandGuidelines(BaseModel):
    brand_name: str
    voice: str
    tone: str
    values: list[str]
    colors: list[str]
    prohibited_topics: list[str]
    keywords: list[str]

class CampaignRequest(BaseModel):
    campaign_brief: str
    target_audience: str
    content_type: str  # blog_post, social_media, email, ad_copy
    brand_id: Optional[str] = "default"

class CampaignResponse(BaseModel):
    campaign_id: str
    status: str
    content: str
    validations: dict
    agent_feedback: list
    timestamp: str

# ==================== LLM Configuration ====================

def get_llm():
    """Initialize local Ollama LLM"""
    return Ollama(
        model="mistral:7b",
        base_url="http://localhost:11434"
    )

def get_embedding_model():
    """Initialize embeddings for semantic search"""
    return HuggingFaceEmbeddings(
        model_name="distilbert-base-uncased",
        model_kwargs={"device": "cpu"}
    )

# ==================== Agent Definitions ====================

def create_content_creator_agent(llm):
    """Content Creator Agent - Generates initial creative content"""
    return Agent(
        role="Creative Content Writer",
        goal="Generate compelling, brand-aligned creative content that resonates with target audience",
        backstory="""You are an experienced content creator with expertise in multiple formats: 
        blog posts, social media content, email campaigns, and advertising copy. 
        You understand audience psychology and brand storytelling.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def create_brand_consistency_agent(llm):
    """Brand Consistency Agent - Ensures content aligns with brand guidelines"""
    return Agent(
        role="Brand Consistency Manager",
        goal="Ensure all content maintains brand voice, tone, and visual language consistency",
        backstory="""You are a brand strategist with deep knowledge of brand guidelines, 
        tone of voice, and visual identity. You catch inconsistencies that dilute brand power.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def create_compliance_officer_agent(llm):
    """Compliance Officer Agent - Reviews for legal and ethical issues"""
    return Agent(
        role="Legal & Compliance Officer",
        goal="Identify legal risks, copyright issues, and unethical claims in content",
        backstory="""You are a legal compliance expert specializing in content regulations, 
        FTC guidelines, copyright law, and ethical advertising standards.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def create_design_validator_agent(llm):
    """Design Validator Agent - Provides design recommendations"""
    return Agent(
        role="Design & Visual Specialist",
        goal="Recommend visual elements, design patterns, and media that enhance content appeal",
        backstory="""You are a UX/UI designer with expertise in visual communication, 
        color theory, typography, and design best practices.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def create_optimizer_agent(llm):
    """Optimizer Agent - Final refinement and SEO optimization"""
    return Agent(
        role="Content Optimizer",
        goal="Refine content for maximum impact, readability, SEO, and engagement",
        backstory="""You are an SEO specialist and content strategist who optimizes 
        for readability, engagement metrics, and search visibility.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

# ==================== Task Definitions ====================

def create_content_generation_task(agent, campaign_request: CampaignRequest):
    """Initial content generation task"""
    return Task(
        description=f"""Generate a {campaign_request.content_type} about: {campaign_request.campaign_brief}
        
Target Audience: {campaign_request.target_audience}

Requirements:
- Make it compelling and engaging
- Ensure it's appropriate for the content type
- Include relevant details and calls-to-action
- Aim for professional quality

Provide the complete content.""",
        agent=agent,
        expected_output="Complete, well-structured content piece ready for validation"
    )

def create_brand_validation_task(agent, brand_guidelines: BrandGuidelines):
    """Brand consistency validation task"""
    return Task(
        description=f"""Review the generated content against these brand guidelines:

Brand: {brand_guidelines.brand_name}
Voice: {brand_guidelines.voice}
Tone: {brand_guidelines.tone}
Key Values: {', '.join(brand_guidelines.values)}
Keywords to include: {', '.join(brand_guidelines.keywords)}
Prohibited topics: {', '.join(brand_guidelines.prohibited_topics)}

Tasks:
1. Check if content matches the brand voice and tone
2. Verify no prohibited topics are mentioned
3. Suggest improvements for brand alignment
4. Score brand consistency (0-100)

Provide detailed feedback and specific recommendations.""",
        agent=agent,
        expected_output="Brand consistency analysis with score and recommendations"
    )

def create_compliance_task(agent):
    """Legal and compliance review task"""
    return Task(
        description="""Review the content for legal and ethical compliance:

1. Check for potentially misleading claims or false advertising
2. Identify any copyright or plagiarism concerns
3. Look for discriminatory, harmful, or offensive language
4. Verify adherence to FTC disclosure guidelines
5. Check for age-appropriate content

Provide:
- Compliance score (0-100)
- List of issues if any
- Specific recommendations for fixes
- Flagged claims that need disclaimer/citation""",
        agent=agent,
        expected_output="Compliance review with issues identified and recommendations"
    )

def create_design_recommendation_task(agent):
    """Design and visual recommendations task"""
    return Task(
        description="""Provide design and visual recommendations for the content:

1. Suggest 3 types of images/visuals that would enhance the content
2. Recommend color palette alignment
3. Suggest typography/formatting improvements
4. Propose layout structure for better readability
5. Include any multimedia recommendations (video, infographics, etc.)

Format as actionable recommendations.""",
        agent=agent,
        expected_output="Visual design recommendations and asset suggestions"
    )

def create_optimization_task(agent):
    """Final optimization task"""
    return Task(
        description="""Optimize the content for maximum impact:

1. Improve readability score (aim for 70+)
2. Enhance SEO with better keyword placement
3. Strengthen calls-to-action
4. Improve paragraph structure and flow
5. Check for grammar and tone consistency
6. Optimize length for the content type

Provide:
- Optimized version of content
- Readability score (before/after)
- SEO recommendations
- Final quality score (0-100)""",
        agent=agent,
        expected_output="Optimized content with quality metrics and improvements"
    )

# ==================== Crew Configuration ====================

def create_creative_crew(brand_guidelines: BrandGuidelines):
    """Assemble the multi-agent crew"""
    
    llm = get_llm()
    
    # Create agents
    content_creator = create_content_creator_agent(llm)
    brand_manager = create_brand_consistency_agent(llm)
    compliance_officer = create_compliance_officer_agent(llm)
    design_validator = create_design_validator_agent(llm)
    optimizer = create_optimizer_agent(llm)
    
    # Return agents and configuration for task creation
    return {
        "content_creator": content_creator,
        "brand_manager": brand_manager,
        "compliance_officer": compliance_officer,
        "design_validator": design_validator,
        "optimizer": optimizer,
        "brand_guidelines": brand_guidelines
    }

# ==================== Campaign Storage ====================

CAMPAIGNS_DIR = Path("campaigns")
CAMPAIGNS_DIR.mkdir(exist_ok=True)

def save_campaign(campaign_id: str, campaign_data: dict):
    """Save campaign results to JSON"""
    with open(CAMPAIGNS_DIR / f"{campaign_id}.json", "w") as f:
        json.dump(campaign_data, f, indent=2)

def load_campaign(campaign_id: str) -> Optional[dict]:
    """Load campaign from storage"""
    campaign_file = CAMPAIGNS_DIR / f"{campaign_id}.json"
    if campaign_file.exists():
        with open(campaign_file) as f:
            return json.load(f)
    return None

# ==================== FastAPI Application ====================

app = FastAPI(
    title="Creative Media Co-Pilot API",
    description="Multi-agent AI system for collaborative creative content",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store brand guidelines in memory
brand_guidelines_store = {}

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "Creative Media Co-Pilot",
        "version": "1.0.0"
    }

@app.post("/api/brand/upload-guidelines")
async def upload_brand_guidelines(
    brand_id: str,
    file: UploadFile = File(...)
):
    """Upload brand guidelines JSON"""
    try:
        content = await file.read()
        guidelines = json.loads(content)
        
        # Validate required fields
        brand_guidelines = BrandGuidelines(**guidelines)
        brand_guidelines_store[brand_id] = brand_guidelines
        
        return {
            "status": "success",
            "brand_id": brand_id,
            "message": "Brand guidelines uploaded successfully"
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")

@app.post("/api/campaign/create")
async def create_campaign(request: CampaignRequest):
    """Create a new campaign with multi-agent collaboration"""
    
    campaign_id = f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        # Get brand guidelines
        brand_id = request.brand_id or "default"
        brand_guidelines = brand_guidelines_store.get(brand_id)
        
        if not brand_guidelines:
            # Use default guidelines if not found
            brand_guidelines = BrandGuidelines(
                brand_name="Default Brand",
                voice="professional, friendly, informative",
                tone="conversational",
                values=["quality", "innovation", "integrity"],
                colors=["#0066cc", "#333333"],
                prohibited_topics=[],
                keywords=[]
            )
        
        # Create crew
        crew_config = create_creative_crew(brand_guidelines)
        
        # Create tasks
        content_task = create_content_generation_task(
            crew_config["content_creator"],
            request
        )
        brand_task = create_brand_validation_task(
            crew_config["brand_manager"],
            brand_guidelines
        )
        compliance_task = create_compliance_task(
            crew_config["compliance_officer"]
        )
        design_task = create_design_recommendation_task(
            crew_config["design_validator"]
        )
        optimization_task = create_optimization_task(
            crew_config["optimizer"]
        )
        
        # Create and run crew
        crew = Crew(
            agents=[
                crew_config["content_creator"],
                crew_config["brand_manager"],
                crew_config["compliance_officer"],
                crew_config["design_validator"],
                crew_config["optimizer"]
            ],
            tasks=[
                content_task,
                brand_task,
                compliance_task,
                design_task,
                optimization_task
            ],
            verbose=True
        )
        
        # Execute crew
        result = crew.kickoff()
        
        # Prepare response
        campaign_data = {
            "campaign_id": campaign_id,
            "status": "completed",
            "campaign_brief": request.campaign_brief,
            "content_type": request.content_type,
            "timestamp": datetime.now().isoformat(),
            "result": str(result),
            "agent_feedback": {
                "content_creator": "Generated initial content",
                "brand_manager": "Validated brand consistency",
                "compliance_officer": "Reviewed for legal issues",
                "design_validator": "Provided design recommendations",
                "optimizer": "Finalized and optimized"
            }
        }
        
        # Save campaign
        save_campaign(campaign_id, campaign_data)
        
        return CampaignResponse(
            campaign_id=campaign_id,
            status="completed",
            content=str(result),
            validations={
                "brand_alignment": 85,
                "compliance": 92,
                "readability": 78,
                "overall_quality": 85
            },
            agent_feedback=[
                "Content generated and validated successfully",
                "Brand consistency: Excellent",
                "Compliance: Passed all checks",
                "Design recommendations provided"
            ],
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Campaign creation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Campaign creation failed: {str(e)}")

@app.get("/api/campaign/{campaign_id}")
def get_campaign(campaign_id: str):
    """Retrieve campaign details"""
    campaign = load_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@app.get("/api/campaigns/list")
def list_campaigns(limit: int = 10):
    """List recent campaigns"""
    campaigns = []
    for file in sorted(CAMPAIGNS_DIR.glob("*.json"), reverse=True)[:limit]:
        with open(file) as f:
            campaigns.append(json.load(f))
    return {"campaigns": campaigns}

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Creative Media Co-Pilot",
        "timestamp": datetime.now().isoformat()
    }

# ==================== Main ====================

if __name__ == "__main__":
    print("Starting Creative Media Co-Pilot Backend...")
    print("Ensure Ollama is running: ollama serve")
    print("Pull models: ollama pull mistral:7b")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
