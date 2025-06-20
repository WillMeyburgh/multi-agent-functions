from typing import Annotated, List, Sequence, TypedDict
from operator import add as add_messages
from langchain_core.messages import BaseMessage

from multi_agent_functions.google.tasks.model.tasklist import TaskList


class GoogleTasksAgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    tasklists: Annotated[List[TaskList], "Store all remote tasklist information"]
