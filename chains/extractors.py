"""Trustcall extractors for the memory agent."""
from langchain_google_genai import ChatGoogleGenerativeAI
from trustcall import create_extractor
from schemas.profile import Profile
from schemas.todo import ToDo
from config import app_config

def initialize_model():
    """Initialize the language model."""
    return ChatGoogleGenerativeAI(model=app_config.model_name)

def create_profile_extractor(model):
    """Create the profile extractor."""
    return create_extractor(
        model,
        tools=[Profile],
        tool_choice="Profile",
    )

def create_todo_extractor(model, tool_name="ToDo"):
    """Create the todo extractor."""
    return create_extractor(
        model,
        tools=[ToDo],
        tool_choice=tool_name,
        enable_inserts=True
    )
