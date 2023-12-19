# Imports
import os.path 
import datetime
import tkinter as tk
from collections import defaultdict
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def authorize():

    """
    Function authorizes google calendar api use
    OAuth2 is used for google api as credentials.json and token.json
    Token.json will eventuall expire and create a new one
    """

    # Your API credentials file (downloaded from the Cloud Console)
    credentials_file = '/Users/keg-macbook/MontyPython/raspi-dashboard/credentials/client_secret.json'

    # OAuth 2.0 scopes for Google Calendar
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    # Check if token file exists
    creds = None
    if os.path.exists('/Users/keg-macbook/MontyPython/raspi-dashboard/credentials/token.json'):
        creds = Credentials.from_authorized_user_file('/Users/keg-macbook/MontyPython/raspi-dashboard/credentials/token.json')

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('/Users/keg-macbook/MontyPython/raspi-dashboard/credentials/token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def get_calendar():
    # Authorize the user
    credentials = authorize()

    # Build the service
    service = build('calendar', 'v3', credentials=credentials)

    # Set start and end times for calendar API call range
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    now_plus_4_days = (datetime.datetime.utcnow() + datetime.timedelta(days=5)).isoformat() + 'Z'  # End of current day

    # Call the Calendar API
    events_result = service.events().list(calendarId='primary', timeMin=now, 
                                          timeMax=now_plus_4_days,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    # Dictionary to append all API data into
    events_dict = defaultdict(list) 

    # For loop to place all data into variables and compile variables into dictionary 
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date')) # Start date and time of event
        end = event['end'].get('dateTime', event['end'].get('date')) # End date and time of event
        summary = event['summary'] # Name of event
        
        # Parse date and time
        event_date = start.split('T')[0] # Extract date of the event
        event_time = start.split('T')[1][:5]  # Extract HH:MM from the time
    
        # Add event information to the dictionary
        events_dict[event_date].append({'start_time': event_time, 'end_time': end, 'summary': summary})

    return events_dict


def events(canvas, x1, y1, x2, y2, x3, y3, x4, y4):

    """
    Function calls Google Calendar API and creates a widget of future events for the next 4 days
    """

    # Call API
    events = get_calendar()

    # Set current date for organizing events based on days ahead of the current date
    current_date = str(datetime.datetime.now().strftime('%Y-%m-%d'))

    # Variables that contain the number of events for each
    # Empty lists to append to through for loop
    day_1 = []
    day_2 = []
    day_3 = []
    day_4 = []

    # For loop to assign event to days of the week from the API Call
    for date in events:
        if date == str(datetime.datetime.strptime(current_date, '%Y-%m-%d') + datetime.timedelta(days=1))[:10]:
            day_1.append(date)
        elif date == str(datetime.datetime.strptime(current_date, '%Y-%m-%d') + datetime.timedelta(days=2))[:10]:
            day_2.append(date)
        elif date == str(datetime.datetime.strptime(current_date, '%Y-%m-%d') + datetime.timedelta(days=3))[:10]:
            day_3.append(date)
        elif date == str(datetime.datetime.strptime(current_date, '%Y-%m-%d') + datetime.timedelta(days=4))[:10]:
            day_4.append(date)
        else:
            return KeyError
        
    # Create labels for widget
    # DAY 1
    if len(day_1) == 1:
        events1 = tk.Label(canvas, text=f'{len(day_1)} EVENT', font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#FFFFFF") # Day_1 events
    else:
        events1 = tk.Label(canvas, text=f'{len(day_1)} EVENTS', font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#FFFFFF") # Day_1 events

    # Collects information about widget
    events1_width = events1.winfo_reqwidth()
    events1_height = events1.winfo_reqheight()
    
    # Makes x and y values based on the center of the widget
    events1_x_centered = x1 - events1_width/2
    events1_y_centered = y1 - events1_height/2

    events1.place(x=events1_x_centered, y=events1_y_centered)

    # DAY 2
    if len(day_2) == 1:
        events2 = tk.Label(canvas, text=f'{len(day_2)} EVENT', font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#FFFFFF") # Day_2 events
    else:
        events2 = tk.Label(canvas, text=f'{len(day_2)} EVENTS', font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#FFFFFF") # Day_2 events

    # Collects information about widget
    events2_width = events2.winfo_reqwidth()
    events2_height = events2.winfo_reqheight()
    
    # Makes x and y values based on the center of the widget
    events2_x_centered = x2 - events2_width/2
    events2_y_centered = y2 - events2_height/2

    events2.place(x=events2_x_centered, y=events2_y_centered)

    # DAY 3
    if len(day_3) == 1:
        events3 = tk.Label(canvas, text=f'{len(day_3)} EVENT', font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#FFFFFF") # Day_3 events
    else:
        events3 = tk.Label(canvas, text=f'{len(day_3)} EVENTS', font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#FFFFFF") # Day_3 events

    # Collects information about widget
    events3_width = events3.winfo_reqwidth()
    events3_height = events3.winfo_reqheight()
    
    # Makes x and y values based on the center of the widget
    events3_x_centered = x3 - events3_width/2
    events3_y_centered = y3 - events3_height/2

    events3.place(x=events3_x_centered, y=events3_y_centered)

    # DAY 4
    if len(day_4) == 1:
        events4 = tk.Label(canvas, text=f'{len(day_4)} EVENT', font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#FFFFFF") # Day_3 events
    else:
        events4 = tk.Label(canvas, text=f'{len(day_4)} EVENTS', font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#FFFFFF") # Day_3 events

    # Collects information about widget
    events4_width = events4.winfo_reqwidth()
    events4_height = events4.winfo_reqheight()
    
    # Makes x and y values based on the center of the widget
    events4_x_centered = x4 - events4_width/2
    events4_y_centered = y4 - events4_height/2

    events4.place(x=events4_x_centered, y=events4_y_centered)

    # UPDATE FUNCTION

    return events1, events2, events3, events4
