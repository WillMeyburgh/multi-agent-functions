from datetime import datetime, timedelta
from multi_agent_functions.v1.google.calender.client import GoogleCalendarClient
from multi_agent_functions.v1.google.calender.model.events import Event

def main():
    client = GoogleCalendarClient()

    # Calculate tomorrow's date
    tomorrow = datetime.now() + timedelta(days=1)
    
    # Set time range for tomorrow at 12 PM
    time_min = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 12, 0, 0).isoformat() + 'Z'
    time_max = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 13, 0, 0).isoformat() + 'Z'

    print(f"Searching for meetings tomorrow between 12:00 PM and 1:00 PM UTC...")
    
    # Get meetings for tomorrow at 12 PM
    events = client.events_list(timeMin=time_min, timeMax=time_max)

    if not events:
        print("No meetings found for tomorrow at 12 PM.")
        return

    # Assuming the first found event is the one to move
    event_to_move = events[0]
    print(f"Found event: '{event_to_move.summary}' (ID: {event_to_move.id})")
    print(f"Current start time: {event_to_move.start.date_time if event_to_move.start.date_time else event_to_move.start.date}")
    print(f"Current end time: {event_to_move.end.date_time if event_to_move.end.date_time else event_to_move.end.date}")

    # Move the event forward by one hour
    # Ensure we are working with dateTime, as per the problem description (meeting at 12 PM)
    if event_to_move.start.date_time and event_to_move.end.date_time:
        updated_start_time = event_to_move.start.date_time + timedelta(hours=1)
        updated_end_time = event_to_move.end.date_time + timedelta(hours=1)
    else:
        print("Event does not have a dateTime, cannot move.")
        return

    event_body = {
        'start': {
            'dateTime': updated_start_time.isoformat(),
            'timeZone': event_to_move.start.time_zone if event_to_move.start.time_zone else 'UTC',
        },
        'end': {
            'dateTime': updated_end_time.isoformat(),
            'timeZone': event_to_move.end.time_zone if event_to_move.end.time_zone else 'UTC',
        },
    }

    print(f"Attempting to move event to new start time: {updated_start_time.isoformat()}")
    
    updated_event = client.events_update(
        calendar_id='primary',
        event_id=event_to_move.id,
        body=event_body
    )

    if updated_event:
        print(f"Event '{updated_event.summary}' successfully moved.")
        print(f"New start time: {updated_event.start.date_time if updated_event.start.date_time else updated_event.start.date}")
        print(f"New end time: {updated_event.end.date_time if updated_event.end.date_time else updated_event.end.date}")
    else:
        print("Failed to move the event.")

if __name__ == '__main__':
    main()
