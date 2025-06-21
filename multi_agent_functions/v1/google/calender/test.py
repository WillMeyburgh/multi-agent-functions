from datetime import datetime, timedelta
from multi_agent_functions.v1.google.calender.client import GoogleCalendarClient
from multi_agent_functions.v1.google.calender.model.events import Event
def main():
    client = GoogleCalendarClient()

    # Calculate tomorrow's date
    tomorrow = datetime.now() + timedelta(days=1)
    
    # Define event times for 9 AM to 10 AM in Africa/Johannesburg
    start_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 9, 0, 0)
    end_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 10, 0, 0)
    
    summary = "Test Event 9 AM SAST"
    description = "This event is created to test the timezone fix for Google Calendar."
    
    event_body = {
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Africa/Johannesburg',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Africa/Johannesburg',
        },
        'summary': summary,
        'description': description,
    }

    print(f"Attempting to create event: '{summary}' for tomorrow at 9 AM SAST...")
    
    created_event = client.events_insert(
        calendar_id='primary',
        summary=summary,
        start=event_body['start'],
        end=event_body['end'],
        description=description
    )

    if created_event:
        print(f"Event '{created_event.summary}' successfully created.")
        print(f"Created event ID: {created_event.id}")
        print(f"Start time: {created_event.start.date_time} (Time Zone: {created_event.start.time_zone})")
        print(f"End time: {created_event.end.date_time} (Time Zone: {created_event.end.time_zone})")
        print("\nPlease check your Google Calendar to confirm this event appears correctly at 9 AM local time (Africa/Johannesburg).")
    else:
        print("Failed to create the event.")

if __name__ == '__main__':
    main()
