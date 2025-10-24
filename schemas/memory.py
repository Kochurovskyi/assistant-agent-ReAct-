"""Memory schema for the memory agent."""
from typing import Literal, TypedDict

class UpdateMemory(TypedDict):
    """Decision on what memory type to update."""
    update_type: Literal['user', 'todo', 'instructions']
