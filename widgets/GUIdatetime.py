# Imports
import tkinter as tk
from datetime import datetime


# Fucntions
def datetime_widget(canvas, x, y):
    
    """
    Function calls current datetime information:
    - Time, Day of the week
    - Month, Day of the month, Year
    """

    # Get current date and time
    current_datetime = datetime.now()

    # Format date and time
    formatted_datetime = current_datetime.strftime("%H:%M %A\n%B %d, %Y").upper()

    # Update and label text
    datetime_label = tk.Label(canvas, text=formatted_datetime, font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#FFFFFF")

    # Collects information about widget
    width = datetime_label.winfo_reqwidth()
    height = datetime_label.winfo_reqheight()
    
    # Makes x and y values based on the center of the widget
    x_centered = x - width/2
    y_centered = y - height/2

    datetime_label.place(x=x_centered, y=y_centered)

    # Update values
    update_datetime_widget(datetime_label)

    return datetime_label


def update_datetime_widget(datetime_label):

    """
    Function updates datetime widget every 60 seconds
    """

    # Get current date and time
    current_datetime = datetime.now()

    # Format date and time
    formatted_datetime = current_datetime.strftime("%H:%M %A\n%B %d, %Y").upper()

    # Update the label text
    datetime_label.config(text=formatted_datetime)

    # Schedule the update_datetime function to run again after 1 second
    return datetime_label.after(1000, update_datetime_widget, datetime_label) # I dont't understand how this works, however it works!


def days_widget(canvas, future_day, x, y):

    """
    Function will define the future days of the week:
    Current day of the week is Monday, then day + 1 is Tuesday and day + 4 is Friday
    """

    # Get current date and time
    current_datetime = datetime.now()

    # Format day of the week
    formatted_datetime = current_datetime.strftime("%A").upper()

    # Day of the week variables
    dotw = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

    # Abbreviation of weekdays
    abbreviation = {
        "MONDAY": "MON",
        "TUESDAY": "TUE",
        "WEDNESDAY": "WED",
        "THURSDAY": "THR",
        "FRIDAY": "FRI",
        "SATURDAY": "SAT",
        "SUNDAY": "SUN",
        }

    # Get current day or the week index
    current_day_index = dotw.index(formatted_datetime)

    # Selecting future days of the week
    selected_day = abbreviation[dotw[(current_day_index + future_day) % 7]]

    # Update the label text based off desired day
    day_label = tk.Label(canvas, text=selected_day, font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#FFFFFF")

    # Collects information about widget
    width = day_label.winfo_reqwidth()
    height = day_label.winfo_reqheight()
    
    # Makes x and y values based on the center of the widget
    x_centered = x - width/2
    y_centered = y - height/2

    day_label.place(x=x_centered, y=y_centered)

    # Update widget for current day
    update_days_widget(day_label, future_day)

    return day_label


def update_days_widget(day_label, future_day):

    """
    Function updates days widget every day
    """

    # Get current date and time
    current_datetime = datetime.now()

    # Format day of the week
    formatted_datetime = current_datetime.strftime("%A").upper()

    # Day of the week variables
    dotw = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

    # Abbreviation of weekdays
    abbreviation = {
        "MONDAY": "MON",
        "TUESDAY": "TUE",
        "WEDNESDAY": "WED",
        "THURSDAY": "THR",
        "FRIDAY": "FRI",
        "SATURDAY": "SAT",
        "SUNDAY": "SUN",
    }

    # Get current day or the week index
    current_day_index = dotw.index(formatted_datetime)

    # Selecting the future day of the week
    selected_day = abbreviation[dotw[(current_day_index + future_day) % 7]]

    # Update the label text based on the desired day
    day_label.config(text=selected_day)

    # Schedule the update_days_widget function to run again after 1 second
    return day_label.after(1000, update_days_widget, day_label, future_day)


def time_widget(canvas, future_time, x, y):

    """
    Function will define the future time of the day:
    Current time ois 12:00, then time + 1 is 13:00 and time + 4 is 16:00
    """

    # Get current date and time
    current_datetime = datetime.now()

    # Format day of the week
    formatted_time = current_datetime.replace(minute=0, second=0, microsecond=0)
    formatted_time = formatted_time.strftime("%H:%M").upper()

    # Day of the week variables
    tod = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", 
           "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00",
           "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00",
           "21:00", "22:00", "23:00"]

    # Get current time index
    current_time_index = tod.index(formatted_time)

    # Selecting future days of the week
    selected_time = tod[(current_time_index + future_time) % 24]

    # Update the label text based off desired day
    time_label = tk.Label(canvas, text=selected_time, font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#FFFFFF")

    # Collects information about widget
    width = time_label.winfo_reqwidth()
    height = time_label.winfo_reqheight()
    
    # Makes x and y values based on the center of the widget
    x_centered = x - width/2
    y_centered = y - height/2

    time_label.place(x=x_centered, y=y_centered)

    # Update widget for current day
    update_time_widget(time_label, future_time)

    return time_label


def update_time_widget(time_label, future_time):

    """
    Function updates time widget every second
    """

    # Get current date and time
    current_datetime = datetime.now()

    # Format day of the week
    formatted_time = current_datetime.replace(minute=0, second=0, microsecond=0)
    formatted_time = formatted_time.strftime("%H:%M").upper()

    # Day of the week variables
    tod = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", 
           "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00",
           "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00",
           "21:00", "22:00", "23:00"]

    # Get current time index
    current_time_index = tod.index(formatted_time)

    # Selecting future days of the week
    selected_time = tod[(current_time_index + future_time) % 24]

    # Update the label text based on the desired day
    time_label.config(text=selected_time)

    # Schedule the update_days_widget function to run again after 1 second
    return time_label.after(1000, update_time_widget, time_label, future_time)
