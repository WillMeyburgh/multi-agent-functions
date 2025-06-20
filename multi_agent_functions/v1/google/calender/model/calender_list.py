from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any

@dataclass(frozen=True)
class DefaultReminder:
    method: str
    minutes: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DefaultReminder":
        """
        Creates a DefaultReminder object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing default reminder data with the following keys:
                - 'method' (str): The method used by this reminder. Possible values are "email", "sms", or "popup".
                - 'minutes' (int): The number of minutes before the start of the event when the reminder should trigger.

        Returns:
            DefaultReminder: A DefaultReminder object populated with the provided data.
        """
        return cls(
            method=data["method"],
            minutes=data["minutes"]
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the DefaultReminder object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the DefaultReminder object.
        """
        return asdict(self)

@dataclass(frozen=True)
class Notification:
    type: str
    method: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Notification":
        """
        Creates a Notification object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing notification data with the following keys:
                - 'type' (str): The type of notification. Possible values are "eventCreation", "eventChange", "eventCancellation", "eventResponse", or "agenda".
                - 'method' (str): The method used to deliver the notification. Possible values are "email" or "sms".

        Returns:
            Notification: A Notification object populated with the provided data.
        """
        return cls(
            type=data["type"],
            method=data["method"]
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Notification object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the Notification object.
        """
        return asdict(self)

@dataclass(frozen=True)
class NotificationSettings:
    notifications: List[Notification] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NotificationSettings":
        """
        Creates a NotificationSettings object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing notification settings data with the following keys:
                - 'notifications' (List[Dict[str, Any]], optional): The list of notifications.

        Returns:
            NotificationSettings: A NotificationSettings object populated with the provided data.
        """
        return cls(
            notifications=[Notification.from_dict(n) for n in data.get("notifications", [])]
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the NotificationSettings object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the NotificationSettings object.
        """
        return asdict(self)

@dataclass(frozen=True)
class ConferenceProperties:
    allowedConferenceSolutionTypes: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConferenceProperties":
        """
        Creates a ConferenceProperties object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing conference properties data with the following keys:
                - 'allowedConferenceSolutionTypes' (List[str], optional): The types of conference solutions that are allowed for this calendar.

        Returns:
            ConferenceProperties: A ConferenceProperties object populated with the provided data.
        """
        return cls(
            allowedConferenceSolutionTypes=data.get("allowedConferenceSolutionTypes", [])
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ConferenceProperties object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the ConferenceProperties object.
        """
        return asdict(self)

@dataclass(frozen=True)
class CalendarListEntry:
    kind: str
    etag: str
    id: str
    summary: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    timeZone: Optional[str] = None
    summaryOverride: Optional[str] = None
    colorId: Optional[str] = None
    backgroundColor: Optional[str] = None
    foregroundColor: Optional[str] = None
    hidden: Optional[bool] = None
    selected: Optional[bool] = None
    accessRole: Optional[str] = None
    defaultReminders: List[DefaultReminder] = field(default_factory=list)
    notificationSettings: Optional[NotificationSettings] = None
    primary: Optional[bool] = None
    deleted: Optional[bool] = None
    conferenceProperties: Optional[ConferenceProperties] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CalendarListEntry":
        """
        Creates a CalendarListEntry object from a dictionary, typically received from the Google Calendar API.

        Args:
            data (Dict[str, Any]): A dictionary containing calendar list entry data with the following keys:
                - 'kind' (str): Type of the resource. Value is always "calendar#calendarListEntry".
                - 'etag' (str): ETag of the resource.
                - 'id' (str): The calendar's ID.
                - 'summary' (str, optional): The summary that the user has set for this calendar.
                - 'description' (str, optional): The description of the calendar.
                - 'location' (str, optional): The location of the calendar.
                - 'timeZone' (str, optional): The time zone of the calendar.
                - 'summaryOverride' (str, optional): The summary that the user has set for this calendar.
                - 'colorId' (str, optional): The color of the calendar.
                - 'backgroundColor' (str, optional): The background color of the calendar.
                - 'foregroundColor' (str, optional): The foreground color of the calendar.
                - 'hidden' (bool, optional): Whether this calendar is hidden from the list.
                - 'selected' (bool, optional): Whether this calendar is selected for display.
                - 'accessRole' (str, optional): The main color of the calendar in the calendar list.
                - 'defaultReminders' (List[Dict[str, Any]], optional): The default reminders that the user has set for this calendar.
                - 'notificationSettings' (Dict[str, Any], optional): The notification settings for this calendar.
                - 'primary' (bool, optional): Whether this is the primary calendar for the user.
                - 'deleted' (bool, optional): Whether this calendar has been deleted from the calendar list.
                - 'conferenceProperties' (Dict[str, Any], optional): The conference properties for this calendar.

        Returns:
            CalendarListEntry: A CalendarListEntry object populated with the provided data.
        """
        default_reminders = [DefaultReminder.from_dict(dr) for dr in data.get("defaultReminders", [])]
        notification_settings = NotificationSettings.from_dict(data["notificationSettings"]) if "notificationSettings" in data else None
        conference_properties = ConferenceProperties.from_dict(data["conferenceProperties"]) if "conferenceProperties" in data else None

        return cls(
            kind=data["kind"],
            etag=data["etag"],
            id=data["id"],
            summary=data.get("summary"),
            description=data.get("description"),
            location=data.get("location"),
            timeZone=data.get("timeZone"),
            summaryOverride=data.get("summaryOverride"),
            colorId=data.get("colorId"),
            backgroundColor=data.get("backgroundColor"),
            foregroundColor=data.get("foregroundColor"),
            hidden=data.get("hidden"),
            selected=data.get("selected"),
            accessRole=data.get("accessRole"),
            defaultReminders=default_reminders,
            notificationSettings=notification_settings,
            primary=data.get("primary"),
            deleted=data.get("deleted"),
            conferenceProperties=conference_properties
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the CalendarListEntry object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the CalendarListEntry object.
        """
        return asdict(self)
