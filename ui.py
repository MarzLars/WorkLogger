import sys
import customtkinter
import time
import os
import subprocess
import csv
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from time_tracker import TimeTracker

customtkinter.set_appearance_mode("dark")  # Set the appearance mode to dark
customtkinter.set_default_color_theme("dark-blue")  # Set the color theme to dark-blue

class TimeTrackingUI:
    def __init__(self, root):
        self.root = root
        self.logs_visible = False  # Initialization
        self.debug_visible = False  # Debug buttons visibility
        self.tracker = TimeTracker()
        self.update_job = None  # To keep track of the update job

        self.frame = customtkinter.CTkFrame(master=self.root)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.label = customtkinter.CTkLabel(master=self.frame, text="WorkLogger", font=("Arial", 20))
        self.label.pack(pady=12, padx=10)

        self.elapsed_time_label = customtkinter.CTkLabel(master=self.frame, text="Elapsed Time", font=("Arial", 14))
        self.elapsed_time_label.pack(fill="x", padx=5, pady=5)

        # Create a frame for the control buttons
        control_frame = customtkinter.CTkFrame(master=self.frame)
        control_frame.pack(pady=12, padx=10, fill="x")

        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)
        control_frame.columnconfigure(2, weight=1)

        self.start_button = customtkinter.CTkButton(master=control_frame, text="Start", font=("Arial", 12), command=self.start)
        self.start_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.pause_button = customtkinter.CTkButton(master=control_frame, text="Pause", font=("Arial", 12), command=self.pause)
        self.pause_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.stop_button = customtkinter.CTkButton(master=control_frame, text="Stop", font=("Arial", 12), command=self.stop)
        self.stop_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Add the "Open Log Location" button
        self.open_log_button = customtkinter.CTkButton(master=self.frame, text="Open Log Location", command=self.open_logs, width=100)
        self.open_log_button.pack(fill="x", padx=5, pady=5)

        # Add the "Debug" button
        self.debug_button = customtkinter.CTkButton(master=self.frame, text="Debug", command=self.toggle_debug, width=100)
        self.debug_button.pack(fill="x", padx=5, pady=5)

        # Add the "Clear Logs" button (initially hidden)
        self.clear_logs_button = customtkinter.CTkButton(master=self.frame, text="Clear Logs", command=self.clear_logs, width=100)
        self.clear_logs_button.pack(fill="x", padx=5, pady=5)
        self.clear_logs_button.pack_forget()

        # Add the "Toggle Logs" button (initially hidden)
        self.toggle_logs_button = customtkinter.CTkButton(master=self.frame, text="Show Logs", command=self.toggle_logs, width=100)
        self.toggle_logs_button.pack(fill="x", padx=5, pady=5)
        self.toggle_logs_button.pack_forget()

        # Add the "Restart" button (initially hidden)
        self.restart_button = customtkinter.CTkButton(master=self.frame, text="Restart", command=self.restart, width=100)
        self.restart_button.pack(fill="x", padx=5, pady=5)
        self.restart_button.pack_forget()

        self.log_frame = customtkinter.CTkFrame(master=self.frame)  # Widget creation
        self.log_frame.pack(fill="both", padx=5, pady=5, expand=True)
        self.log_frame.pack_forget()  # Initially hide the log frame

        self.log_tree = ttk.Treeview(self.log_frame, columns=("Description", "Date", "Week", "Time Spent", "Hours", "Minutes", "Seconds"), show='headings')
        self.log_tree.heading("Description", text="Description")
        self.log_tree.heading("Date", text="Date")
        self.log_tree.heading("Week", text="Week")
        self.log_tree.heading("Time Spent", text="Time Spent")
        self.log_tree.heading("Hours", text="Hours")
        self.log_tree.heading("Minutes", text="Minutes")
        self.log_tree.heading("Seconds", text="Seconds")
        self.log_tree.pack(fill="both", padx=5, pady=5, expand=True)

        self.display_logs()

    def start(self):
        self.tracker.start()
        self.start_button.configure(fg_color="green", text_color="white", state="disabled")  # Change button color to green, text to white, and disable it
        if not self.update_job:
            self.update_elapsed_time()  # Ensure the update method is called when starting

    def pause(self):
        self.tracker.pause()
        self.start_button.configure(fg_color="yellow", text_color="black", state="normal")  # Change button color to yellow, text to black, and enable it
        if self.update_job:
            self.root.after_cancel(self.update_job)
            self.update_job = None

    def stop(self):
        self.tracker.stop()
        self.start_button.configure(fg_color="#1f6aa5", text_color="white", state="normal")  # Reset button color to blue, text to white, and enable it
        if self.update_job:
            self.root.after_cancel(self.update_job)
            self.update_job = None
        self.prompt_log_time()

    def prompt_log_time(self):
        description = simpledialog.askstring("Input", "Enter a description for the worklog:")
        if description:
            self.tracker.log_time(description)
        self.display_logs()

    def clear_logs(self):
        try:
            os.remove('time_log.xlsx')
            os.remove('time_log.csv')
            messagebox.showinfo("Success", "Log files cleared successfully.")
            self.display_logs()
        except FileNotFoundError:
            messagebox.showwarning("Warning", "Log files not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def display_logs(self):
        for row in self.log_tree.get_children():
            self.log_tree.delete(row)
        if os.path.exists('time_log.csv'):
            with open('time_log.csv', mode='r') as file:
                reader = csv.reader(file, delimiter=';')
                for row in reader:
                    if row[0] == "sep=;":
                        continue  # Skip the "sep=;" line
                    if row == ['Description', 'Date', 'Week', 'Time Spent', 'Hours', 'Minutes', 'Seconds']:
                        continue  # Skip the duplicate header row
                    self.log_tree.insert("", tk.END, values=row)

    def open_logs(self):
        log_file_path = os.path.abspath('time_log.xlsx')
        log_dir = os.path.dirname(log_file_path)
        subprocess.Popen(f'explorer "{log_dir}"')

    def toggle_logs(self):
        if self.logs_visible:
            self.log_frame.pack_forget()
            self.toggle_logs_button.configure(text="Show Logs")
        else:
            self.log_frame.pack(fill="both", padx=5, pady=5, expand=True)
            self.toggle_logs_button.configure(text="Hide Logs")
        self.logs_visible = not self.logs_visible

    def toggle_debug(self):
        if self.debug_visible:
            self.clear_logs_button.pack_forget()
            self.toggle_logs_button.pack_forget()
            self.restart_button.pack_forget()
            self.log_frame.pack_forget()
        else:
            self.clear_logs_button.pack(fill="x", padx=5, pady=5)
            self.toggle_logs_button.pack(fill="x", padx=5, pady=5)
            self.restart_button.pack(fill="x", padx=5, pady=5)
            if self.logs_visible:
                self.log_frame.pack(fill="both", padx=5, pady=5, expand=True)
        self.debug_visible = not self.debug_visible

    def restart(self):
        self.root.destroy()
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def update_elapsed_time(self):
        if self.tracker.running:
            elapsed_time = time.time() - self.tracker.start_time + self.tracker.elapsed_time
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.elapsed_time_label.configure(text=f"{int(hours)}h {int(minutes)}m {int(seconds)}s")
        self.update_job = self.root.after(1000, self.update_elapsed_time)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = customtkinter.CTk()
    root.geometry("400x400")
    root.title("WorkLogger")  # Set the window title
    app = TimeTrackingUI(root)
    app.run()