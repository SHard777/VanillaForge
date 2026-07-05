from pydantic import BaseModel, Field


class ConversationTurn(BaseModel):
    """Represents a single conversational turn in history."""

    role: str  # "user" or "model"
    content: str  # The actual message text


class WorkflowState(BaseModel):
    """
    Shared workflow state for VanillaForge_agent.
    Contains the conversation history, turn counter, and variables
    for tracking current query, response, and classification.
    """

    history: list[ConversationTurn] = Field(default_factory=list)
    turn_count: int = 0
    current_query: str = ""
    last_response: str = ""
    selected_skill: str = ""
