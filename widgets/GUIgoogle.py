# Imports
import os.path 
import datetime
import random
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
    Token.json will eventually expire and create a new one
    """

    # Your API credentials file (downloaded from the Cloud Console)
    credentials_file = '~/Raspi-Dashboard-0.1.2-alpha/credentials/client_secret.json'

    # OAuth 2.0 scopes for Google Calendar
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    # Check if token file exists
    creds = None
    if os.path.exists('~/Raspi-Dashboard-0.1.2-alpha/credentials/token.json'):
        creds = Credentials.from_authorized_user_file('~/Raspi-Dashboard-0.1.2-alpha/credentials/token.json')

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                creds = None

        if not creds:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print(f"Error running local server: {e}")
                creds = None

        # Save the credentials for the next run
        if creds:
            with open('~/Raspi-Dashboard-0.1.2-alpha/credentials/token.json', 'w') as token:
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
        event_stime = start.split('T')[1][:5]  # Extract HH:MM from the time
        event_etime = end.split('T')[1][:5]

        # Add event information to the dictionary
        events_dict[event_date].append({'start_time': event_stime, 'end_time': event_etime, 'summary': summary})

    return events_dict
 

def events(canvas, x1, y1, x2, y2, x3, y3, x4, y4):

    """
    Function calls Google Calendar API and creates a widget of future events for the next 4 days
    """
   
    # Call API
    events = get_calendar()
    #print(events)

    # Set current date for organizing events based on days ahead of the current date
    current_date = str(datetime.datetime.now().strftime('%Y-%m-%d'))

    # Variables that contain the number of events for each
    # Empty lists to append to through for loop
    day_1 = []
    day_2 = []
    day_3 = []
    day_4 = []

    # For loop to assign event to days of the week from the API Call
    for date, event_list in events.items():
        if date == str(datetime.datetime.strptime(current_date, '%Y-%m-%d') + datetime.timedelta(days=1))[:10]:
            day_1.extend(event_list)
        elif date == str(datetime.datetime.strptime(current_date, '%Y-%m-%d') + datetime.timedelta(days=2))[:10]:
            day_2.extend(event_list)
        elif date == str(datetime.datetime.strptime(current_date, '%Y-%m-%d') + datetime.timedelta(days=3))[:10]:
            day_3.extend(event_list)
        elif date == str(datetime.datetime.strptime(current_date, '%Y-%m-%d') + datetime.timedelta(days=4))[:10]:
            day_4.extend(event_list)
        else:
            pass
        
    # Create labels for widget
    # DAY 1
    if len(day_1) == 1:
        events1 = tk.Label(canvas, text=f'{len(day_1)} EVENT', font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#A9A9A9") # Day_1 events
    else:
        events1 = tk.Label(canvas, text=f'{len(day_1)} EVENTS', font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#A9A9A9") # Day_1 events

    # Collects information about widget
    events1_width = events1.winfo_reqwidth()
    events1_height = events1.winfo_reqheight()
    
    # Makes x and y values based on the center of the widget
    events1_x_centered = x1 - events1_width/2
    events1_y_centered = y1 - events1_height/2

    events1.place(x=events1_x_centered, y=events1_y_centered)

    # DAY 2
    if len(day_2) == 1:
        events2 = tk.Label(canvas, text=f'{len(day_2)} EVENT', font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#A9A9A9") # Day_2 events
    else:
        events2 = tk.Label(canvas, text=f'{len(day_2)} EVENTS', font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#A9A9A9") # Day_2 events

    # Collects information about widget
    events2_width = events2.winfo_reqwidth()
    events2_height = events2.winfo_reqheight()
    
    # Makes x and y values based on the center of the widget
    events2_x_centered = x2 - events2_width/2
    events2_y_centered = y2 - events2_height/2

    events2.place(x=events2_x_centered, y=events2_y_centered)

    # DAY 3
    if len(day_3) == 1:
        events3 = tk.Label(canvas, text=f'{len(day_3)} EVENT', font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#A9A9A9") # Day_3 events
    else:
        events3 = tk.Label(canvas, text=f'{len(day_3)} EVENTS', font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#A9A9A9") # Day_3 events

    # Collects information about widget
    events3_width = events3.winfo_reqwidth()
    events3_height = events3.winfo_reqheight()
    
    # Makes x and y values based on the center of the widget
    events3_x_centered = x3 - events3_width/2
    events3_y_centered = y3 - events3_height/2

    events3.place(x=events3_x_centered, y=events3_y_centered)

    # DAY 4
    if len(day_4) == 1:
        events4 = tk.Label(canvas, text=f'{len(day_4)} EVENT', font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#A9A9A9") # Day_3 events
    else:
        events4 = tk.Label(canvas, text=f'{len(day_4)} EVENTS', font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#A9A9A9") # Day_3 events

    # Collects information about widget
    events4_width = events4.winfo_reqwidth()
    events4_height = events4.winfo_reqheight()
    
    # Makes x and y values based on the center of the widget
    events4_x_centered = x4 - events4_width/2
    events4_y_centered = y4 - events4_height/2

    events4.place(x=events4_x_centered, y=events4_y_centered)

    # UPDATE FUNCTION
    update_events(canvas, events1, x1, y1, events2, x2, y2, events3, x3, y3, events4, x4, y4)

    return events1, events2, events3, events4
    

def update_events(canvas, events1, x1, y1, events2, x2, y2, events3, x3, y3, events4, x4, y4):

    """
    Function will update the events google calendar API call
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
    for date, event_list in events.items():
        if date == str(datetime.datetime.strptime(current_date, '%Y-%m-%d') + datetime.timedelta(days=1))[:10]:
            day_1.extend(event_list)
        elif date == str(datetime.datetime.strptime(current_date, '%Y-%m-%d') + datetime.timedelta(days=2))[:10]:
            day_2.extend(event_list)
        elif date == str(datetime.datetime.strptime(current_date, '%Y-%m-%d') + datetime.timedelta(days=3))[:10]:
            day_3.extend(event_list)
        elif date == str(datetime.datetime.strptime(current_date, '%Y-%m-%d') + datetime.timedelta(days=4))[:10]:
            day_4.extend(event_list)
        else:
            pass
    
    # Assign text configurations
    # DAY 1
    if len(day_1) == 1:
        day_1_text = '1 EVENT'
    else:
        day_1_text = f'{len(day_1)} EVENTS'
    
    events1.config(text= day_1_text)

    # Collects information about widget
    events1_width = events1.winfo_reqwidth()
    events1_height = events1.winfo_reqheight()
    
    # Makes x and y values based on the center of the widget
    events1_x_centered = x1 - events1_width/2
    events1_y_centered = y1 - events1_height/2

    events1.place(x=events1_x_centered, y=events1_y_centered)

    # DAY 2
    if len(day_2) == 1:
        day_2_text = '1 EVENT'
    else:
        day_2_text = f'{len(day_2)} EVENTS'
    
    events2.config(text= day_2_text)

    # Collects information about widget
    events2_width = events2.winfo_reqwidth()
    events2_height = events2.winfo_reqheight()
    
    # Makes x and y values based on the center of the widget
    events2_x_centered = x2 - events2_width/2
    events2_y_centered = y2 - events2_height/2

    events2.place(x=events2_x_centered, y=events2_y_centered)

    # DAY 3
    if len(day_3) == 1:
        day_3_text = '1 EVENT'
    else:
        day_3_text = f'{len(day_3)} EVENTS'
    
    events3.config(text= day_3_text)

    # Collects information about widget
    events3_width = events3.winfo_reqwidth()
    events3_height = events3.winfo_reqheight()
    
    # Makes x and y values based on the center of the widget
    events3_x_centered = x3 - events3_width/2
    events3_y_centered = y3 - events3_height/2

    events3.place(x=events3_x_centered, y=events3_y_centered)

    # DAY 4
    if len(day_4) == 1:
        day_4_text = '1 EVENT'
    else:
        day_4_text = f'{len(day_4)} EVENTS'
    
    events4.config(text= day_4_text)

    # Collects information about widget
    events4_width = events4.winfo_reqwidth()
    events4_height = events4.winfo_reqheight()
    
    # Makes x and y values based on the center of the widget
    events4_x_centered = x4 - events4_width/2
    events4_y_centered = y4 - events4_height/2

    events4.place(x=events4_x_centered, y=events4_y_centered)

    return canvas.after(1000, update_events, canvas, events1, x1, y1, events2, x2, y2, events3, x3, y3, events4, x4, y4)


def calendar(canvas):

    """
    Function updates the calendar based on the selected time.
    """

    # Call API
    calendar = get_calendar()

    # Set current date for organizing events based on days ahead of the current date
    current_date = str(datetime.datetime.now().strftime('%Y-%m-%d'))

    # Calendar list of events, empty to be appended into
    calendar_events = []

    # For loop to separate out events for current date
    for date, event_list in calendar.items():
        if date == str(datetime.datetime.strptime(current_date, '%Y-%m-%d'))[:10]:
            calendar_events.extend(event_list)
    
    # Standard y values for calendar section so events can move and be correctly placed based on star and end time
    hour_height = 95
    minute_height = 360 / (60 * 4)

    # Color list that will be selected randomly
    colors = ['#7C92B7', '#B77B9E', '#7BB77E']

    # For loop to parse through calendar date and show events for today
    for event in calendar_events:
        shour, smin = map(int, event["start_time"].split(':')) # Separates hour and min in Start time of events
        ehour, emin = map(int, event["end_time"].split(':')) # Separates hour and min in End time of events
        if shour == int(datetime.datetime.now().strftime('%H')): # Current hour
            # Pick x value
            x = 353
            
            # Y value based on time event starts
            y = 10 + (smin * minute_height)
            
            # Build Rectangle box
            canvas.create_rectangle(x, y, (x + 140.5), (((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height)), fill=colors[0])
            
            # Create Label will summary of event
            calendar = tk.Label(canvas, text=f"{event['summary']}", font=("Inter", 18, "bold"), bg=colors[0], fg="#FFFFFF", wraplength=95,
                                width=round(7/140 * 140.5), height=round(5/200 * (((((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height))) - y)))

            # Center Label based on rectangular box size
            width = calendar.winfo_reqwidth()
            height = calendar.winfo_reqheight()
            x_centered = (x + 70.25) - width/2
            y_centered = (y + ((((((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height))) - y) / 2)) - height/2
            
            # Place label
            calendar.place(x=x_centered, y=y_centered)

        elif shour == (int(datetime.datetime.now().strftime('%H')) + 1): # Current hour + 1
            # Set x value
            x = 503.5

            # Y value based on time event starts
            y = 105 + (smin * minute_height)

            # Build Rectangle box
            canvas.create_rectangle(x, y, (x + 140.5), (((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height)), fill=colors[1])
            
            # Create Label will summary of event
            calendar = tk.Label(canvas, text=f"{event['summary']}", font=("Inter", 18, "bold"), bg=colors[1], fg="#FFFFFF", wraplength=95,
                                width=round(7/140 * 140.5), height=round(5/200 * (((((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height))) - y)))
            
            # Center Label based on rectangular box size
            width = calendar.winfo_reqwidth()
            height = calendar.winfo_reqheight()
            x_centered = (x + 70.25) - width/2
            y_centered = (y + ((((((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height))) - y) / 2)) - height/2
            
            # Place label
            calendar.place(x=x_centered, y=y_centered)

        elif shour == (int(datetime.datetime.now().strftime('%H')) + 2): # Current hour + 2
            # Set x value
            x = 353

            # Y value based on time event starts
            y = 200 + (smin * minute_height)

            # Build Rectangle box
            canvas.create_rectangle(x, y, (x + 140.5), (((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height)), fill=colors[2])
            
            # Create Label will summary of event
            calendar = tk.Label(canvas, text=f"{event['summary']}", font=("Inter", 18, "bold"), bg=colors[2], fg="#FFFFFF", wraplength=95, 
                                width=round(7/140 * 140.5), height=round(5/200 * (((((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height))) - y)))
            
            # Center Label based on rectangular box size
            width = calendar.winfo_reqwidth()
            height = calendar.winfo_reqheight()
            x_centered = (x + 70.25) - width/2
            y_centered = (y + ((((((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height))) - y) / 2)) - height/2
            
            # Place label
            calendar.place(x=x_centered, y=y_centered)

        elif shour == (int(datetime.datetime.now().strftime('%H')) + 3): # Current hour + 3 
            # Set x value
            x = 503.5

            # Y value based on time event starts
            y = 295 + (smin * minute_height)

            # Build Rectangle box
            canvas.create_rectangle(x, y, (x + 140.5), (((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height)), fill=colors[0])
            
            # Create Label will summary of event
            calendar = tk.Label(canvas, text=f"{event['summary']}", font=("Inter", 18, "bold"), bg=colors[0], fg="#FFFFFF", wraplength=95,
                                width=round(7/140 * 140.5), height=round(5/200 * (((((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height))) - y)))
            
            # Center Label based on rectangular box size
            width = calendar.winfo_reqwidth()
            height = calendar.winfo_reqheight()
            x_centered = (x + 70.25) - width/2
            y_centered = (y + ((((((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height))) - y) / 2)) - height/2
            
            # Place label
            calendar.place(x=x_centered, y=y_centered)

    # Update Function
    update_calendar(canvas)

    return


def update_calendar(canvas):

    """
    Function updates google calendar by calling API again
    """

    # Call API
    calendar = get_calendar()

    # Set current date for organizing events based on days ahead of the current date
    current_date = str(datetime.datetime.now().strftime('%Y-%m-%d'))

    # Calendar list of events, empty to be appended into
    calendar_events = []
    calendar_event_id = []

    # For loop to separate out events for current date
    for date, event_list in calendar.items():
        if date == str(datetime.datetime.strptime(current_date, '%Y-%m-%d'))[:10]:
            calendar_events.extend(event_list)
    
    # Standard y values for calendar section so events can move and be correctly placed based on star and end time
    hour_height = 95
    minute_height = 360 / (60 * 4)

    # Color list that will be selected randomly
    colors = ['#7C92B7', '#B77B9E', '#7BB77E']

    # For loop to parse through calendar date and show events for today
    for event in calendar_events:
        shour, smin = map(int, event["start_time"].split(':')) # Separates hour and min in Start time of events
        ehour, emin = map(int, event["end_time"].split(':')) # Separates hour and min in End time of events
        if shour == int(datetime.datetime.now().strftime('%H')): # Current hour
            # Pick x value
            x = 353
            
            # Y value based on time event starts
            y = 10 + (smin * minute_height)
            
            # Build Rectangle box
            event_rect = canvas.create_rectangle(x, y, (x + 140.5), (((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height)), fill=colors[0])
            
            # Create Label will summary of event
            calendar = tk.Label(canvas, text=f"{event['summary']}", font=("Inter", 18, "bold"), bg=colors[0], fg="#FFFFFF", wraplength=95,
                                width=round(7/140 * 140.5), height=round(5/200 * (((((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height))) - y)))

            # Center Label based on rectangular box size
            width = calendar.winfo_reqwidth()
            height = calendar.winfo_reqheight()
            x_centered = (x + 70.25) - width/2
            y_centered = (y + ((((((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height))) - y) / 2)) - height/2
            
            # Place label
            calendar.place(x=x_centered, y=y_centered)
            
            # Append values to list for update function
            calendar_event_id.extend([event_rect, calendar])

        elif shour == (int(datetime.datetime.now().strftime('%H')) + 1): # Current hour + 1
            # Set x value
            x = 503.5

            # Y value based on time event starts
            y = 105 + (smin * minute_height)

            # Build Rectangle box
            event_rect = canvas.create_rectangle(x, y, (x + 140.5), (((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height)), fill=colors[1])
            
            # Create Label will summary of event
            calendar = tk.Label(canvas, text=f"{event['summary']}", font=("Inter", 18, "bold"), bg=colors[1], fg="#FFFFFF", wraplength=95, 
                                width=round(7/140 * 140.5), height=round(5/200 * (((((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height))) - y)))
            
            # Center Label based on rectangular box size
            width = calendar.winfo_reqwidth()
            height = calendar.winfo_reqheight()
            x_centered = (x + 70.25) - width/2
            y_centered = (y + ((((((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height))) - y) / 2)) - height/2
            
            # Place label
            calendar.place(x=x_centered, y=y_centered)

            # Append values to list for update function
            calendar_event_id.extend([event_rect, calendar])

        elif shour == (int(datetime.datetime.now().strftime('%H')) + 2): # Current hour + 2
            # Set x value
            x = 353

            # Y value based on time event starts
            y = 200 + (smin * minute_height)

            # Build Rectangle box
            event_rect = canvas.create_rectangle(x, y, (x + 140.5), (((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height)), fill=colors[2])
            
            # Create Label will summary of event
            calendar = tk.Label(canvas, text=f"{event['summary']}", font=("Inter", 18, "bold"), bg=colors[2], fg="#FFFFFF", wraplength=95, 
                                width=round(7/140 * 140.5), height=round(5/200 * (((((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height))) - y)))
            
            # Center Label based on rectangular box size
            width = calendar.winfo_reqwidth()
            height = calendar.winfo_reqheight()
            x_centered = (x + 70.25) - width/2
            y_centered = (y + ((((((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height))) - y) / 2)) - height/2
            
            # Place label
            calendar.place(x=x_centered, y=y_centered)

            # Append values to list for update function
            calendar_event_id.extend([event_rect, calendar])

        elif shour == (int(datetime.datetime.now().strftime('%H')) + 3): # Current hour + 3 
            # Set x value
            x = 503.5

            # Y value based on time event starts
            y = 295 + (smin * minute_height)

            # Build Rectangle box
            event_rect = canvas.create_rectangle(x, y, (x + 140.5), (((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height)), fill=colors[0])
            
            # Create Label will summary of event
            calendar = tk.Label(canvas, text=f"{event['summary']}", font=("Inter", 18, "bold"), bg=colors[0], fg="#FFFFFF", wraplength=95, 
                                width=round(7/140 * 140.5), height=round(5/200 * (((((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height))) - y)))
            
            # Center Label based on rectangular box size
            width = calendar.winfo_reqwidth()
            height = calendar.winfo_reqheight()
            x_centered = (x + 70.25) - width/2
            y_centered = (y + ((((((abs(ehour - int(datetime.datetime.now().strftime('%H')))* hour_height) + 10) + (emin * minute_height))) - y) / 2)) - height/2
            
            # Place label
            calendar.place(x=x_centered, y=y_centered)

            # Append values to list for update function
            calendar_event_id.extend([event_rect, calendar])
    """
    for i in range(len(calendar_event_id) // 2):
        event_rect_id = calendar_event_id[i * 2]
        event_label_id = calendar_event_id[i * 2 + 1]
        canvas.delete(event_rect_id)
        canvas.delete(event_label_id)
    """
    return canvas.after(1000, update_calendar, canvas)
