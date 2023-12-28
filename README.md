# Raspi-Dashboard
Raspberry Pi Dashboard Application v0.1.2-alpha  
This application is intended for a 7inch 800x400 touchscreen. The application is a desktop dashboard that updates:
- Date and time
- Weather and forecast
- Google Calendar

**CURRENT PROGRESS**

<img width="792" alt="Screenshot 2023-12-27 at 6 51 50 PM" src="https://github.com/Heisenberg-UP/Raspi-Dashboard/assets/99283516/789649ef-d56b-475a-aec4-593d8bdf3dd4">  

**v0.1.2-alpha Notes:**  
The dashboard application requires the user to have a Google account and a Tomorrow.io account. Must use OAuth2.0 to pull user data from google calendar and an API key to pull from Tomorrow.io. To sucessfully use the application in its current state, one must create a virtual environment in python and install all the necessary libraries (found in .py files). Go to google's API website and obtain your client_secret.json file and replace the client_secret.json file in the credentials folder. Now go to GUIgoogle.py file and change all of the directory paths in the authorize() to your preference. Make an account with Tomorrow.io and copy your API key into the GUIweather.py api_key variable and change the location variable to your desired city, state, and country. 

Coming soon:
- Calendar update function
- High resolution icons
- Night time weather icons
- Deployable bash script
