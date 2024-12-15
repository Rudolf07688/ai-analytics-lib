"""Configuration management for AI Analytics Library."""

from typing import Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Global settings for AI Analytics Library."""
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4", env="OPENAI_MODEL")
    
    # Azure Configuration (optional)
    azure_openai_api_key: Optional[str] = Field(None, env="AZURE_OPENAI_API_KEY")
    azure_openai_endpoint: Optional[str] = Field(None, env="AZURE_OPENAI_ENDPOINT")
    
    # Agent Configuration
    agent_timeout: float = Field(30.0, env="AGENT_TIMEOUT")
    max_retries: int = Field(3, env="MAX_RETRIES")
    
    # Monitoring Configuration
    enable_monitoring: bool = Field(True, env="ENABLE_MONITORING")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = True