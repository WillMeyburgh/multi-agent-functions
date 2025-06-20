from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from typing import List, Optional, Dict, Any

def _parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
    if dt_str:
        try:
            return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        except ValueError:
            # Handle cases where timezone info might be missing or malformed
            return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")
    return None

def _parse_date(date_str: Optional[str]) -> Optional[date]:
    if date_str:
        return date.fromisoformat(date_str)
    return None

@dataclass(frozen=True)
class Creator:
    id: Optional[str] = None
    email: Optional[str] = None
    display_name: Optional[str] = None
    self: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['Creator']:
        """
        Creates a Creator object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing creator data with the following keys:
                - 'id' (str, optional): The creator's ID, if available.
                - 'email' (str, optional): The creator's email address.
                - 'displayName' (str, optional): The creator's name, if available.
                - 'self' (bool, optional): Whether the creator corresponds to the calendar owner.

        Returns:
            Optional[Creator]: A Creator object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(
            id=data.get('id'),
            email=data.get('email'),
            display_name=data.get('displayName'),
            self=data.get('self')
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Creator object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the Creator object.
        """
        return asdict(self)

@dataclass(frozen=True)
class Organizer:
    id: Optional[str] = None
    email: Optional[str] = None
    display_name: Optional[str] = None
    self: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['Organizer']:
        """
        Creates an Organizer object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing organizer data with the following keys:
                - 'id' (str, optional): The organizer's ID, if available.
                - 'email' (str, optional): The organizer's email address.
                - 'displayName' (str, optional): The organizer's name, if available.
                - 'self' (bool, optional): Whether the organizer corresponds to the calendar owner.

        Returns:
            Optional[Organizer]: An Organizer object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(
            id=data.get('id'),
            email=data.get('email'),
            display_name=data.get('displayName'),
            self=data.get('self')
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Organizer object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the Organizer object.
        """
        return asdict(self)

@dataclass(frozen=True)
class EventDateTime:
    date: Optional[date] = None
    date_time: Optional[datetime] = None
    time_zone: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['EventDateTime']:
        """
        Creates an EventDateTime object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing event date/time data with the following keys:
                - 'date' (str, optional): The date, in the format "yyyy-mm-dd".
                - 'dateTime' (str, optional): The date-time, as a string in RFC3339 format.
                - 'timeZone' (str, optional): The time zone in which the time is specified.

        Returns:
            Optional[EventDateTime]: An EventDateTime object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(
            date=_parse_date(data.get('date')),
            date_time=_parse_datetime(data.get('dateTime')),
            time_zone=data.get('timeZone')
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the EventDateTime object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the EventDateTime object.
        """
        result = asdict(self)
        if self.date_time:
            result['dateTime'] = self.date_time.isoformat()
        if self.date:
            result['date'] = self.date.isoformat()
        return result

@dataclass(frozen=True)
class Attendee:
    id: Optional[str] = None
    email: Optional[str] = None
    display_name: Optional[str] = None
    organizer: Optional[bool] = None
    self: Optional[bool] = None
    resource: Optional[bool] = None
    optional: Optional[bool] = None
    response_status: Optional[str] = None
    comment: Optional[str] = None
    additional_guests: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['Attendee']:
        """
        Creates an Attendee object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing attendee data with the following keys:
                - 'id' (str, optional): The attendee's ID, if available.
                - 'email' (str, optional): The attendee's email address.
                - 'displayName' (str, optional): The attendee's name, if available.
                - 'organizer' (bool, optional): Whether this is the organizer of the event.
                - 'self' (bool, optional): Whether this is the calendar owner's attendee entry.
                - 'resource' (bool, optional): Whether this is a resource attendee.
                - 'optional' (bool, optional): Whether the attendee is optional.
                - 'responseStatus' (str, optional): The attendee's response status. Can be "needsAction", "declined", "tentative", or "accepted".
                - 'comment' (str, optional): The attendee's comment.
                - 'additionalGuests' (int, optional): The number of additional guests for this attendee.

        Returns:
            Optional[Attendee]: An Attendee object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(
            id=data.get('id'),
            email=data.get('email'),
            display_name=data.get('displayName'),
            organizer=data.get('organizer'),
            self=data.get('self'),
            resource=data.get('resource'),
            optional=data.get('optional'),
            response_status=data.get('responseStatus'),
            comment=data.get('comment'),
            additional_guests=data.get('additionalGuests')
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Attendee object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the Attendee object.
        """
        return asdict(self)

@dataclass(frozen=True)
class ExtendedProperties:
    private: Optional[Dict[str, str]] = None
    shared: Optional[Dict[str, str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['ExtendedProperties']:
        """
        Creates an ExtendedProperties object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing extended properties data with the following keys:
                - 'private' (Dict[str, str], optional): A dictionary of private extended properties.
                - 'shared' (Dict[str, str], optional): A dictionary of shared extended properties.

        Returns:
            Optional[ExtendedProperties]: An ExtendedProperties object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(
            private=data.get('private'),
            shared=data.get('shared')
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ExtendedProperties object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the ExtendedProperties object.
        """
        return asdict(self)

@dataclass(frozen=True)
class ConferenceSolutionKey:
    type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['ConferenceSolutionKey']:
        """
        Creates a ConferenceSolutionKey object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing conference solution key data with the following keys:
                - 'type' (str, optional): The conference solution type.

        Returns:
            Optional[ConferenceSolutionKey]: A ConferenceSolutionKey object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(type=data.get('type'))

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ConferenceSolutionKey object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the ConferenceSolutionKey object.
        """
        return asdict(self)

@dataclass(frozen=True)
class ConferenceSolution:
    key: Optional[ConferenceSolutionKey] = None
    name: Optional[str] = None
    icon_uri: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['ConferenceSolution']:
        """
        Creates a ConferenceSolution object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing conference solution data with the following keys:
                - 'key' (Dict[str, Any], optional): The key of the conference solution.
                - 'name' (str, optional): The name of the conference solution.
                - 'iconUri' (str, optional): The icon URI of the conference solution.

        Returns:
            Optional[ConferenceSolution]: A ConferenceSolution object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(
            key=ConferenceSolutionKey.from_dict(data.get('key', {})),
            name=data.get('name'),
            icon_uri=data.get('iconUri')
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ConferenceSolution object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the ConferenceSolution object.
        """
        return asdict(self)

@dataclass(frozen=True)
class ConferenceRequestStatus:
    status_code: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['ConferenceRequestStatus']:
        """
        Creates a ConferenceRequestStatus object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing conference request status data with the following keys:
                - 'statusCode' (str, optional): The status code of the conference request.

        Returns:
            Optional[ConferenceRequestStatus]: A ConferenceRequestStatus object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(status_code=data.get('statusCode'))

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ConferenceRequestStatus object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the ConferenceRequestStatus object.
        """
        return asdict(self)

@dataclass(frozen=True)
class CreateConferenceRequest:
    request_id: Optional[str] = None
    conference_solution_key: Optional[ConferenceSolutionKey] = None
    status: Optional[ConferenceRequestStatus] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['CreateConferenceRequest']:
        """
        Creates a CreateConferenceRequest object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing create conference request data with the following keys:
                - 'requestId' (str, optional): The request ID.
                - 'conferenceSolutionKey' (Dict[str, Any], optional): The conference solution key.
                - 'status' (Dict[str, Any], optional): The status of the conference request.

        Returns:
            Optional[CreateConferenceRequest]: A CreateConferenceRequest object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(
            request_id=data.get('requestId'),
            conference_solution_key=ConferenceSolutionKey.from_dict(data.get('conferenceSolutionKey', {})),
            status=ConferenceRequestStatus.from_dict(data.get('status', {}))
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the CreateConferenceRequest object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the CreateConferenceRequest object.
        """
        return asdict(self)

@dataclass(frozen=True)
class EntryPoint:
    entry_point_type: Optional[str] = None
    uri: Optional[str] = None
    label: Optional[str] = None
    pin: Optional[str] = None
    access_code: Optional[str] = None
    meeting_code: Optional[str] = None
    passcode: Optional[str] = None
    password: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['EntryPoint']:
        """
        Creates an EntryPoint object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing entry point data with the following keys:
                - 'entryPointType' (str, optional): The type of entry point.
                - 'uri' (str, optional): The URI of the entry point.
                - 'label' (str, optional): The label of the entry point.
                - 'pin' (str, optional): The PIN code for the entry point.
                - 'accessCode' (str, optional): The access code for the entry point.
                - 'meetingCode' (str, optional): The meeting code for the entry point.
                - 'passcode' (str, optional): The passcode for the entry point.
                - 'password' (str, optional): The password for the entry point.

        Returns:
            Optional[EntryPoint]: An EntryPoint object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(
            entry_point_type=data.get('entryPointType'),
            uri=data.get('uri'),
            label=data.get('label'),
            pin=data.get('pin'),
            access_code=data.get('accessCode'),
            meeting_code=data.get('meetingCode'),
            passcode=data.get('passcode'),
            password=data.get('password')
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the EntryPoint object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the EntryPoint object.
        """
        return asdict(self)

@dataclass(frozen=True)
class ConferenceData:
    create_request: Optional[CreateConferenceRequest] = None
    entry_points: Optional[List[EntryPoint]] = field(default_factory=list)
    conference_solution: Optional[ConferenceSolution] = None
    conference_id: Optional[str] = None
    signature: Optional[str] = None
    notes: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['ConferenceData']:
        """
        Creates a ConferenceData object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing conference data with the following keys:
                - 'createRequest' (Dict[str, Any], optional): The create conference request.
                - 'entryPoints' (List[Dict[str, Any]], optional): The entry points for the conference.
                - 'conferenceSolution' (Dict[str, Any], optional): The conference solution.
                - 'conferenceId' (str, optional): The conference ID.
                - 'signature' (str, optional): The signature of the conference data.
                - 'notes' (str, optional): Additional notes for the conference.

        Returns:
            Optional[ConferenceData]: A ConferenceData object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(
            create_request=CreateConferenceRequest.from_dict(data.get('createRequest', {})),
            entry_points=[EntryPoint.from_dict(ep) for ep in data.get('entryPoints', []) if ep] if data.get('entryPoints') else None,
            conference_solution=ConferenceSolution.from_dict(data.get('conferenceSolution', {})),
            conference_id=data.get('conferenceId'),
            signature=data.get('signature'),
            notes=data.get('notes')
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ConferenceData object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the ConferenceData object.
        """
        return asdict(self)

@dataclass(frozen=True)
class Gadget:
    type: Optional[str] = None
    title: Optional[str] = None
    link: Optional[str] = None
    icon_link: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    display: Optional[str] = None
    preferences: Optional[Dict[str, str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['Gadget']:
        """
        Creates a Gadget object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing gadget data with the following keys:
                - 'type' (str, optional): The type of the gadget.
                - 'title' (str, optional): The title of the gadget.
                - 'link' (str, optional): The link to the gadget.
                - 'iconLink' (str, optional): The icon link of the gadget.
                - 'width' (int, optional): The width of the gadget.
                - 'height' (int, optional): The height of the gadget.
                - 'display' (str, optional): The display mode of the gadget.
                - 'preferences' (Dict[str, str], optional): The preferences of the gadget.

        Returns:
            Optional[Gadget]: A Gadget object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(
            type=data.get('type'),
            title=data.get('title'),
            link=data.get('link'),
            icon_link=data.get('iconLink'),
            width=data.get('width'),
            height=data.get('height'),
            display=data.get('display'),
            preferences=data.get('preferences')
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Gadget object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the Gadget object.
        """
        return asdict(self)

@dataclass(frozen=True)
class ReminderOverride:
    method: Optional[str] = None
    minutes: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['ReminderOverride']:
        """
        Creates a ReminderOverride object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing reminder override data with the following keys:
                - 'method' (str, optional): The method used by this reminder. Possible values are "email", "sms", or "popup".
                - 'minutes' (int, optional): The number of minutes before the start of the event when the reminder should trigger.

        Returns:
            Optional[ReminderOverride]: A ReminderOverride object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(
            method=data.get('method'),
            minutes=data.get('minutes')
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ReminderOverride object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the ReminderOverride object.
        """
        return asdict(self)

@dataclass(frozen=True)
class Reminders:
    use_default: Optional[bool] = None
    overrides: Optional[List[ReminderOverride]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['Reminders']:
        """
        Creates a Reminders object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing reminders data with the following keys:
                - 'useDefault' (bool, optional): Whether the default reminders of the calendar apply to this event.
                - 'overrides' (List[Dict[str, Any]], optional): If 'useDefault' is false, this specifies the reminders that apply to the event.

        Returns:
            Optional[Reminders]: A Reminders object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(
            use_default=data.get('useDefault'),
            overrides=[ReminderOverride.from_dict(ro) for ro in data.get('overrides', []) if ro] if data.get('overrides') else None
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Reminders object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the Reminders object.
        """
        return asdict(self)

@dataclass(frozen=True)
class Source:
    url: Optional[str] = None
    title: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['Source']:
        """
        Creates a Source object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing source data with the following keys:
                - 'url' (str, optional): The URL of the source.
                - 'title' (str, optional): The title of the source.

        Returns:
            Optional[Source]: A Source object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(
            url=data.get('url'),
            title=data.get('title')
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Source object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the Source object.
        """
        return asdict(self)

@dataclass(frozen=True)
class WorkingLocationCustomLocation:
    label: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['WorkingLocationCustomLocation']:
        """
        Creates a WorkingLocationCustomLocation object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing working location custom location data with the following keys:
                - 'label' (str, optional): The label of the custom working location.

        Returns:
            Optional[WorkingLocationCustomLocation]: A WorkingLocationCustomLocation object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(label=data.get('label'))

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the WorkingLocationCustomLocation object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the WorkingLocationCustomLocation object.
        """
        return asdict(self)

@dataclass(frozen=True)
class WorkingLocationOfficeLocation:
    building_id: Optional[str] = None
    floor_id: Optional[str] = None
    floor_section_id: Optional[str] = None
    desk_id: Optional[str] = None
    label: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['WorkingLocationOfficeLocation']:
        """
        Creates a WorkingLocationOfficeLocation object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing working location office location data with the following keys:
                - 'buildingId' (str, optional): The building ID.
                - 'floorId' (str, optional): The floor ID.
                - 'floorSectionId' (str, optional): The floor section ID.
                - 'deskId' (str, optional): The desk ID.
                - 'label' (str, optional): The label of the office location.

        Returns:
            Optional[WorkingLocationOfficeLocation]: A WorkingLocationOfficeLocation object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(
            building_id=data.get('buildingId'),
            floor_id=data.get('floorId'),
            floor_section_id=data.get('floorSectionId'),
            desk_id=data.get('deskId'),
            label=data.get('label')
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the WorkingLocationOfficeLocation object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the WorkingLocationOfficeLocation object.
        """
        return asdict(self)

@dataclass(frozen=True)
class WorkingLocationProperties:
    type: Optional[str] = None
    home_office: Optional[Any] = None # Value can be anything, typically empty object
    custom_location: Optional[WorkingLocationCustomLocation] = None
    office_location: Optional[WorkingLocationOfficeLocation] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['WorkingLocationProperties']:
        """
        Creates a WorkingLocationProperties object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing working location properties data with the following keys:
                - 'type' (str, optional): The type of working location.
                - 'homeOffice' (Any, optional): Home office properties.
                - 'customLocation' (Dict[str, Any], optional): Custom location properties.
                - 'officeLocation' (Dict[str, Any], optional): Office location properties.

        Returns:
            Optional[WorkingLocationProperties]: A WorkingLocationProperties object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(
            type=data.get('type'),
            home_office=data.get('homeOffice'),
            custom_location=WorkingLocationCustomLocation.from_dict(data.get('customLocation', {})),
            office_location=WorkingLocationOfficeLocation.from_dict(data.get('officeLocation', {}))
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the WorkingLocationProperties object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the WorkingLocationProperties object.
        """
        return asdict(self)

@dataclass(frozen=True)
class OutOfOfficeProperties:
    auto_decline_mode: Optional[str] = None
    decline_message: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['OutOfOfficeProperties']:
        """
        Creates an OutOfOfficeProperties object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing out of office properties data with the following keys:
                - 'autoDeclineMode' (str, optional): The auto decline mode.
                - 'declineMessage' (str, optional): The decline message.

        Returns:
            Optional[OutOfOfficeProperties]: An OutOfOfficeProperties object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(
            auto_decline_mode=data.get('autoDeclineMode'),
            decline_message=data.get('declineMessage')
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the OutOfOfficeProperties object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the OutOfOfficeProperties object.
        """
        return asdict(self)

@dataclass(frozen=True)
class FocusTimeProperties:
    auto_decline_mode: Optional[str] = None
    decline_message: Optional[str] = None
    chat_status: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['FocusTimeProperties']:
        """
        Creates a FocusTimeProperties object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing focus time properties data with the following keys:
                - 'autoDeclineMode' (str, optional): The auto decline mode.
                - 'declineMessage' (str, optional): The decline message.
                - 'chatStatus' (str, optional): The chat status.

        Returns:
            Optional[FocusTimeProperties]: A FocusTimeProperties object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(
            auto_decline_mode=data.get('autoDeclineMode'),
            decline_message=data.get('declineMessage'),
            chat_status=data.get('chatStatus')
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the FocusTimeProperties object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the FocusTimeProperties object.
        """
        return asdict(self)

@dataclass(frozen=True)
class Attachment:
    file_url: Optional[str] = None
    title: Optional[str] = None
    mime_type: Optional[str] = None
    icon_link: Optional[str] = None
    file_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['Attachment']:
        """
        Creates an Attachment object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing attachment data with the following keys:
                - 'fileUrl' (str, optional): The URL of the attachment.
                - 'title' (str, optional): The title of the attachment.
                - 'mimeType' (str, optional): The MIME type of the attachment.
                - 'iconLink' (str, optional): The icon link of the attachment.
                - 'fileId' (str, optional): The ID of the attachment file.

        Returns:
            Optional[Attachment]: An Attachment object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(
            file_url=data.get('fileUrl'),
            title=data.get('title'),
            mime_type=data.get('mimeType'),
            icon_link=data.get('iconLink'),
            file_id=data.get('fileId')
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Attachment object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the Attachment object.
        """
        return asdict(self)

@dataclass(frozen=True)
class BirthdayProperties:
    contact: Optional[str] = None
    type: Optional[str] = None
    custom_type_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['BirthdayProperties']:
        """
        Creates a BirthdayProperties object from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing birthday properties data with the following keys:
                - 'contact' (str, optional): The contact ID of the birthday.
                - 'type' (str, optional): The type of birthday.
                - 'customTypeName' (str, optional): The custom type name of the birthday.

        Returns:
            Optional[BirthdayProperties]: A BirthdayProperties object populated with the provided data, or None if data is empty.
        """
        if not data:
            return None
        return cls(
            contact=data.get('contact'),
            type=data.get('type'),
            custom_type_name=data.get('customTypeName')
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the BirthdayProperties object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the BirthdayProperties object.
        """
        return asdict(self)

@dataclass(frozen=True)
class Event:
    kind: Optional[str] = None
    etag: Optional[str] = None
    id: Optional[str] = None
    status: Optional[str] = None
    html_link: Optional[str] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    color_id: Optional[str] = None
    creator: Optional[Creator] = None
    organizer: Optional[Organizer] = None
    start: Optional[EventDateTime] = None
    end: Optional[EventDateTime] = None
    end_time_unspecified: Optional[bool] = None
    recurrence: Optional[List[str]] = field(default_factory=list)
    recurring_event_id: Optional[str] = None
    original_start_time: Optional[EventDateTime] = None
    transparency: Optional[str] = None
    visibility: Optional[str] = None
    i_cal_uid: Optional[str] = None
    sequence: Optional[int] = None
    attendees: Optional[List[Attendee]] = field(default_factory=list)
    attendees_omitted: Optional[bool] = None
    extended_properties: Optional[ExtendedProperties] = None
    hangout_link: Optional[str] = None
    conference_data: Optional[ConferenceData] = None
    gadget: Optional[Gadget] = None
    anyone_can_add_self: Optional[bool] = None
    guests_can_invite_others: Optional[bool] = None
    guests_can_modify: Optional[bool] = None
    guests_can_see_other_guests: Optional[bool] = None
    private_copy: Optional[bool] = None
    locked: Optional[bool] = None
    reminders: Optional[Reminders] = None
    source: Optional[Source] = None
    working_location_properties: Optional[WorkingLocationProperties] = None
    out_of_office_properties: Optional[OutOfOfficeProperties] = None
    focus_time_properties: Optional[FocusTimeProperties] = None
    attachments: Optional[List[Attachment]] = field(default_factory=list)
    birthday_properties: Optional[BirthdayProperties] = None
    event_type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        """
        Creates an Event object from a dictionary, typically received from the Google Calendar API.

        Args:
            data (Dict[str, Any]): A dictionary containing event data with the following keys:
                - 'kind' (str, optional): Type of the resource. Value is always "calendar#event".
                - 'etag' (str, optional): ETag of the resource.
                - 'id' (str, optional): Opaque identifier of the event.
                - 'status' (str, optional): Status of the event. Can be "confirmed", "tentative", or "cancelled".
                - 'htmlLink' (str, optional): An absolute link to the Google Calendar Web UI.
                - 'created' (str, optional): Creation time of the event (RFC3339 timestamp).
                - 'updated' (str, optional): Last modification time of the event (RFC3339 timestamp).
                - 'summary' (str, optional): Title of the event.
                - 'description' (str, optional): Description of the event.
                - 'location' (str, optional): Geographic location of the event.
                - 'colorId' (str, optional): The color of the event.
                - 'creator' (Dict[str, Any], optional): The creator of the event.
                - 'organizer' (Dict[str, Any], optional): The organizer of the event.
                - 'start' (Dict[str, Any], optional): The start time of the event.
                - 'end' (Dict[str, Any], optional): The end time of the event.
                - 'endTimeUnspecified' (bool, optional): Whether the end time is unspecified.
                - 'recurrence' (List[str], optional): List of RRULE, RDATE, EXRULE, or EXDATE strings.
                - 'recurringEventId' (str, optional): For an instance of a recurring event, this is the id of the recurring event master.
                - 'originalStartTime' (Dict[str, Any], optional): For an instance of a recurring event, this is the time at which this event would start according to the recurrence rule.
                - 'transparency' (str, optional): Whether the event blocks time on the calendar. Can be "opaque" or "transparent".
                - 'visibility' (str, optional): Visibility of the event. Can be "default", "public", "private", or "confidential".
                - 'iCalUID' (str, optional): Opaque calendar unique ID.
                - 'sequence' (int, optional): Sequence number as per iCalendar.
                - 'attendees' (List[Dict[str, Any]], optional): The attendees of the event.
                - 'attendeesOmitted' (bool, optional): Whether the list of attendees is omitted.
                - 'extendedProperties' (Dict[str, Any], optional): Extended properties of the event.
                - 'hangoutLink' (str, optional): The URL of the hangout.
                - 'conferenceData' (Dict[str, Any], optional): The conference data for the event.
                - 'gadget' (Dict[str, Any], optional): A gadget that extends the event.
                - 'anyoneCanAddSelf' (bool, optional): Whether anyone can add themselves to the event.
                - 'guestsCanInviteOthers' (bool, optional): Whether guests can invite other guests.
                - 'guestsCanModify' (bool, optional): Whether guests can modify the event.
                - 'guestsCanSeeOtherGuests' (bool, optional): Whether guests can see other guests.
                - 'privateCopy' (bool, optional): Whether this is a private copy of a public event.
                - 'locked' (bool, optional): Whether the event is locked.
                - 'reminders' (Dict[str, Any], optional): Information about the event's reminders.
                - 'source' (Dict[str, Any], optional): Source from which the event was created.
                - 'workingLocationProperties' (Dict[str, Any], optional): Working location properties.
                - 'outOfOfficeProperties' (Dict[str, Any], optional): Out of office properties.
                - 'focusTimeProperties' (Dict[str, Any], optional): Focus time properties.
                - 'attachments' (List[Dict[str, Any]], optional): Attachments for the event.
                - 'birthdayProperties' (Dict[str, Any], optional): Birthday properties.
                - 'eventType' (str, optional): The type of the event.

        Returns:
            Event: An Event object populated with the provided data.
        """
        return cls(
            kind=data.get('kind'),
            etag=data.get('etag'),
            id=data.get('id'),
            status=data.get('status'),
            html_link=data.get('htmlLink'),
            created=_parse_datetime(data.get('created')),
            updated=_parse_datetime(data.get('updated')),
            summary=data.get('summary'),
            description=data.get('description'),
            location=data.get('location'),
            color_id=data.get('colorId'),
            creator=Creator.from_dict(data.get('creator', {})),
            organizer=Organizer.from_dict(data.get('organizer', {})),
            start=EventDateTime.from_dict(data.get('start', {})),
            end=EventDateTime.from_dict(data.get('end', {})),
            end_time_unspecified=data.get('endTimeUnspecified'),
            recurrence=data.get('recurrence'),
            recurring_event_id=data.get('recurringEventId'),
            original_start_time=EventDateTime.from_dict(data.get('originalStartTime', {})),
            transparency=data.get('transparency'),
            visibility=data.get('visibility'),
            i_cal_uid=data.get('iCalUID'),
            sequence=data.get('sequence'),
            attendees=[Attendee.from_dict(att) for att in data.get('attendees', []) if att] if data.get('attendees') else None,
            attendees_omitted=data.get('attendeesOmitted'),
            extended_properties=ExtendedProperties.from_dict(data.get('extendedProperties', {})),
            hangout_link=data.get('hangoutLink'),
            conference_data=ConferenceData.from_dict(data.get('conferenceData', {})),
            gadget=Gadget.from_dict(data.get('gadget', {})),
            anyone_can_add_self=data.get('anyoneCanAddSelf'),
            guests_can_invite_others=data.get('guestsCanInviteOthers'),
            guests_can_modify=data.get('guestsCanModify'),
            guests_can_see_other_guests=data.get('guestsCanSeeOtherGuests'),
            private_copy=data.get('privateCopy'),
            locked=data.get('locked'),
            reminders=Reminders.from_dict(data.get('reminders', {})),
            source=Source.from_dict(data.get('source', {})),
            working_location_properties=WorkingLocationProperties.from_dict(data.get('workingLocationProperties', {})),
            out_of_office_properties=OutOfOfficeProperties.from_dict(data.get('outOfOfficeProperties', {})),
            focus_time_properties=FocusTimeProperties.from_dict(data.get('focusTimeProperties', {})),
            attachments=[Attachment.from_dict(att) for att in data.get('attachments', []) if att] if data.get('attachments') else None,
            birthday_properties=BirthdayProperties.from_dict(data.get('birthdayProperties', {})),
            event_type=data.get('eventType')
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Event object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the Event object.
        """
        result = asdict(self)
        if self.created:
            result['created'] = self.created.isoformat()
        if self.updated:
            result['updated'] = self.updated.isoformat()
        if self.start:
            result['start'] = self.start.to_dict()
        if self.end:
            result['end'] = self.end.to_dict()
        if self.original_start_time:
            result['originalStartTime'] = self.original_start_time.to_dict()
        if self.creator:
            result['creator'] = self.creator.to_dict()
        if self.organizer:
            result['organizer'] = self.organizer.to_dict()
        if self.attendees:
            result['attendees'] = [att.to_dict() for att in self.attendees]
        if self.extended_properties:
            result['extendedProperties'] = self.extended_properties.to_dict()
        if self.conference_data:
            result['conferenceData'] = self.conference_data.to_dict()
        if self.gadget:
            result['gadget'] = self.gadget.to_dict()
        if self.reminders:
            result['reminders'] = self.reminders.to_dict()
        if self.source:
            result['source'] = self.source.to_dict()
        if self.working_location_properties:
            result['workingLocationProperties'] = self.working_location_properties.to_dict()
        if self.out_of_office_properties:
            result['outOfOfficeProperties'] = self.out_of_office_properties.to_dict()
        if self.focus_time_properties:
            result['focusTimeProperties'] = self.focus_time_properties.to_dict()
        if self.attachments:
            result['attachments'] = [att.to_dict() for att in self.attachments]
        if self.birthday_properties:
            result['birthdayProperties'] = self.birthday_properties.to_dict()
        return result
