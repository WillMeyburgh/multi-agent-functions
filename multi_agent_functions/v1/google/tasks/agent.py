from typing import Optional, Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent

from multi_agent_functions.v1.google.tasks.state import GoogleTasksAgentState
from multi_agent_functions.v1.google.tasks.system_prompt import SYSTEM_PROMPT
from multi_agent_functions.v1.google.tasks.toolkit import GoogleTasksToolkit


class GoogleTasksAgent():
    @classmethod
    def init_state(cls, messages: Optional[Sequence[BaseMessage]] = None) -> GoogleTasksAgentState:
        return GoogleTasksAgentState(
            messages=messages or [], 
            tasklists=[]
        )
    
    def __init__(self):
        self.toolkit = GoogleTasksToolkit()
    
    def compile(self, model) -> CompiledStateGraph:
        return create_react_agent(
            model,
            tools=self.toolkit.get_tools(),
            prompt=SYSTEM_PROMPT,
            name='google_tasks'
        )
