"""Tests for the TextAnalysisAgent."""

import pytest
from unittest.mock import AsyncMock, patch

from ai_analytics import TextAnalysisAgent
from ai_analytics.agents.text_analysis import TextAnalysisRequest
from ai_analytics.config import Settings


@pytest.fixture
def settings():
    """Create test settings."""
    return Settings(
        openai_api_key="test-key",
        openai_model="gpt-4",
        enable_monitoring=False,
    )


@pytest.fixture
def text_agent(settings):
    """Create TextAnalysisAgent instance."""
    return TextAnalysisAgent(settings)


@pytest.mark.asyncio
async def test_text_analysis(text_agent):
    """Test text analysis execution."""
    mock_response = AsyncMock()
    mock_response.choices = [
        AsyncMock(message=AsyncMock(content="Test analysis result"))
    ]
    
    with patch("openai.ChatCompletion.acreate", return_value=mock_response):
        request = TextAnalysisRequest(
            text="Test text",
            tasks=["sentiment", "summary"]
        )
        
        result = await text_agent.execute(request)
        
        assert "analysis" in result
        assert result["analysis"] == "Test analysis result"
        assert "tasks" in result
        assert len(result["tasks"]) == 2


def test_invalid_settings():
    """Test agent initialization with invalid settings."""
    with pytest.raises(ValueError):
        TextAnalysisAgent(Settings(openai_api_key=""))