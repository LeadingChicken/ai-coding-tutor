from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    """Message model for chat history."""
    role: str
    content: str

class AgentAction(BaseModel):
    """Model for agent actions."""
    tool: str
    input: str
    thought: str

class AgentResponse(BaseModel):
    """Model for agent responses."""
    thoughts: List[str]
    actions: List[AgentAction]
    final_answer: str

class CodeRequest(BaseModel):
    """Model for code execution requests."""
    code: str
    unit_test: Optional[str] = None 