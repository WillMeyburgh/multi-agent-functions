from typing import List, Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import StructuredTool
from multi_agent_functions.v1.google.calender.agent import GoogleCalendarAgent
from multi_agent_functions.v1.google.tasks.agent import GoogleTasksAgent
from multi_agent_functions.v1.supervisor.state import SupervisorState
from multi_agent_functions.v1.supervisor.system_prompt import SYSTEM_PROMPT # Import SupervisorState

class SupervisorAgent():
    def __init__(self):
        self.agents = {
            'google_tasks': GoogleTasksAgent(),
            'google_calender': GoogleCalendarAgent()
        }

    @classmethod
    def init_state(cls) -> SupervisorState:
        """Initializes the state for the supervisor."""
        return SupervisorState(messages=[])

    def compile(self, model):
        self.graphs = {
            name:agent.compile(model) 
            for name, agent in self.agents.items()
        }

        return create_react_agent(
            model,
            tools=[StructuredTool.from_function(self.delegate_to)],
            prompt=SYSTEM_PROMPT
        )
