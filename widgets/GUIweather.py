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
    api_key = "Your API Key" # Change to actual API Key

    # Weather details
    location = "City, State, Country" # Location of weather if in United States,
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
    api_key = "Your API Key" # Change to actual API Key

    # Weather details
    location = "City, State, Country" # Location of weather if in the United States
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
        weathercode = day.get("values", {}).get("weatherCodeMax", "N/A")
        tempmax = round(day.get("values", {}).get("temperatureMax", "N/A"),None)
        tempmin = round(day.get("values", {}).get("temperatureMin", "N/A"),None)
        forecast_weathercode.append(weathercode)
        forecast_tempmax.append(tempmax)
        forecast_tempmin.append(tempmin)

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
    image_path = "~/Raspi-Dashboard/pictures/" # Change to actual directory path leading to pictures folder

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
    if type(weathercode) == list:
        icon_code = [weatherCode.get(f"{i}", "N/A") for i in weathercode] # Retreives weather icons for forecast weather code
        # Assign directory for images
        icon = [image_path + i for i in icon_code]
    else:
        icon_code = weatherCode.get(f"{weathercode}", "N/A")
        # Assign directory for images
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
    icon = icon.resize((icon_width, icon_height), Image.BICUBIC)

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
    new_icon = new_icon.resize((75, 75), Image.BICUBIC)
    new_icon = ImageTk.PhotoImage(new_icon)

    # Update the icon label with the new icon
    icon_label.config(image=new_icon)
    icon_label.image = new_icon  # Keep a reference to avoid garbage collection

    # Return the updated labels and icon
    return canvas.after(300000, update_weather, canvas, temp_label, humidity_label, windspeed_label, icon_label)


def forecast(canvas, temp1_x, temp1_y, icon1_x, icon1_y, temp2_x, temp2_y, icon2_x, icon2_y, temp3_x, temp3_y, icon3_x, icon3_y, 
             temp4_x, temp4_y, icon4_x, icon4_y):

    """
    Function will create widget for one of the four forecasted days:
    - Max temp forecast
    - Min temp forecast
    - Weather icon forecast
    """

    # Run API function
    forecast_data = request_forecast()

    # Create variables for API data
    # Day 1
    maxtemp = forecast_data["forecast max temp"]
    mintemp = forecast_data["forecast min temp"]
    icon = forecast_data["forecast weather"]

    icons = weather_icons(icon)

    ########## DAY 1 ##########
    
    # Icon 
    icon_1 = Image.open(icons[0]) # Opens .png file 

    # Resize image
    icon_1_width = 65
    icon_1_height = 65
    icon_1 = icon_1.resize((icon_1_width, icon_1_height), Image.BICUBIC)

    icon_1 = ImageTk.PhotoImage(icon_1) # Creates image

    # Label text and icons and locations
    icon_1_label = tk.Label(canvas, image=icon_1, bg="#1E1E1E")

    icon_1_width = icon_1_label.winfo_reqwidth() # Collects widget width
    icon_1_height = icon_1_label.winfo_reqheight() # Collects widget height

    icon_1_x_centered = icon1_x - icon_1_width/2 # Centers x value
    icon_1_y_centered = icon1_y - icon_1_height/2 # Centers y value 

    icon_1_label.place(x=icon_1_x_centered, y=icon_1_y_centered) # Location of widget

    # Temp
    # Label text and icons and locations
    temp_1_label = tk.Label(canvas, text=f"{mintemp[0]}˚    {maxtemp[0]}˚", font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#FFFFFF")

    temp_1_width = temp_1_label.winfo_reqwidth() # Collects widget width
    temp_1_height = temp_1_label.winfo_reqheight() # Collects widget height

    temp_1_x_centered = temp1_x - temp_1_width/2 # Centers x value
    temp_1_y_centered = temp1_y - temp_1_height/2 # Centers y value

    temp_1_label.place(x=temp_1_x_centered, y=temp_1_y_centered)

    ###########################

    ########## DAY 2 ##########

    # Icon 
    icon_2 = Image.open(icons[1]) # Opens .png file

    # Resize image
    icon_2_width = 65
    icon_2_height = 65
    icon_2 = icon_2.resize((icon_2_width, icon_2_height), Image.BICUBIC)

    icon_2 = ImageTk.PhotoImage(icon_2) # Creates image

    # Label text and icons and locations
    icon_2_label = tk.Label(canvas, image=icon_2, bg="#1E1E1E")

    icon_2_width = icon_2_label.winfo_reqwidth() # Collects widget width
    icon_2_height = icon_2_label.winfo_reqheight() # Collects widget height

    icon_2_x_centered = icon2_x - icon_2_width/2 # Centers x value
    icon_2_y_centered = icon2_y - icon_2_height/2 # Centers y value 

    icon_2_label.place(x=icon_2_x_centered, y=icon_2_y_centered) # Location of widget

    # Temp
    # Label text and icons and locations
    temp_2_label = tk.Label(canvas, text=f"{mintemp[1]}˚    {maxtemp[1]}˚", font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#FFFFFF")

    temp_2_width = temp_2_label.winfo_reqwidth() # Collects widget width
    temp_2_height = temp_2_label.winfo_reqheight() # Collects widget height

    temp_2_x_centered = temp2_x - temp_2_width/2 # Centers x value
    temp_2_y_centered = temp2_y - temp_2_height/2 # Centers y value

    temp_2_label.place(x=temp_2_x_centered, y=temp_2_y_centered)

    ###########################

    ########## DAY 3 ##########
    
    # Icon 
    icon_3 = Image.open(icons[2]) # Opens .png file

    # Resize image
    icon_3_width = 65
    icon_3_height = 65
    icon_3 = icon_3.resize((icon_3_width, icon_3_height), Image.BICUBIC)

    icon_3 = ImageTk.PhotoImage(icon_3) # Creates image

    # Label text and icons and locations
    icon_3_label = tk.Label(canvas, image=icon_3, bg="#1E1E1E")

    icon_3_width = icon_3_label.winfo_reqwidth() # Collects widget width
    icon_3_height = icon_3_label.winfo_reqheight() # Collects widget height

    icon_3_x_centered = icon3_x - icon_3_width/2 # Centers x value
    icon_3_y_centered = icon3_y - icon_3_height/2 # Centers y value 

    icon_3_label.place(x=icon_3_x_centered, y=icon_3_y_centered) # Location of widget

    # Temp
    # Label text and icons and locations
    temp_3_label = tk.Label(canvas, text=f"{mintemp[2]}˚    {maxtemp[2]}˚", font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#FFFFFF")

    temp_3_width = temp_3_label.winfo_reqwidth() # Collects widget width
    temp_3_height = temp_3_label.winfo_reqheight() # Collects widget height

    temp_3_x_centered = temp3_x - temp_3_width/2 # Centers x value
    temp_3_y_centered = temp3_y - temp_3_height/2 # Centers y value

    temp_3_label.place(x=temp_3_x_centered, y=temp_3_y_centered)

    ###########################

    ########## DAY 4 ##########
    
    # Icon 
    icon_4 = Image.open(icons[3]) # Opens .png file

    # Resize image
    icon_4_width = 65
    icon_4_height = 65
    icon_4 = icon_4.resize((icon_4_width, icon_4_height), Image.BICUBIC)

    icon_4 = ImageTk.PhotoImage(icon_4) # Creates image

    # Label text and icons and locations
    icon_4_label = tk.Label(canvas, image=icon_4, bg="#1E1E1E")

    icon_4_width = icon_4_label.winfo_reqwidth() # Collects widget width
    icon_4_height = icon_4_label.winfo_reqheight() # Collects widget height

    icon_4_x_centered = icon4_x - icon_4_width/2 # Centers x value
    icon_4_y_centered = icon4_y - icon_4_height/2 # Centers y value 

    icon_4_label.place(x=icon_4_x_centered, y=icon_4_y_centered) # Location of widget

    # Temp
    # Label text and icons and locations
    temp_4_label = tk.Label(canvas, text=f"{mintemp[3]}˚    {maxtemp[3]}˚", font=("Inter", 22, "bold"), bg="#1E1E1E", fg="#FFFFFF")

    temp_4_width = temp_4_label.winfo_reqwidth() # Collects widget width
    temp_4_height = temp_4_label.winfo_reqheight() # Collects widget height

    temp_4_x_centered = temp4_x - temp_4_width/2 # Centers x value
    temp_4_y_centered = temp4_y - temp_4_height/2 # Centers y value

    temp_4_label.place(x=temp_4_x_centered, y=temp_4_y_centered)

    ###########################

    # Update API Data
    update_forecast(canvas, icon_1_label, icon_2_label, icon_3_label, icon_4_label, temp_1_label, temp_2_label, temp_3_label, temp_4_label)

    return icon_1_label, icon_2_label, icon_3_label, icon_4_label, temp_1_label, temp_2_label, temp_3_label, temp_4_label


def update_forecast(canvas, icon_1_label, icon_2_label, icon_3_label, icon_4_label, temp_1_label, temp_2_label, temp_3_label, temp_4_label):

    """
    Function updates the API Data for weather() Function
    """

    # Call the API and get updated weather data
    weather_data = request_forecast()

    # Update the labels and icon with the new data
    temp_1_label.config(text=f"{weather_data['forecast min temp'][0]}˚    {weather_data['forecast max temp'][0]}")
    temp_2_label.config(text=f"{weather_data['forecast min temp'][1]}˚    {weather_data['forecast max temp'][1]}")
    temp_3_label.config(text=f"{weather_data['forecast min temp'][2]}˚    {weather_data['forecast max temp'][2]}")
    temp_4_label.config(text=f"{weather_data['forecast min temp'][3]}˚    {weather_data['forecast max temp'][3]}")

    # Convert new weather code into icon DAY 1
    icon_1_path = weather_icons(weather_data['forecast weather'][0])
    new_icon_1 = Image.open(icon_1_path)
    new_icon_1 = new_icon_1.resize((65, 65), Image.BICUBIC)
    new_icon_1 = ImageTk.PhotoImage(new_icon_1)

    # Update the icon label with the new icon
    icon_1_label.config(image=new_icon_1)
    icon_1_label.image = new_icon_1  # Keep a reference to avoid garbage collection

    # Convert new weather code into icon DAY 2
    icon_2_path = weather_icons(weather_data['forecast weather'][1])
    new_icon_2 = Image.open(icon_2_path)
    new_icon_2 = new_icon_2.resize((65, 65), Image.BICUBIC)
    new_icon_2 = ImageTk.PhotoImage(new_icon_2)

    # Update the icon label with the new icon 
    icon_2_label.config(image=new_icon_2)
    icon_2_label.image = new_icon_2  # Keep a reference to avoid garbage collection

    # Convert new weather code into icon DAY 3
    icon_3_path = weather_icons(weather_data['forecast weather'][2])
    new_icon_3 = Image.open(icon_3_path)
    new_icon_3 = new_icon_3.resize((65, 65), Image.BICUBIC)
    new_icon_3 = ImageTk.PhotoImage(new_icon_3)

    # Update the icon label with the new icon
    icon_3_label.config(image=new_icon_3)
    icon_3_label.image = new_icon_3  # Keep a reference to avoid garbage collection

    # Convert new weather code into icon DAY 4
    icon_4_path = weather_icons(weather_data['forecast weather'][3])
    new_icon_4 = Image.open(icon_4_path)
    new_icon_4 = new_icon_4.resize((65, 65), Image.BICUBIC)
    new_icon_4 = ImageTk.PhotoImage(new_icon_4)

    # Update the icon label with the new icon
    icon_4_label.config(image=new_icon_4)
    icon_4_label.image = new_icon_4  # Keep a reference to avoid garbage collection

    # Return the updated labels and icon
    return canvas.after(300000, update_weather, canvas, icon_1_label, icon_2_label, icon_3_label, icon_4_label, temp_1_label, temp_2_label, temp_3_label, temp_4_label)
