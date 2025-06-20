from typing import Annotated, List, Sequence, TypedDict
from operator import add as add_messages
from langchain_core.messages import BaseMessage

from multi_agent_functions.v1.google.calender.model.calender_list import CalendarListEntry


class GoogleCalendarAgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    calendars: Annotated[List[CalendarListEntry], "Store all remote calendar information"]
