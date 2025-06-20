from typing import Optional, Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent

from multi_agent_functions.v1.google.calender.state import GoogleCalendarAgentState
from multi_agent_functions.v1.google.calender.system_prompt import SYSTEM_PROMPT
from multi_agent_functions.v1.google.calender.toolkit import GoogleCalendarToolkit


class GoogleCalendarAgent():
    @classmethod
    def init_state(cls, messages: Optional[Sequence[BaseMessage]] = None) -> GoogleCalendarAgentState:
        return GoogleCalendarAgentState(
            messages=messages or [], 
            calendars=[]
        )
    
    def __init__(self):
        self.toolkit = GoogleCalendarToolkit()
    
    def compile(self, model) -> CompiledStateGraph:
        return create_react_agent(
            model,
            tools=self.toolkit.get_tools(),
            prompt=SYSTEM_PROMPT,
            name='google_calender'
        )
