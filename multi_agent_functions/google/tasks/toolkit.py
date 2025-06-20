from typing import List
from langchain_core.tools import create_schema_from_function, BaseTool, StructuredTool

from multi_agent_functions.google.tasks.client import GoogleTasksClient
from multi_agent_functions.google.tasks.model.task import Task
from multi_agent_functions.google.tasks.model.tasklist import TaskList
from multi_agent_functions.google.tasks.state import GoogleTasksAgentState

class GoogleTasksToolkit:
    def __init__(self):
        self.client = GoogleTasksClient()

    def tasklists_list(self, state: GoogleTasksAgentState) -> GoogleTasksAgentState:
        """
        Lists all available task lists and updates the agent's state with the retrieved task lists.

        Args:
            state (GoogleTasksAgentState): The current state of the agent, which includes
                                           a list of task lists to be updated.

        Returns:
            GoogleTasksAgentState: The updated state of the agent with the 'tasklists' field populated.
        """
        state['tasklists'] = self.client.tasklists_list()
        return state

    def get_tools(self) -> List[BaseTool]:
        return list(map(
            StructuredTool.from_function,
            [
                Task.from_dict,
                TaskList.from_dict,
                Task.to_dict,
                TaskList.to_dict,
                self.tasklists_list,
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