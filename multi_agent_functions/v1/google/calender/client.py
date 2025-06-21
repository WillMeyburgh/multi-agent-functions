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

    def calendar_list_insert(self, id: str, color_id: Optional[str] = None, hidden: Optional[bool] = None, selected: Optional[bool] = None, summary_override: Optional[str] = None) -> CalendarListEntry:
        """
        Inserts an existing calendar into the user's calendar list.

        Args:
            id (str): The calendar ID to insert. (required)
            color_id (Optional[str]): The color of the calendar in the UI.
            hidden (Optional[bool]): Whether the calendar is hidden from the list.
            selected (Optional[bool]): Whether the calendar is selected for display.
            summary_override (Optional[str]): The summary that the user has set for the calendar.

        Returns:
            CalendarListEntry: The inserted calendar list entry.

        Raises:
            Exception: If insertion failed or an error occurs.
        """
        try:
            body = {'id': id}
            if color_id is not None:
                body['colorId'] = color_id
            if hidden is not None:
                body['hidden'] = hidden
            if selected is not None:
                body['selected'] = selected
            if summary_override is not None:
                body['summaryOverride'] = summary_override

            calendar_data = self.service.calendarList().insert(body=body).execute()
            if calendar_data:
                return CalendarListEntry.from_dict(calendar_data)
            else:
                raise Exception("Failed to insert calendar list entry: No data returned.")
        except Exception as e:
            raise Exception(f"Failed to insert calendar list entry: {e}")

    def calendar_list_list(self, max_results: Optional[int] = None, min_access_role: Optional[str] = None, page_token: Optional[str] = None, show_deleted: Optional[bool] = None, show_hidden: Optional[bool] = None, sync_token: Optional[str] = None) -> List[CalendarListEntry]:
        """
        Returns the calendars on the user's calendar list.

        Args:
            max_results (Optional[int]): Maximum number of entries returned on one result page.
            min_access_role (Optional[str]): The minimum access role for the calendars to return.
            page_token (Optional[str]): Token specifying which result page to return.
            show_deleted (Optional[bool]): Whether to include deleted calendars in the results.
            show_hidden (Optional[bool]): Whether to include hidden calendars in the results.
            sync_token (Optional[str]): Token obtained from the nextSyncToken field returned on the last page of results from the previous list request.

        Returns:
            List[CalendarListEntry]: A list of calendar list entries.
        """
        kwargs = {}
        if max_results is not None:
            kwargs['maxResults'] = max_results
        if min_access_role is not None:
            kwargs['minAccessRole'] = min_access_role
        if page_token is not None:
            kwargs['pageToken'] = page_token
        if show_deleted is not None:
            kwargs['showDeleted'] = show_deleted
        if show_hidden is not None:
            kwargs['showHidden'] = show_hidden
        if sync_token is not None:
            kwargs['syncToken'] = sync_token

        calendars_data = self.service.calendarList().list(**kwargs).execute()
        return [CalendarListEntry.from_dict(item) for item in calendars_data.get('items', [])]

    def calendar_list_patch(self, calendar_id: str, color_id: Optional[str] = None, hidden: Optional[bool] = None, selected: Optional[bool] = None, summary_override: Optional[str] = None) -> Optional[CalendarListEntry]:
        """
        Updates an existing calendar on the user's calendar list. This method supports patch semantics.

        Args:
            calendar_id (str): The ID of the calendar to patch.
            color_id (Optional[str]): The color of the calendar in the UI.
            hidden (Optional[bool]): Whether the calendar is hidden from the list.
            selected (Optional[bool]): Whether the calendar is selected for display.
            summary_override (Optional[str]): The summary that the user has set for the calendar.
            Only the fields to be updated are required.

        Returns:
            Optional[CalendarListEntry]: The updated calendar list entry, or None if update failed.
        """
        body = {}
        if color_id is not None:
            body['colorId'] = color_id
        if hidden is not None:
            body['hidden'] = hidden
        if selected is not None:
            body['selected'] = selected
        if summary_override is not None:
            body['summaryOverride'] = summary_override

        calendar_data = self.service.calendarList().patch(calendarId=calendar_id, body=body).execute()
        return CalendarListEntry.from_dict(calendar_data) if calendar_data else None

    def calendar_list_update(self, calendar_id: str, id: str, color_id: Optional[str] = None, hidden: Optional[bool] = None, selected: Optional[bool] = None, summary_override: Optional[str] = None) -> Optional[CalendarListEntry]:
        """
        Updates an existing calendar on the user's calendar list.

        Args:
            calendar_id (str): The ID of the calendar to update.
            id (str): The calendar ID. (required)
            color_id (Optional[str]): The color of the calendar in the UI.
            hidden (Optional[bool]): Whether the calendar is hidden from the list.
            selected (Optional[bool]): Whether the calendar is selected for display.
            summary_override (Optional[str]): The summary that the user has set for the calendar.
            All fields will be replaced with the values provided.

        Returns:
            Optional[CalendarListEntry]: The updated calendar list entry, or None if update failed.
        """
        body = {'id': id}
        if color_id is not None:
            body['colorId'] = color_id
        if hidden is not None:
            body['hidden'] = hidden
        if selected is not None:
            body['selected'] = selected
        if summary_override is not None:
            body['summaryOverride'] = summary_override

        calendar_data = self.service.calendarList().update(calendarId=calendar_id, body=body).execute()
        return CalendarListEntry.from_dict(calendar_data) if calendar_data else None

    def calendar_list_watch(self, id: str, type: str, address: str, expiration: Optional[str] = None, token: Optional[str] = None) -> Dict[str, Any]:
        """
        Watch for changes to CalendarList resources.

        Args:
            id (str): A UUID or similar unique string that identifies this channel. (required)
            type (str): The type of delivery mechanism used for this channel. (required, value is always 'web_hook')
            address (str): The URL where notifications are sent. (required)
            expiration (Optional[str]): An optional expiration date and time for the channel.
            token (Optional[str]): An optional arbitrary string that will be echoed back in notifications.

        Returns:
            Dict[str, Any]: The response from the watch operation.
        """
        body = {
            'id': id,
            'type': type,
            'address': address,
        }
        if expiration is not None:
            body['expiration'] = expiration
        if token is not None:
            body['token'] = token
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

    def events_import(self, calendar_id: str, i_cal_uid: str, start: Dict[str, Any], end: Dict[str, Any], sequence: Optional[int] = None, status: Optional[str] = None, summary: Optional[str] = None, description: Optional[str] = None, location: Optional[str] = None, attendees: Optional[List[Dict[str, Any]]] = None, reminders: Optional[Dict[str, Any]] = None, visibility: Optional[str] = None) -> Optional[Event]:
        """
        Imports an event.

        Args:
            calendar_id (str): Calendar identifier.
            i_cal_uid (str): The iCalendar UID of the event. (required)
            start (Dict[str, Any]): The start time of the event. (required)
                - 'date' (str): The date, in the format "yyyy-mm-dd".
                - 'dateTime' (str): The date-time, in the RFC 3339 format.
                - 'timeZone' (str): The time zone in RFC 5545 format.
            end (Dict[str, Any]): The end time of the event. (required)
                - 'date' (str): The date, in the format "yyyy-mm-dd".
                - 'dateTime' (str): The date-time, in the RFC 3339 format.
                - 'timeZone' (str): The time zone in RFC 5545 format.
            sequence (Optional[int]): The sequence number of the event.
            status (Optional[str]): Status of the event.
            summary (Optional[str]): Title of the event.
            description (Optional[str]): Description of the event.
            location (Optional[str]): Geographic location of the event.
            attendees (Optional[List[Dict[str, Any]]]): The attendees of the event.
                - 'email' (str): The attendee's email address.
                - 'displayName' (str): The attendee's name.
                - 'responseStatus' (str): The attendee's response status.
            reminders (Optional[Dict[str, Any]]): Information about the event's reminders.
                - 'useDefault' (bool): Whether the default reminders of the calendar apply.
                - 'overrides' (List[Dict]): If 'useDefault' is False, this lists the reminders for this event.
                    - 'method' (str): The reminder method.
                    - 'minutes' (int): The number of minutes before the start of the event when the reminder should trigger.
            visibility (Optional[str]): Visibility of the event.

        Returns:
            Optional[Event]: The imported event, or None if import failed.
        """
        body = {
            'iCalUID': i_cal_uid,
            'start': start,
            'end': end,
        }
        if sequence is not None:
            body['sequence'] = sequence
        if status is not None:
            body['status'] = status
        if summary is not None:
            body['summary'] = summary
        if description is not None:
            body['description'] = description
        if location is not None:
            body['location'] = location
        if attendees is not None:
            body['attendees'] = attendees
        if reminders is not None:
            body['reminders'] = reminders
        if visibility is not None:
            body['visibility'] = visibility

        event_data = self.service.events().import_(calendarId=calendar_id, body=body).execute()
        return Event.from_dict(event_data) if event_data else None

    def events_insert(self, calendar_id: str, summary: str, start: Dict[str, Any], end: Dict[str, Any], location: Optional[str] = None, description: Optional[str] = None, attendees: Optional[List[Dict[str, Any]]] = None, reminders: Optional[Dict[str, Any]] = None, visibility: Optional[str] = None) -> Optional[Event]:
        """
        Creates an event.

        Args:
            calendar_id (str): Calendar identifier.
            summary (str): Title of the event. (required)
            start (Dict[str, Any]): The start time of the event. (required)
                - 'date' (str): The date, in the format "yyyy-mm-dd".
                - 'dateTime' (str): The date-time, in the RFC 3339 format.
                - 'timeZone' (str): The time zone in RFC 5545 format.
            end (Dict[str, Any]): The end time of the event. (required)
                - 'date' (str): The date, in the format "yyyy-mm-dd".
                - 'dateTime' (str): The date-time, in the RFC 3339 format.
                - 'timeZone' (str): The time zone in RFC 5545 format.
            location (Optional[str]): Geographic location of the event.
            description (Optional[str]): Description of the event.
            attendees (Optional[List[Dict[str, Any]]]): The attendees of the event.
                - 'email' (str): The attendee's email address.
                - 'displayName' (str): The attendee's name.
                - 'responseStatus' (str): The attendee's response status.
            reminders (Optional[Dict[str, Any]]): Information about the event's reminders.
                - 'useDefault' (bool): Whether the default reminders of the calendar apply.
                - 'overrides' (List[Dict]): If 'useDefault' is False, this lists the reminders for this event.
                    - 'method' (str): The reminder method.
                    - 'minutes' (int): The number of minutes before the start of the event when the reminder should trigger.
            visibility (Optional[str]): Visibility of the event.

        Returns:
            Optional[Event]: The created event, or None if creation failed.
        """
        # Ensure timeZone is set for start and end times
        if 'timeZone' not in start:
            start['timeZone'] = 'Africa/Johannesburg'
        if 'timeZone' not in end:
            end['timeZone'] = 'Africa/Johannesburg'

        body = {
            'summary': summary,
            'start': start,
            'end': end,
        }
        if location is not None:
            body['location'] = location
        if description is not None:
            body['description'] = description
        if attendees is not None:
            body['attendees'] = attendees
        if reminders is not None:
            body['reminders'] = reminders
        if visibility is not None:
            body['visibility'] = visibility

        event_data = self.service.events().insert(calendarId=calendar_id, body=body).execute()
        return Event.from_dict(event_data) if event_data else None

    def events_instances(self, calendar_id: str, event_id: str, max_results: Optional[int] = None, original_start: Optional[str] = None, page_token: Optional[str] = None, show_deleted: Optional[bool] = None, time_max: Optional[str] = None, time_min: Optional[str] = None) -> List[Event]:
        """
        Returns instances of the specified recurring event.

        Args:
            calendar_id (str): Calendar identifier.
            event_id (str): Recurring event identifier.
            max_results (Optional[int]): Maximum number of instances returned on one result page.
            original_start (Optional[str]): The original start time of the instance in the result.
            page_token (Optional[str]): Token specifying which result page to return.
            show_deleted (Optional[bool]): Whether to include deleted events.
            time_max (Optional[str]): Upper bound (exclusive) for an event's start time to filter by.
            time_min (Optional[str]): Lower bound (inclusive) for an event's start time to filter by.

        Returns:
            List[Event]: A list of event instances.
        """
        kwargs = {}
        if max_results is not None:
            kwargs['maxResults'] = max_results
        if original_start is not None:
            kwargs['originalStart'] = original_start
        if page_token is not None:
            kwargs['pageToken'] = page_token
        if show_deleted is not None:
            kwargs['showDeleted'] = show_deleted
        if time_max is not None:
            kwargs['timeMax'] = time_max
        if time_min is not None:
            kwargs['timeMin'] = time_min

        instances_data = self.service.events().instances(calendarId=calendar_id, eventId=event_id, **kwargs).execute()
        return [Event.from_dict(item) for item in instances_data.get('items', [])]

    def events_list(self, calendar_id: str = 'primary', i_cal_uid: Optional[str] = None, max_attendees: Optional[int] = None, max_results: Optional[int] = None, order_by: Optional[str] = None, page_token: Optional[str] = None, q: Optional[str] = None, show_deleted: Optional[bool] = None, show_hidden_invitations: Optional[bool] = None, single_events: Optional[bool] = None, sync_token: Optional[str] = None, time_max: Optional[str] = None, time_min: Optional[str] = None, time_zone: Optional[str] = None, updated_min: Optional[str] = None) -> List[Event]:
        """
        Returns events on the specified calendar.

        Args:
            calendar_id (str): Calendar identifier. Defaults to 'primary'.
            i_cal_uid (Optional[str]): Specifies an iCalendar UID in the response.
            max_attendees (Optional[int]): The maximum number of attendees to include in the response.
            max_results (Optional[int]): Maximum number of events returned on one result page.
            order_by (Optional[str]): The order of the events returned in the result.
            page_token (Optional[str]): Token specifying which result page to return.
            q (Optional[str]): Free text search terms to find events that match these terms in the following fields: summary, description, location, attendee's displayName, attendee's email.
            show_deleted (Optional[bool]): Whether to include deleted events.
            show_hidden_invitations (Optional[bool]): Whether to include events with hidden invitations.
            single_events (Optional[bool]): Whether to expand recurring events into instances and return single events.
            sync_token (Optional[str]): Token obtained from the nextSyncToken field returned on the last page of results from the previous list request.
            time_max (Optional[str]): Upper bound (exclusive) for an event's start time to filter by.
            time_min (Optional[str]): Lower bound (inclusive) for an event's start time to filter by.
            time_zone (Optional[str]): Time zone used in the response.
            updated_min (Optional[str]): Lower bound for an event's last modification time (inclusive) to filter by.

        Returns:
            List[Event]: A list of events.
        """
        kwargs = {}
        if i_cal_uid is not None:
            kwargs['iCalUID'] = i_cal_uid
        if max_attendees is not None:
            kwargs['maxAttendees'] = max_attendees
        if max_results is not None:
            kwargs['maxResults'] = max_results
        if order_by is not None:
            kwargs['orderBy'] = order_by
        if page_token is not None:
            kwargs['pageToken'] = page_token
        if q is not None:
            kwargs['q'] = q
        if show_deleted is not None:
            kwargs['showDeleted'] = show_deleted
        if show_hidden_invitations is not None:
            kwargs['showHiddenInvitations'] = show_hidden_invitations
        if single_events is not None:
            kwargs['singleEvents'] = single_events
        if sync_token is not None:
            kwargs['syncToken'] = sync_token
        if time_max is not None:
            kwargs['timeMax'] = time_max
        if time_min is not None:
            kwargs['timeMin'] = time_min
        if time_zone is not None:
            kwargs['timeZone'] = time_zone
        if updated_min is not None:
            kwargs['updatedMin'] = updated_min

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

    def events_patch(self, calendar_id: str, event_id: str, summary: Optional[str] = None, location: Optional[str] = None, description: Optional[str] = None, start: Optional[Dict[str, Any]] = None, end: Optional[Dict[str, Any]] = None, attendees: Optional[List[Dict[str, Any]]] = None, reminders: Optional[Dict[str, Any]] = None, visibility: Optional[str] = None) -> Optional[Event]:
        """
        Updates an event. This method supports patch semantics.

        Args:
            calendar_id (str): Calendar identifier.
            event_id (str): Event identifier.
            summary (Optional[str]): Title of the event.
            location (Optional[str]): Geographic location of the event.
            description (Optional[str]): Description of the event.
            start (Optional[Dict[str, Any]]): The start time of the event.
                - 'date' (str): The date, in the format "yyyy-mm-dd".
                - 'dateTime' (str): The date-time, in the RFC 3339 format.
                - 'timeZone' (str): The time zone in RFC 5545 format.
            end (Optional[Dict[str, Any]]): The end time of the event.
                - 'date' (str): The date, in the format "yyyy-mm-dd".
                - 'dateTime' (str): The date-time, in the RFC 3339 format.
                - 'timeZone' (str): The time zone in RFC 5545 format.
            attendees (Optional[List[Dict[str, Any]]]): The attendees of the event.
                - 'email' (str): The attendee's email address.
                - 'displayName' (str): The attendee's name.
                - 'responseStatus' (str): The attendee's response status.
            reminders (Optional[Dict[str, Any]]): Information about the event's reminders.
                - 'useDefault' (bool): Whether the default reminders of the calendar apply.
                - 'overrides' (List[Dict]): If 'useDefault' is False, this lists the reminders for this event.
                    - 'method' (str): The reminder method.
                    - 'minutes' (int): The number of minutes before the start of the event when the reminder should trigger.
            visibility (Optional[str]): Visibility of the event.
            Only the fields to be updated are required.

        Returns:
            Optional[Event]: The patched event, or None if patch failed.
        """
        body = {}
        if summary is not None:
            body['summary'] = summary
        if location is not None:
            body['location'] = location
        if description is not None:
            body['description'] = description
        if start is not None:
            body['start'] = start
        if end is not None:
            body['end'] = end
        if attendees is not None:
            body['attendees'] = attendees
        if reminders is not None:
            body['reminders'] = reminders
        if visibility is not None:
            body['visibility'] = visibility

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

    def events_update(self, calendar_id: str, event_id: str, summary: str, start: Dict[str, Any], end: Dict[str, Any], location: Optional[str] = None, description: Optional[str] = None, attendees: Optional[List[Dict[str, Any]]] = None, reminders: Optional[Dict[str, Any]] = None, visibility: Optional[str] = None) -> Optional[Event]:
        """
        Updates an event. This method does not support patch semantics.

        Args:
            calendar_id (str): Calendar identifier.
            event_id (str): Event identifier.
            summary (str): Title of the event. (required)
            start (Dict[str, Any]): The start time of the event. (required)
                - 'date' (str): The date, in the format "yyyy-mm-dd".
                - 'dateTime' (str): The date-time, in the RFC 3339 format.
                - 'timeZone' (str): The time zone in RFC 5545 format.
            end (Dict[str, Any]): The end time of the event. (required)
                - 'date' (str): The date, in the format "yyyy-mm-dd".
                - 'dateTime' (str): The date-time, in the RFC 3339 format.
                - 'timeZone' (str): The time zone in RFC 5545 format.
            location (Optional[str]): Geographic location of the event.
            description (Optional[str]): Description of the event.
            attendees (Optional[List[Dict[str, Any]]]): The attendees of the event.
                - 'email' (str): The attendee's email address.
                - 'displayName' (str): The attendee's name.
                - 'responseStatus' (str): The attendee's response status.
            reminders (Optional[Dict[str, Any]]): Information about the event's reminders.
                - 'useDefault' (bool): Whether the default reminders of the calendar apply.
                - 'overrides' (List[Dict]): If 'useDefault' is False, this lists the reminders for this event.
                    - 'method' (str): The reminder method.
                    - 'minutes' (int): The number of minutes before the start of the event when the reminder should trigger.
            visibility (Optional[str]): Visibility of the event.
            All fields will be replaced with the values provided.

        Returns:
            Optional[Event]: The updated event, or None if update failed.
        """
        body = {
            'summary': summary,
            'start': start,
            'end': end,
        }
        if location is not None:
            body['location'] = location
        if description is not None:
            body['description'] = description
        if attendees is not None:
            body['attendees'] = attendees
        if reminders is not None:
            body['reminders'] = reminders
        if visibility is not None:
            body['visibility'] = visibility

        event_data = self.service.events().update(calendarId=calendar_id, eventId=event_id, body=body).execute()
        return Event.from_dict(event_data) if event_data else None

    def events_watch(self, calendar_id: str, id: str, type: str, address: str, expiration: Optional[str] = None, token: Optional[str] = None) -> Dict[str, Any]:
        """
        Watch for changes to Events resources.

        Args:
            calendar_id (str): Calendar identifier.
            id (str): A UUID or similar unique string that identifies this channel. (required)
            type (str): The type of delivery mechanism used for this channel. (required, value is always 'web_hook')
            address (str): The URL where notifications are sent. (required)
            expiration (Optional[str]): An optional expiration date and time for the channel.
            token (Optional[str]): An optional arbitrary string that will be echoed back in notifications.

        Returns:
            Dict[str, Any]: The response from the watch operation.
        """
        body = {
            'id': id,
            'type': type,
            'address': address,
        }
        if expiration is not None:
            body['expiration'] = expiration
        if token is not None:
            body['token'] = token
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
