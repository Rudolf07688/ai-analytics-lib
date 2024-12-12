"""Example FastAPI application using AI Analytics Library."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ai_analytics import TextAnalysisAgent
from ai_analytics.agents.text_analysis import TextAnalysisRequest
from ai_analytics.config import Settings

app = FastAPI(title="AI Analytics API")

# Initialize settings and agent
settings = Settings()
text_agent = TextAnalysisAgent(settings)


@app.post("/analyze/text")
async def analyze_text(request: TextAnalysisRequest):
    """Analyze text using the TextAnalysisAgent.
    
    Args:
        request: TextAnalysisRequest containing text and analysis parameters.
        
    Returns:
        Analysis results from the agent.
    """
    try:
        result = await text_agent.execute(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint.
    
    Returns:
        Dict indicating service status.
    """
    return {"status": "healthy", "version": "0.1.0"}