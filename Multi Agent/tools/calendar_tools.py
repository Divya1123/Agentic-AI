from langchain.tools import tool
from datetime import datetime

# in-memory calendar
EVENTS = []

@tool
def add_event(event:str):
    """
    This function adds a calendar event.
    Formt: "Meeting with John at 3pm on 22nd Nov, 2025"
    """
    EVENTS.append({
        "event": event,
        "created_on": datetime.now().isoformat()
    })
    return f'Event added {event}'

@tool
def view_events():
    """
    Return all stored calendar events.
    """
    if not EVENTS:
        return "No events to show"
    
    events = []
    for e in EVENTS:
        events = events.append(f'{e['event']} created on {e['created_on']}')
    
    return '\n'.join(events)