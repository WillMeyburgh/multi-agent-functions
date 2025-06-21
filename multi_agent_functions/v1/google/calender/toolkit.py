from typing import List
from langchain_core.tools import create_schema_from_function, BaseTool, StructuredTool
from datetime import datetime

from multi_agent_functions.v1.google.calender.client import GoogleCalendarClient
from multi_agent_functions.v1.google.calender.model.events import Event
from multi_agent_functions.v1.google.calender.model.calender_list import CalendarListEntry
from multi_agent_functions.v1.google.calender.state import GoogleCalendarAgentState

class GoogleCalendarToolkit:
    def __init__(self):
        self.client = GoogleCalendarClient()

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
                Event.from_dict,
                CalendarListEntry.from_dict,
                Event.to_dict,
                CalendarListEntry.to_dict,
                self.client.calendar_list_list,
                self.client.calendar_list_delete,
                self.client.calendar_list_get,
                self.client.calendar_list_insert,
                self.client.calendar_list_patch,
                self.client.calendar_list_update,
                self.client.calendar_list_watch,
                self.client.events_list,
                self.client.events_delete,
                self.client.events_get,
                self.client.events_import,
                self.client.events_insert,
                self.client.events_instances,
                self.client.events_move,
                self.client.events_patch,
                self.client.events_quick_add,
                self.client.events_update,
                self.client.events_watch,
            ]
        ))
