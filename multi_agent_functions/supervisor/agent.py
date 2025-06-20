from typing import List, Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph_supervisor import create_supervisor

from multi_agent_functions.google.calender.agent import GoogleCalendarAgent
from multi_agent_functions.google.tasks.agent import GoogleTasksAgent
from multi_agent_functions.supervisor.state import SupervisorState
from multi_agent_functions.supervisor.system_prompt import SYSTEM_PROMPT # Import SupervisorState

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
        return create_supervisor(
            [agent.compile(model) for agent in self.agents.values()],
            model=model,
            prompt=SYSTEM_PROMPT,
            output_mode="full_history"
        ).compile()
