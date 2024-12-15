"""Text analysis agent implementation."""

from typing import Any, Dict, List, Optional

import openai
from pydantic import BaseModel

from ai_analytics.agents.base import BaseAgent
from ai_analytics.config import Settings


class TextAnalysisRequest(BaseModel):
    """Request model for text analysis."""
    
    text: str
    tasks: List[str]
    language: Optional[str] = "en"


class TextAnalysisAgent(BaseAgent):
    """Agent for performing text analysis tasks."""

    def _validate_settings(self) -> None:
        """Validate required settings for text analysis."""
        if not self.settings.openai_api_key:
            raise ValueError("OpenAI API key is required")

    def _initialize_client(self) -> None:
        """Initialize OpenAI client."""
        openai.api_key = self.settings.openai_api_key
        if self.settings.azure_openai_endpoint:
            openai.api_base = self.settings.azure_openai_endpoint
            openai.api_type = "azure"

    async def _process(self, input_data: TextAnalysisRequest) -> Dict[str, Any]:
        """Process text analysis request.
        
        Args:
            input_data: TextAnalysisRequest containing text and analysis parameters.
            
        Returns:
            Dict containing analysis results.
        """
        system_prompt = self._build_system_prompt(input_data.tasks)
        
        response = await openai.ChatCompletion.acreate(
            model=self.settings.openai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_data.text}
            ],
            temperature=0.3,
        )
        
        return {
            "analysis": response.choices[0].message.content,
            "tasks": input_data.tasks,
            "language": input_data.language,
        }

    def _build_system_prompt(self, tasks: List[str]) -> str:
        """Build system prompt based on requested tasks.
        
        Args:
            tasks: List of analysis tasks to perform.
            
        Returns:
            Formatted system prompt string.
        """
        task_descriptions = {
            "sentiment": "Analyze the sentiment of the text",
            "keywords": "Extract key topics and keywords",
            "summary": "Provide a concise summary",
            "entities": "Identify named entities",
            "language": "Detect the language if not specified",
        }
        
        selected_tasks = [
            task_descriptions.get(task, f"Perform {task} analysis")
            for task in tasks
        ]
        
        return (
            "You are an advanced text analysis system. "
            f"Please perform the following tasks:\n"
            f"- {'\n- '.join(selected_tasks)}\n\n"
            "Provide the results in a clear, structured format."
        )