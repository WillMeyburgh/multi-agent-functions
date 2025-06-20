from typing import List, Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from multi_agent_functions.v1.google.calender.model.calender_list import CalendarListEntry
from multi_agent_functions.v1.google.tasks.model.tasklist import TaskList

class SupervisorState(TypedDict):
    """Represents the state of the supervisor."""
    messages: Annotated[List[BaseMessage], add_messages]
