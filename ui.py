import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from time_tracker import TimeTracker
import time
import os
import subprocess
import csv
import sys

class TimeTrackingUI:
    def __init__(self):
        self.tracker = TimeTracker()
        self.tracker.ensure_log_file_exists()
        self.root = tk.Tk()
        self.root.title("Time Tracker")

        # Create a frame for the control buttons
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        self.start_button = tk.Button(control_frame, text="Start", command=self.start)
        self.start_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, pady=5)

        self.pause_button = tk.Button(control_frame, text="Pause", command=self.pause)
        self.pause_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, pady=5)

        self.stop_button = tk.Button(control_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, pady=5)

        self.open_logs_button = tk.Button(self.root, text="Open Logs", command=self.open_logs)
        self.open_logs_button.pack(fill=tk.X, padx=5, pady=5)

        self.clear_logs_button = tk.Button(self.root, text="Clear Logs", command=self.clear_logs)
        self.clear_logs_button.pack(fill=tk.X, padx=5, pady=5)

        self.toggle_logs_button = tk.Button(self.root, text="Show Logs", command=self.toggle_logs)
        self.toggle_logs_button.pack(fill=tk.X, padx=5, pady=5)

        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart)
        self.restart_button.pack(fill=tk.X, padx=5, pady=5)

        self.label = tk.Label(self.root, text="Elapsed Time: 0 seconds")
        self.label.pack(fill=tk.X, padx=5, pady=5)

        self.log_frame = tk.Frame(self.root)
        self.log_tree = ttk.Treeview(self.log_frame, columns=("Description", "Date", "Week", "Time Spent", "Hours", "Minutes", "Seconds"), show='headings')
        self.log_tree.heading("Description", text="Description")
        self.log_tree.heading("Date", text="Date")
        self.log_tree.heading("Week", text="Week")
        self.log_tree.heading("Time Spent", text="Time Spent")
        self.log_tree.heading("Hours", text="Hours")
        self.log_tree.heading("Minutes", text="Minutes")
        self.log_tree.heading("Seconds", text="Seconds")
        self.log_tree.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)

        self.update_elapsed_time()
        self.display_logs()

    def start(self):
        self.tracker.start()
        self.update_elapsed_time()  # Ensure the update method is called when starting

    def pause(self):
        self.tracker.pause()

    def stop(self):
        elapsed_time = self.tracker.stop()
        self.label.config(text=f"Elapsed Time: {elapsed_time:.2f} seconds")
        self.prompt_log_time()

    def prompt_log_time(self):
        description = simpledialog.askstring("Input", "Enter a description for the time log:")
        if description:
            self.tracker.log_time(description)
        self.display_logs()

    def update_elapsed_time(self):
        if self.tracker.running:
            elapsed_time = time.time() - self.tracker.start_time + self.tracker.elapsed_time
            self.label.config(text=f"Elapsed Time: {elapsed_time:.2f} seconds")
        self.root.after(1000, self.update_elapsed_time)

    def open_logs(self):
        log_file_path = os.path.abspath('time_log.xlsx')
        log_dir = os.path.dirname(log_file_path)
        subprocess.Popen(f'explorer "{log_dir}"')

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

    def toggle_logs(self):
        if self.log_frame.winfo_ismapped():
            self.log_frame.pack_forget()
            self.toggle_logs_button.config(text="Show Logs")
        else:
            self.log_frame.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)
            self.toggle_logs_button.config(text="Hide Logs")

    def restart(self):
        self.root.destroy()
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TimeTrackingUI()
    app.run()