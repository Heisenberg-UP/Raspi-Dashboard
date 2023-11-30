# Imports
import tkinter as tk
from GUIdatetime import *
from GUIweather import *
#from TEST import *

# Functions
def dashboard_base():

    """
    Function that creates the base dashboard:
    - Size
    - Lines
    - Widgets *COMING LATER*
    """

    # Set root for tk
    root = tk.Tk()

    # Remove top bar and window decorations
    root.overrideredirect(True)

    # Window size
    window_height = 400
    window_width = 800
    root.geometry(f"{window_width}x{window_height}")

    # Background color
    background_color = "#1E1E1E"
    root.configure(bg=background_color)

    # Canvas area for widgets
    canvas = tk.Canvas(root, width=window_width, height=window_height, bg=background_color)
    canvas.pack(fill="none", expand=False)

    # Lines
    canvas.create_line(10, 71, 255, 71, fill="#696969", width=1) # Line at the top left of the GUI, this is just below the date and time
    canvas.create_line(10, 153, 255, 153, fill="#696969", width=1) # Line at the top left of the GUI, below the temperature of the day
    canvas.create_line(265, 10, 265, 390, fill="#F0F0F0", width=1) # Line at the top left of the GUI, Vertical line between temp and calendar
    canvas.create_line(654, 10, 654, 390, fill="#F0F0F0", width=1) # Line at the top right of the GUI, vertical line between calendar and events
    canvas.create_line(275, 105, 644, 105, fill="#696969", width=1) # Line at the top middle of the GUI, horizontal line in calendar
    canvas.create_line(275, 200, 644, 200, fill="#696969", width=1) # line at the middle of the GUI, horizontal line in calendar
    canvas.create_line(275, 295, 644, 295, fill="#696969", width=1) # Line at the bottom middle ofthe GUI, horizontal line in calendar
    canvas.create_line(664, 105, 790, 105, fill="#696969", width=1) # Line at the top right of the GUI, line in event section
    canvas.create_line(664, 200, 790, 200, fill="#696969", width=1) # Line at the middle right of the GUI, line in event section
    canvas.create_line(664, 295, 790, 295, fill="#696969", width=1) # Line at the bottom right of the GUI, line in event section

    ########## Widgets ##########

    # Datetime widgets
    datetime_widget(canvas, 132.5, 40) # Creates Time, Day, and Date in top left of GUI, updates every second 
    days_widget(canvas, 1, 71.25, 173) # Creates day + 1, top left of GUI, updates every second
    days_widget(canvas, 2, 193.75, 173) # Creates day + 2, top left of GUI, updates every second
    days_widget(canvas, 3, 71.25, 287.5) # Creates day + 3, top left of GUI, updates every second
    days_widget(canvas, 4, 193.75, 287.5) # Creates day + 4, top left of GUI, updates every second
    days_widget(canvas, 1, 727, 26.5) # Creates day + 1, top right of GUI, updates every second 
    days_widget(canvas, 2, 727, 121.5) # Creates day + 2, middle right of GUI, updates every second 
    days_widget(canvas, 3, 727, 216.5) # Creates day + 3, middle right of GUI, updates every second 
    days_widget(canvas, 4, 727, 311.5) # Creates day + 4, bottom right of GUI, updates every second 
    time_widget(canvas, 0, 309, 52.5) # Creates time + 0, top middle of GUI, updates every second
    time_widget(canvas, 1, 309, 150.5) # Creates time + 1, top middle of GUI, updates every second
    time_widget(canvas, 2, 309, 245.5) # Creates time + 2, top middle of GUI, updates every second
    time_widget(canvas, 3, 309, 340.5) # Creates time + 2, top middle of GUI, updates every second

    # Weather widgets
    weather(canvas, 10, 73, 198, 85.5, 198, 112, 153.5, 112) # Creates widgets for realtime weather

    #############################

    # Event loop
    root.mainloop()
    return


# Run script
if __name__ == "__main__":
    try:
        dashboard_base()
    except KeyboardInterrupt:
        SystemExit
