"""Configuration management for the memory agent."""
import os
from dataclasses import dataclass, field, fields
from typing import Any, Optional

from langchain_core.runnables import RunnableConfig
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass(kw_only=True)
class Configuration:
    """The configurable fields for the chatbot."""
    user_id: str = "default-user"
    todo_category: str = "general" 
    task_asis_role: str = "You are a helpful task management assistant. You help you create, organize, and manage the user's ToDo list."

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        return cls(**{k: v for k, v in values.items() if v})

# Environment-based configuration
class AppConfig:
    """Application configuration loaded from environment variables."""
    
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "gemini-2.0-flash-lite")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.user_id = os.getenv("USER_ID", "default-user")
        self.todo_category = os.getenv("TODO_CATEGORY", "general")
        
        # Validate required environment variables
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")

# Global configuration instance
app_config = AppConfig()
