from typing import List
from langchain_core.tools import create_schema_from_function, BaseTool, StructuredTool
from datetime import datetime

from multi_agent_functions.v1.google.tasks.client import GoogleTasksClient
from multi_agent_functions.v1.google.tasks.model.task import Task
from multi_agent_functions.v1.google.tasks.model.tasklist import TaskList
from multi_agent_functions.v1.google.tasks.state import GoogleTasksAgentState

class GoogleTasksToolkit:
    def __init__(self):
        self.client = GoogleTasksClient()

    def get_current_time(self) -> str:
        """
        Returns the current date and time with timezone information.
        """
        return datetime.now().astimezone().isoformat()

    def get_tools(self) -> List[BaseTool]:
        return list(map(
            StructuredTool.from_function,
            [
                self.get_current_time,
                Task.from_dict,
                TaskList.from_dict,
                Task.to_dict,
                TaskList.to_dict,
                self.client.tasklists_list,
                self.client.tasklists_delete,
                self.client.tasklists_get,
                self.client.tasklists_insert,
                self.client.tasklists_patch,
                self.client.tasklists_update,
                self.client.tasks_list,
                self.client.tasks_clear,
                self.client.tasks_delete,
                self.client.tasks_get,
                self.client.tasks_insert,
                self.client.tasks_patch,
                self.client.tasks_update,
            ]
        ))
