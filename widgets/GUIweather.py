# Imports
import tkinter as tk
import requests
from PIL import Image, ImageTk


# Functions
def request_weather():

    """
    Function will call realtim API data 
    Function will collect and sort weather data
    """

    # API key
    api_key = "Zv09qzYfSpbyDnZFZ2T9HYIEUQljZkNk"

    # Weather details
    location = "Mobile, AL, USA" # Location of weather
    units = "imperial" # Units of weather (I am ashamed I need imperial)

    # URL realtime api
    realtime_url = f"https://api.tomorrow.io/v4/weather/realtime?location={location}&units={units}&apikey={api_key}"

    # Accept api data
    realtime_headers = {"accept": "application/json"} # For realtime weather

    # Retrieve a response
    realtime_response = requests.get(url=realtime_url, headers=realtime_headers).json() # Convert response into json file for handling

    # Sort data for realtime weather response
    realtime_data = realtime_response.get("data", {}) # Retreives data from json file
    realtime_temperature = round(realtime_data.get("values", {}).get("temperature", "N/A"),None) # Retreives temperature from json file
    realtime_humidity = realtime_data.get("values", {}).get("humidity", "N/A") # Retreives humidity from json file
    realtime_windspeed = round(realtime_data.get("values", {}).get("windSpeed", "N/A"),None) # Retrives wind speed from json file
    realtime_weathercode = realtime_data.get("values", {}).get("weatherCode", "N/A") # Retreives weather code from json file

    # Return a dictionary for modularly calling on values when creating widgets in GUI
    return {
        "temp": realtime_temperature,
        "humidity": realtime_humidity,
        "windspeed": realtime_windspeed,
        "weather": realtime_weathercode,
    }


def request_forecast():

    """
    Function will make API call for forecast data for the coming week
    Function will collect, and sort weather data
    """

    # API key
    api_key = "Zv09qzYfSpbyDnZFZ2T9HYIEUQljZkNk"

    # Weather details
    location = "Mobile, AL, USA" # Location of weather
    timesteps = "1d" # Refresh interval
    units = "imperial" # Units of weather (I am ashamed I need imperial)

    # URL forecast api
    forecast_url = f"https://api.tomorrow.io/v4/weather/forecast?location={location}&timesteps={timesteps}&units={units}&apikey={api_key}"

    # Accept api data
    forecast_headers = {"accept": "application/json"} # For forecast weather

    # Retrieve a response
    forecast_response = requests.get(url=forecast_url, headers=forecast_headers).json() # Convert response into json file for handling

    # Sort data for forecast weather response
    forecast_data = forecast_response.get("timelines", {}).get("daily", []) # Retreives daily weather data for the next 5 days

    forecast_weathercode = [] # Empty list for weather codes in the forecast
    forecast_tempmax = [] # Empty list for temp maxs in the forecast
    forecast_tempmin = [] # Empty list for temp mins in the forecast
    
    for day in forecast_data: # For loop through the 5 days in the forecast and 
        forecast_weathercode.append(day.get("values", {}).get("weatherCodeMax", "N/A"))
        forecast_tempmax.append(day.get("values", {}).get("temperatureMax", "N/A"))
        forecast_tempmin.append(day.get("values", {}).get("temperatureMin", "N/A"))

    # Return a dictionary for modularly calling on values when creating widgets in GUI
    return {
        "forecast max temp": forecast_tempmax,
        "forecast min temp": forecast_tempmin,
        "forecast weather": forecast_weathercode
    }


def weather_icons(weathercode):

    """
    Function converts weather codes from API into common weather images for GUI
    """

    # Weather icon path
    image_path = "/Users/keg-macbook/MontyPython/raspi-dashboard/pictures/"

    # WeatherCode dictionary from Tomorrow.io
    weatherCode = {
        "0": "N/A",
        "1000": "1000.png",
        "1100": "1101,1100.png",
        "1101": "1101,1100.png",
        "1102": "1102,1001,2000,2100.png",
        "1001": "1102,1001,2000,2100.png",
        "2000": "1102,1001,2000,2100.png",
        "2100": "1102,1001,2000,2100.png",
        "4000": "4000,4001,4200.png",
        "4001": "4000,4001,4200.png",
        "4200": "4000,4001,4200.png",
        "4201": "4201.png",
        "5000": "5001,5000,5100.png",
        "5001": "5001,5000,5100.png",
        "5100": "5001,5000,5100.png",
        "5101": "5101.png",
        "6000": "6000,6001,6200,6201.png",
        "6001": "6000,6001,6200,6201.png",
        "6200": "6000,6001,6200,6201.png",
        "6201": "6000,6001,6200,6201.png",
        "7000": "7000,7101,7102.png",
        "7101": "7000,7101,7102.png",
        "7102": "7000,7101,7102.png",
        "8000": "8000.png"
    }

# Assign image for weather
    #icon_code = [weatherCode.get(str(i), "N/A") for i in weathercode] # Retreives weather icons for forecast weather code
    icon_code = weatherCode.get(f"{weathercode}", "N/A")

    # Assign directory for images
    #icon = [image_path + i for i in icon_code]
    icon = image_path + icon_code

    return icon


def weather(canvas, temp_x, temp_y, hum_x, hum_y, wind_x, wind_y, weather_x, weather_y):

    """
    Function will create widget for realtime weather:
    - Temperature in F
    - Weather icon
    - Humidity
    - Windspeed
    """

    # Run Api function
    weather_data = request_weather()

    # Create variables for api data
    temp = weather_data["temp"]
    humidity = weather_data["humidity"]
    windspeed = weather_data["windspeed"]
    weather = weather_data["weather"]

    # Convert weathercode into icon
    icon = weather_icons(weather) # Runs functions to convert code into icon path
    icon = Image.open(icon) # Opens .png file

    # Resize image
    icon_width = 75
    icon_height = 75
    icon = icon.resize((icon_width, icon_height), Image.LANCZOS)

    icon = ImageTk.PhotoImage(icon) # Creates image

    # Label text and icons including location
    # Temp
    temp_label = tk.Label(canvas, text=f"{temp}˚", font=("Inter", 60, "bold"), bg="#1E1E1E", fg="#FFFFFF")
    temp_label.place(x=temp_x, y=temp_y) # Location of widget 

    # Humidity
    humidity_label = tk.Label(canvas, text=f"H:{humidity}", font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#FFFFFF")
    humidity_label.place(x=hum_x, y=hum_y) # Location of widget 

    # Windspeed
    windspeed_label = tk.Label(canvas, text=f"W:{windspeed}", font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#FFFFFF")
    windspeed_label.place(x=wind_x, y=wind_y) # Location of widget, NOTE: image lays on top on other labels!

    # Icon
    icon_label = tk.Label(canvas, image=icon, bg="#1E1E1E")

    icon_width = icon_label.winfo_reqwidth() # Collects widget width
    icon_height = icon_label.winfo_reqheight() # Collects widget height

    icon_x_centered = weather_x - icon_width/2 # Centers x value
    icon_y_centered = weather_y - icon_height/2 # Centers y value 

    icon_label.place(x=icon_x_centered, y=icon_y_centered) # Location of widget 

    # Update API data
    update_weather(canvas, temp_label, humidity_label, windspeed_label, icon_label)

    return temp_label, humidity_label, windspeed_label, icon_label


def update_weather(canvas, temp_label, humidity_label, windspeed_label, icon_label):

    """
    Function updates the API Data for weather() Function
    """

    # Call the API and get updated weather data
    weather_data = request_weather()

    # Update the labels and icon with the new data
    temp_label.config(text=f"{weather_data['temp']}˚")
    humidity_label.config(text=f"H:{weather_data['humidity']}")
    windspeed_label.config(text=f"W:{weather_data['windspeed']}")

    # Convert new weather code into icon
    icon_path = weather_icons(weather_data['weather'])
    new_icon = Image.open(icon_path)
    new_icon = new_icon.resize((75, 75), Image.LANCZOS)
    new_icon = ImageTk.PhotoImage(new_icon)

    # Update the icon label with the new icon
    icon_label.config(image=new_icon)
    icon_label.image = new_icon  # Keep a reference to avoid garbage collection

    # Return the updated labels and icon
    return canvas.after(300000, update_weather, canvas, temp_label, humidity_label, windspeed_label, icon_label)


#def forecast(canvas, tom_x, tom_y, tom1_x, tom1_y, tom2_x, tom2_y, tom3_x, tom3_y):

