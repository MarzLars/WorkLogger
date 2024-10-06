import time
import os
import csv
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Alignment, PatternFill
from datetime import datetime

class TimeTracker:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False

    def start(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True

    def _update_elapsed_time(self):
        if self.running:
            self.elapsed_time += time.time() - self.start_time
            self.start_time = time.time()

    def pause(self):
        self._update_elapsed_time()
        self.running = False

    def stop(self):
        self._update_elapsed_time()
        self.running = False
        return self.elapsed_time

    def reset(self):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False

    def _apply_header_style(self, sheet):
        # Define the fill styles
        orange_fill = PatternFill(start_color="FFA500", end_color="FFA500", fill_type="solid")
        dark_grey_fill = PatternFill(start_color="A9A9A9", end_color="A9A9A9", fill_type="solid")
        
        # Define the font style
        bold_font = Font(name='Arial', size=8, bold=True)
        
        # Apply styles to the header row
        for cell in sheet[1]:
            if cell.value in ["Hours", "Minutes", "Seconds"]:
                cell.fill = orange_fill
            else:
                cell.fill = dark_grey_fill
            cell.font = bold_font  # Apply bold font to header cells

    def _apply_row_style(self, sheet, row_number):
        regular_font = Font(name='Arial', size=8)
        
        for cell in sheet[row_number]:
            cell.font = regular_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
        # Apply wrap text to the Description column
        sheet[f'A{row_number}'].alignment = Alignment(wrap_text=True)
        # Apply Date format to the Date column
        date_cell = sheet[f'B{row_number}']
        date_cell.number_format = 'DD/MM/YYYY'  # Set the date format to DAY/MONTH/YEAR

    def _adjust_column_widths(self, sheet):
        for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
            max_length = 0
            column = sheet[col]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            sheet.column_dimensions[col].width = adjusted_width
        
        # Ensure column B width is at least 12
        if sheet.column_dimensions['B'].width < 12:
            sheet.column_dimensions['B'].width = 12

    def log_time(self, description, file_path='time_log.xlsx', csv_file_path='time_log.csv'):
        hours, remainder = divmod(self.elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        now = datetime.now()
        current_date = now.date()  # Use date object instead of string
        week_number = now.isocalendar()[1]
        
        # Log to Excel
        if os.path.exists(file_path):
            workbook = load_workbook(file_path)
            sheet = workbook.active
        else:
            workbook = Workbook()
            sheet = workbook.active
            sheet.append(['Description', 'Date', 'Week', 'Time Spent', 'Hours', 'Minutes', 'Seconds'])
            self._apply_header_style(sheet)

        row = [description, current_date, week_number, f"={int(hours)} + ({int(minutes)}/60)", int(hours), int(minutes), int(seconds)]
        sheet.append(row)
        
        # Apply row style
        self._apply_row_style(sheet, sheet.max_row)
        
        # Adjust column widths after updating the file
        self._adjust_column_widths(sheet)
        
        workbook.save(file_path)
        
        # Log to CSV
        self.log_time_to_csv(description, current_date, week_number, hours, minutes, seconds, csv_file_path)
        
        self.reset()

    def log_time_to_csv(self, description, current_date, week_number, hours, minutes, seconds, csv_file_path):
        file_exists = os.path.isfile(csv_file_path)
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            if not file_exists:
                file.write("sep=;\n")
                writer.writerow(['Description', 'Date', 'Week', 'Time Spent', 'Hours', 'Minutes', 'Seconds'])
            writer.writerow([description, current_date, week_number, hours + (minutes / 60), int(hours), int(minutes), int(seconds)])

    def ensure_log_file_exists(self, file_path='time_log.xlsx', csv_file_path='time_log.csv'):
        if not os.path.exists(file_path):
            workbook = Workbook()
            sheet = workbook.active
            sheet.append(['Description', 'Date', 'Week', 'Time Spent', 'Hours', 'Minutes', 'Seconds'])
            self._apply_header_style(sheet)
            self._adjust_column_widths(sheet)
            workbook.save(file_path)
        
        if not os.path.exists(csv_file_path):
            with open(csv_file_path, mode='w', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                file.write("sep=;\n")
                writer.writerow(['Description', 'Date', 'Week', 'Time Spent', 'Hours', 'Minutes', 'Seconds'])