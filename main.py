# Import the TimeTrackerUI class from the ui module
from ui import TimeTrackerUI
import customtkinter

# Entry point of the application
if __name__ == "__main__":
    root = customtkinter.CTk()
    root.geometry("400x400")
    root.title("WorkLogger")
    # Create an instance of the TimeTrackerUI class
    app = TimeTrackerUI(root)
    # Run the Tkinter main loop to start the application
    app.run()