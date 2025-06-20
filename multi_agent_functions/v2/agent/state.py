from typing import List, Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """Represents the state of the supervisor."""
    messages: Annotated[List[BaseMessage], add_messages]
