"""Base agent implementation for AI Analytics Library."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from tenacity import retry, stop_after_attempt, wait_exponential

from ai_analytics.config import Settings
from ai_analytics.utils.logging import get_logger


class BaseAgent(ABC):
    """Base class for all AI agents in the library."""

    def __init__(self, settings: Settings):
        """Initialize the base agent.
        
        Args:
            settings: Configuration settings for the agent.
        """
        self.settings = settings
        self.logger = get_logger(self.__class__.__name__)
        self._setup()

    def _setup(self) -> None:
        """Set up the agent with necessary configurations."""
        self.logger.info(f"Initializing {self.__class__.__name__}")
        self._validate_settings()
        self._initialize_client()

    @abstractmethod
    def _validate_settings(self) -> None:
        """Validate that all required settings are present."""
        pass

    @abstractmethod
    def _initialize_client(self) -> None:
        """Initialize any necessary clients or connections."""
        pass

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def execute(self, input_data: Any) -> Dict[str, Any]:
        """Execute the agent's main functionality.
        
        Args:
            input_data: The input data for the agent to process.
            
        Returns:
            Dict containing the results of the agent's execution.
        """
        try:
            self.logger.info(f"Executing {self.__class__.__name__}")
            result = await self._process(input_data)
            self.logger.info(f"Execution completed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Error during execution: {str(e)}")
            raise

    @abstractmethod
    async def _process(self, input_data: Any) -> Dict[str, Any]:
        """Process the input data and return results.
        
        Args:
            input_data: The input data to process.
            
        Returns:
            Dict containing the processing results.
        """
        pass

    def get_metadata(self) -> Dict[str, Any]:
        """Get agent metadata.
        
        Returns:
            Dict containing agent metadata.
        """
        return {
            "agent_type": self.__class__.__name__,
            "settings": self.settings.dict(exclude={"openai_api_key", "azure_openai_api_key"}),
        }