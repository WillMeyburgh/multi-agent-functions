import os
import pickle
from pathlib import Path

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from multi_agent_functions.v1.google.calender.model.events import Event
from multi_agent_functions.v1.google.calender.model.calender_list import CalendarListEntry
from typing import Optional, Dict, Any, List

class GoogleCalendarClient:
    def __init__(self):
        self.credentials = self.__get_credentials()
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def calendar_list_delete(self, calendar_id: str) -> None:
        """
        Removes a calendar from the user's calendar list.

        Args:
            calendar_id (str): The ID of the calendar to delete.
        """
        self.service.calendarList().delete(calendarId=calendar_id).execute()

    def calendar_list_get(self, calendar_id: str) -> CalendarListEntry:
        """
        Returns a calendar from the user's calendar list.

        Args:
            calendar_id (str): The ID of the calendar to retrieve.

        Returns:
            CalendarListEntry: The retrieved calendar list entry.

        Raises:
            Exception: If the calendar is not found or an error occurs.
        """
        try:
            calendar_data = self.service.calendarList().get(calendarId=calendar_id).execute()
            if calendar_data:
                return CalendarListEntry.from_dict(calendar_data)
            else:
                raise Exception(f"Calendar with ID '{calendar_id}' not found.")
        except Exception as e:
            raise Exception(f"Failed to get calendar list entry: {e}")

    def calendar_list_insert(self, body: Dict[str, Any]) -> CalendarListEntry:
        """
        Inserts an existing calendar into the user's calendar list.

        Args:
            body (Dict[str, Any]): The request body for the calendar list entry.
                Expected keys include:
                - 'id' (str): The calendar ID to insert. (required)
                - 'colorId' (str): The color of the calendar in the UI.
                - 'hidden' (bool): Whether the calendar is hidden from the list.
                - 'selected' (bool): Whether the calendar is selected for display.
                - 'summaryOverride' (str): The summary that the user has set for the calendar.

        Returns:
            CalendarListEntry: The inserted calendar list entry.

        Raises:
            Exception: If insertion failed or an error occurs.
        """
        try:
            calendar_data = self.service.calendarList().insert(body=body).execute()
            if calendar_data:
                return CalendarListEntry.from_dict(calendar_data)
            else:
                raise Exception("Failed to insert calendar list entry: No data returned.")
        except Exception as e:
            raise Exception(f"Failed to insert calendar list entry: {e}")

    def calendar_list_list(self, **kwargs) -> List[CalendarListEntry]:
        """
        Returns the calendars on the user's calendar list.

        Args:
            **kwargs: Additional parameters for the list request. Common parameters include:
                - 'maxResults' (int): Maximum number of entries returned on one result page.
                - 'minAccessRole' (str): The minimum access role for the calendars to return.
                - 'pageToken' (str): Token specifying which result page to return.
                - 'showDeleted' (bool): Whether to include deleted calendars in the results.
                - 'showHidden' (bool): Whether to include hidden calendars in the results.
                - 'syncToken' (str): Token obtained from the nextSyncToken field returned on the last page of results from the previous list request.

        Returns:
            List[CalendarListEntry]: A list of calendar list entries.
        """
        calendars_data = self.service.calendarList().list(**kwargs).execute()
        return [CalendarListEntry.from_dict(item) for item in calendars_data.get('items', [])]

    def calendar_list_patch(self, calendar_id: str, body: Dict[str, Any]) -> Optional[CalendarListEntry]:
        """
        Updates an existing calendar on the user's calendar list. This method supports patch semantics.

        Args:
            calendar_id (str): The ID of the calendar to patch.
            body (Dict[str, Any]): The request body with the fields to patch.
                Expected keys include:
                - 'colorId' (str): The color of the calendar in the UI.
                - 'hidden' (bool): Whether the calendar is hidden from the list.
                - 'selected' (bool): Whether the calendar is selected for display.
                - 'summaryOverride' (str): The summary that the user has set for the calendar.
                Only the fields to be updated are required in the body.

        Returns:
            Optional[CalendarListEntry]: The updated calendar list entry, or None if update failed.
        """
        calendar_data = self.service.calendarList().patch(calendarId=calendar_id, body=body).execute()
        return CalendarListEntry.from_dict(calendar_data) if calendar_data else None

    def calendar_list_update(self, calendar_id: str, body: Dict[str, Any]) -> Optional[CalendarListEntry]:
        """
        Updates an existing calendar on the user's calendar list.

        Args:
            calendar_id (str): The ID of the calendar to update.
            body (Dict[str, Any]): The complete request body for the calendar list entry.
                Expected keys include:
                - 'id' (str): The calendar ID to insert. (required)
                - 'colorId' (str): The color of the calendar in the UI.
                - 'hidden' (bool): Whether the calendar is hidden from the list.
                - 'selected' (bool): Whether the calendar is selected for display.
                - 'summaryOverride' (str): The summary that the user has set for the calendar.
                All fields will be replaced with the values in the body.

        Returns:
            Optional[CalendarListEntry]: The updated calendar list entry, or None if update failed.
        """
        calendar_data = self.service.calendarList().update(calendarId=calendar_id, body=body).execute()
        return CalendarListEntry.from_dict(calendar_data) if calendar_data else None

    def calendar_list_watch(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Watch for changes to CalendarList resources.

        Args:
            body (Dict[str, Any]): The request body for the watch operation.
                Expected keys include:
                - 'id' (str): A UUID or similar unique string that identifies this channel. (required)
                - 'type' (str): The type of delivery mechanism used for this channel. (required, value is always 'web_hook')
                - 'address' (str): The URL where notifications are sent. (required)
                - 'expiration' (str): An optional expiration date and time for the channel.
                - 'token' (str): An optional arbitrary string that will be echoed back in notifications.

        Returns:
            Dict[str, Any]: The response from the watch operation.
        """
        return self.service.calendarList().watch(body=body).execute()

    def events_delete(self, calendar_id: str, event_id: str) -> None:
        """
        Deletes an event.

        Args:
            calendar_id (str): Calendar identifier.
            event_id (str): Event identifier.
        """
        self.service.events().delete(calendarId=calendar_id, eventId=event_id).execute()

    def events_get(self, calendar_id: str, event_id: str) -> Optional[Event]:
        """
        Returns an event based on its Google Calendar ID.

        Args:
            calendar_id (str): Calendar identifier.
            event_id (str): Event identifier.

        Returns:
            Optional[Event]: The retrieved event, or None if not found.
        """
        event_data = self.service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        return Event.from_dict(event_data) if event_data else None

    def events_import(self, calendar_id: str, body: Dict[str, Any]) -> Optional[Event]:
        """
        Imports an event.

        Args:
            calendar_id (str): Calendar identifier.
            body (Dict[str, Any]): The request body for the event.
                Expected keys include:
                - 'iCalUID' (str): The iCalendar UID of the event. (required)
                - 'sequence' (int): The sequence number of the event.
                - 'status' (str): Status of the event.
                - 'summary' (str): Title of the event.
                - 'description' (str): Description of the event.
                - 'location' (str): Geographic location of the event.
                - 'start' (Dict): The start time of the event. (required)
                    - 'date' (str): The date, in the format "yyyy-mm-dd".
                    - 'dateTime' (str): The date-time, in the RFC 3339 format.
                    - 'timeZone' (str): The time zone in RFC 5545 format.
                - 'end' (Dict): The end time of the event. (required)
                    - 'date' (str): The date, in the format "yyyy-mm-dd".
                    - 'dateTime' (str): The date-time, in the RFC 3339 format.
                    - 'timeZone' (str): The time zone in RFC 5545 format.
                - 'attendees' (List[Dict]): The attendees of the event.
                    - 'email' (str): The attendee's email address.
                    - 'displayName' (str): The attendee's name.
                    - 'responseStatus' (str): The attendee's response status.
                - 'reminders' (Dict): Information about the event's reminders.
                    - 'useDefault' (bool): Whether the default reminders of the calendar apply.
                    - 'overrides' (List[Dict]): If 'useDefault' is False, this lists the reminders for this event.
                        - 'method' (str): The reminder method.
                        - 'minutes' (int): The number of minutes before the start of the event when the reminder should trigger.
                - 'visibility' (str): Visibility of the event.

        Returns:
            Optional[Event]: The imported event, or None if import failed.
        """
        event_data = self.service.events().import_(calendarId=calendar_id, body=body).execute()
        return Event.from_dict(event_data) if event_data else None

    def events_insert(self, calendar_id: str, body: Dict[str, Any]) -> Optional[Event]:
        """
        Creates an event.

        Args:
            calendar_id (str): Calendar identifier.
            body (Dict[str, Any]): The request body for the event.
                Expected keys include:
                - 'summary' (str): Title of the event. (required)
                - 'location' (str): Geographic location of the event.
                - 'description' (str): Description of the event.
                - 'start' (Dict): The start time of the event. (required)
                    - 'date' (str): The date, in the format "yyyy-mm-dd".
                    - 'dateTime' (str): The date-time, in the RFC 3339 format.
                    - 'timeZone' (str): The time zone in RFC 5545 format.
                - 'end' (Dict): The end time of the event. (required)
                    - 'date' (str): The date, in the format "yyyy-mm-dd".
                    - 'dateTime' (str): The date-time, in the RFC 3339 format.
                    - 'timeZone' (str): The time zone in RFC 5545 format.
                - 'attendees' (List[Dict]): The attendees of the event.
                    - 'email' (str): The attendee's email address.
                    - 'displayName' (str): The attendee's name.
                    - 'responseStatus' (str): The attendee's response status.
                - 'reminders' (Dict): Information about the event's reminders.
                    - 'useDefault' (bool): Whether the default reminders of the calendar apply.
                    - 'overrides' (List[Dict]): If 'useDefault' is False, this lists the reminders for this event.
                        - 'method' (str): The reminder method.
                        - 'minutes' (int): The number of minutes before the start of the event when the reminder should trigger.
                - 'visibility' (str): Visibility of the event.

        Returns:
            Optional[Event]: The created event, or None if creation failed.
        """
        event_data = self.service.events().insert(calendarId=calendar_id, body=body).execute()
        return Event.from_dict(event_data) if event_data else None

    def events_instances(self, calendar_id: str, event_id: str, **kwargs) -> List[Event]:
        """
        Returns instances of the specified recurring event.

        Args:
            calendar_id (str): Calendar identifier.
            event_id (str): Recurring event identifier.
            **kwargs: Additional parameters for the instances request. Common parameters include:
                - 'maxResults' (int): Maximum number of instances returned on one result page.
                - 'originalStart' (str): The original start time of the instance in the result.
                - 'pageToken' (str): Token specifying which result page to return.
                - 'showDeleted' (bool): Whether to include deleted events.
                - 'timeMax' (str): Upper bound (exclusive) for an event's start time to filter by.
                - 'timeMin' (str): Lower bound (inclusive) for an event's start time to filter by.

        Returns:
            List[Event]: A list of event instances.
        """
        instances_data = self.service.events().instances(calendarId=calendar_id, eventId=event_id, **kwargs).execute()
        return [Event.from_dict(item) for item in instances_data.get('items', [])]

    def events_list(self, calendar_id: str = 'primary', **kwargs) -> List[Event]:
        """
        Returns events on the specified calendar.

        Args:
            calendar_id (str): Calendar identifier. Defaults to 'primary'.
            **kwargs: Additional parameters for the list request. Common parameters include:
                - 'iCalUID' (str): Specifies an iCalendar UID in the response.
                - 'maxAttendees' (int): The maximum number of attendees to include in the response.
                - 'maxResults' (int): Maximum number of events returned on one result page.
                - 'orderBy' (str): The order of the events returned in the result.
                - 'pageToken' (str): Token specifying which result page to return.
                - 'q' (str): Free text search terms to find events that match these terms in the following fields: summary, description, location, attendee's displayName, attendee's email.
                - 'showDeleted' (bool): Whether to include deleted events.
                - 'showHiddenInvitations' (bool): Whether to include events with hidden invitations.
                - 'singleEvents' (bool): Whether to expand recurring events into instances and return single events.
                - 'syncToken' (str): Token obtained from the nextSyncToken field returned on the last page of results from the previous list request.
                - 'timeMax' (str): Upper bound (exclusive) for an event's start time to filter by.
                - 'timeMin' (str): Lower bound (inclusive) for an event's start time to filter by.
                - 'timeZone' (str): Time zone used in the response.
                - 'updatedMin' (str): Lower bound for an event's last modification time (inclusive) to filter by.

        Returns:
            List[Event]: A list of events.
        """
        events_data = self.service.events().list(calendarId=calendar_id, **kwargs).execute()
        return [Event.from_dict(item) for item in events_data.get('items', [])]

    def events_move(self, calendar_id: str, event_id: str, destination_calendar_id: str) -> Optional[Event]:
        """
        Moves an event to another calendar.

        Args:
            calendar_id (str): Calendar identifier of the source calendar.
            event_id (str): Event identifier.
            destination_calendar_id (str): Calendar identifier of the destination calendar.

        Returns:
            Optional[Event]: The moved event, or None if move failed.
        """
        event_data = self.service.events().move(calendarId=calendar_id, eventId=event_id, destination=destination_calendar_id).execute()
        return Event.from_dict(event_data) if event_data else None

    def events_patch(self, calendar_id: str, event_id: str, body: Dict[str, Any]) -> Optional[Event]:
        """
        Updates an event. This method supports patch semantics.

        Args:
            calendar_id (str): Calendar identifier.
            event_id (str): Event identifier.
            body (Dict[str, Any]): The request body with the fields to patch.
                Expected keys include:
                - 'summary' (str): Title of the event.
                - 'location' (str): Geographic location of the event.
                - 'description' (str): Description of the event.
                - 'start' (Dict): The start time of the event.
                    - 'date' (str): The date, in the format "yyyy-mm-dd".
                    - 'dateTime' (str): The date-time, in the RFC 3339 format.
                    - 'timeZone' (str): The time zone in RFC 5545 format.
                - 'end' (Dict): The end time of the event.
                    - 'date' (str): The date, in the format "yyyy-mm-dd".
                    - 'dateTime' (str): The date-time, in the RFC 3339 format.
                    - 'timeZone' (str): The time zone in RFC 5545 format.
                - 'attendees' (List[Dict]): The attendees of the event.
                    - 'email' (str): The attendee's email address.
                    - 'displayName' (str): The attendee's name.
                    - 'responseStatus' (str): The attendee's response status.
                - 'reminders' (Dict): Information about the event's reminders.
                    - 'useDefault' (bool): Whether the default reminders of the calendar apply.
                    - 'overrides' (List[Dict]): If 'useDefault' is False, this lists the reminders for this event.
                        - 'method' (str): The reminder method.
                        - 'minutes' (int): The number of minutes before the start of the event when the reminder should trigger.
                - 'visibility' (str): Visibility of the event.
                Only the fields to be updated are required in the body.

        Returns:
            Optional[Event]: The patched event, or None if patch failed.
        """
        event_data = self.service.events().patch(calendarId=calendar_id, eventId=event_id, body=body).execute()
        return Event.from_dict(event_data) if event_data else None

    def events_quick_add(self, calendar_id: str, text: str) -> Optional[Event]:
        """
        Creates an event based on a simple text string.

        Args:
            calendar_id (str): Calendar identifier.
            text (str): The text string to create the event from.

        Returns:
            Optional[Event]: The created event, or None if creation failed.
        """
        event_data = self.service.events().quickAdd(calendarId=calendar_id, text=text).execute()
        return Event.from_dict(event_data) if event_data else None

    def events_update(self, calendar_id: str, event_id: str, body: Dict[str, Any]) -> Optional[Event]:
        """
        Updates an event. This method does not support patch semantics.

        Args:
            calendar_id (str): Calendar identifier.
            event_id (str): Event identifier.
            body (Dict[str, Any]): The complete request body for the event.
                Expected keys include:
                - 'summary' (str): Title of the event. (required)
                - 'location' (str): Geographic location of the event.
                - 'description' (str): Description of the event.
                - 'start' (Dict): The start time of the event. (required)
                    - 'date' (str): The date, in the format "yyyy-mm-dd".
                    - 'dateTime' (str): The date-time, in the RFC 3339 format.
                    - 'timeZone' (str): The time zone in RFC 5545 format.
                - 'end' (Dict): The end time of the event. (required)
                    - 'date' (str): The date, in the format "yyyy-mm-dd".
                    - 'dateTime' (str): The date-time, in the RFC 3339 format.
                    - 'timeZone' (str): The time zone in RFC 5545 format.
                - 'attendees' (List[Dict]): The attendees of the event.
                    - 'email' (str): The attendee's email address.
                    - 'displayName' (str): The attendee's name.
                    - 'responseStatus' (str): The attendee's response status.
                - 'reminders' (Dict): Information about the event's reminders.
                    - 'useDefault' (bool): Whether the default reminders of the calendar apply.
                    - 'overrides' (List[Dict]): If 'useDefault' is False, this lists the reminders for this event.
                        - 'method' (str): The reminder method.
                        - 'minutes' (int): The number of minutes before the start of the event when the reminder should trigger.
                - 'visibility' (str): Visibility of the event.
                All fields will be replaced with the values in the body.

        Returns:
            Optional[Event]: The updated event, or None if update failed.
        """
        event_data = self.service.events().update(calendarId=calendar_id, eventId=event_id, body=body).execute()
        return Event.from_dict(event_data) if event_data else None

    def events_watch(self, calendar_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Watch for changes to Events resources.

        Args:
            calendar_id (str): Calendar identifier.
            body (Dict[str, Any]): The request body for the watch operation.
                Expected keys include:
                - 'id' (str): A UUID or similar unique string that identifies this channel. (required)
                - 'type' (str): The type of delivery mechanism used for this channel. (required, value is always 'web_hook')
                - 'address' (str): The URL where notifications are sent. (required)
                - 'expiration' (str): An optional expiration date and time for the channel.
                - 'token' (str): An optional arbitrary string that will be echoed back in notifications.

        Returns:
            Dict[str, Any]: The response from the watch operation.
        """
        return self.service.events().watch(calendarId=calendar_id, body=body).execute()

    def __get_credentials(self):
        """
        Retrieves user credentials for Google Calendar API.
        It first tries to load credentials from a pickle file. If not found or expired,
        it initiates the OAuth 2.0 flow to get new credentials and saves them.

        Returns:
            google.oauth2.credentials.Credentials: The user's Google API credentials.
        """
        Path('tmp').mkdir(exist_ok=True)
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None
        if os.path.exists('tmp/google-calendar-token.pickle'):
            with open('tmp/google-calendar-token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('tmp/google-calendar-token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds
