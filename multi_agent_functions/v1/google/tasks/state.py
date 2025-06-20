from typing import Annotated, List, Sequence, TypedDict, Optional
from operator import add as add_messages
from langchain_core.messages import BaseMessage

from multi_agent_functions.v1.google.tasks.model.tasklist import TaskList
from multi_agent_functions.v1.google.tasks.model.task import Task


class GoogleTasksAgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    tasklists: Annotated[List[TaskList], "Store all remote tasklist information"]
