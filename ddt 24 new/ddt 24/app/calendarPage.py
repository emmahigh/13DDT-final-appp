import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime, timedelta
import sqlite3
import os
from pathlib import Path
from userSession import UserSession


class CalendarPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.script_dir = Path(__file__).parent

        session = UserSession()
        self.user = session.get_user()

        self.calendar = Calendar(self)
        self.calendar.pack(fill=tk.BOTH, expand=True)

        self.set_date_values()

    def set_date_values(self):
        first_date = self.get_first_displayed_date(self.calendar)

        for i, row in enumerate(self.calendar._calendar):
            for j, label in enumerate(row):
                cell_date = first_date + timedelta(days=i * 7 + j)
                has_reflection = self.get_reflection(cell_date)
                has_journal = self.get_journal(cell_date)
                
                # Get the text from the label (the day number)
                label_text=label.cget("text")

                print(f"Cell at Row {i}, Col {j}: Date = {cell_date}, Text = {label_text}")

                self.calendar._cal_frame.rowconfigure(i + 1, uniform=1)
                self.calendar._cal_frame.columnconfigure(j + 1, uniform=1)
                new_label_text = f'\n{label_text}'
                if has_journal:
                    new_label_text += f'\nJournal'
                if has_reflection:
                    new_label_text += f'\nReflection'
                label.configure(justify="center", anchor="n", padding=(1, 4), text=new_label_text)

    def get_reflection(self, date):
        conn = sqlite3.connect(self.script_dir / "database/database.db")
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM reflection WHERE date = ? AND username = ?
        ''', (date.strftime("%d/%m/%Y"),self.user.username))
        reflection = cursor.fetchone()
        if reflection:
            return True
        else:
            return False
    
    def get_journal(self, date):
        conn = sqlite3.connect(self.script_dir / "database/database.db")
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM journal WHERE date = ? AND username = ?
        ''', (date.strftime("%d/%m/%Y"),self.user.username))
        journal = cursor.fetchone()
        if journal:
            return True
        else:
            return False

    def get_first_displayed_date(self, cal):
        # Get the year and month displayed in the calendar
        month, year = cal.get_displayed_month()  # Returns a tuple (year, month)
        print(f"{year}-{month} type={type(month)}")
        
        # Find the first day of the displayed month
        first_day_of_month = datetime(year, month, 1)
        
        # Determine the weekday of the first day (0 = Monday, 6 = Sunday)
        first_day_weekday = first_day_of_month.weekday()
        
        # Calculate the first displayed date (including overflow from previous month)
        # Assuming Monday is the first day of the week 
        start_day_offset = (first_day_weekday - 0) % 7
        first_displayed_date = first_day_of_month - timedelta(days=start_day_offset)
        
        return first_displayed_date 