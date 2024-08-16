from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path
import sqlite3
from userSession import UserSession

class HomePage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.script_dir = Path(__file__).parent
        self.app = app

        session = UserSession()
        self.user = session.get_user()

        # Create a Canvas widget
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill='both', expand=True)  # Fill the whole frame and expand
        
        # Load and resize the image
        self.original_image = Image.open(self.script_dir / "img/logo.png")
        self.update_image()

        # Add the image to the canvas
        self.canvas.create_image(0, 0, anchor='nw', image=self.image)

        # Draw circles with initials
        self.draw_circles()

        # Update the image and circles when the window is resized
        self.bind("<Configure>", self._on_resize)

    def update_image(self):
        screen_width = self.winfo_width()
        screen_height = self.winfo_height()
        resized_image = self.original_image.resize((screen_width, screen_height), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(resized_image)

    def draw_circles(self):

        # Clear the canvas before drawing
        self.canvas.delete("all")
        
        # Draw the image on the canvas
        self.canvas.create_image(0, 0, anchor='nw', image=self.image)
        
        if self.app.logged_in.get() == False:
            return

        # Days of the week initials
        days = ['M', 'T', 'W', 'T', 'F', 'S', 'S']
        num_circles = len(days)
        radius = 25  # Radius of the circle
        margin = 7  # Margin between circles
        
        canvas_width = self.winfo_width()
        canvas_height = self.winfo_height()
        
        # Calculate total width required for circles and margin
        total_width = num_circles * (2 * radius + margin) - margin
        start_x = (canvas_width - total_width) // 2
        y = canvas_height - radius - 20  # Position circles near the bottom with some padding
        
        # Calculate the current date and the start of the week
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())  # Monday as the start of the week

        for i, day in enumerate(days):
            # Calculate the date for each day of the week
            day_date = start_of_week + timedelta(days=i)
            # Call method with the date
            has_entry = self.handle_day_date(day_date)
            
            x = start_x + i * (2 * radius + margin) + radius
            # Draw circle
            if has_entry:
                self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline='blue', fill="blue", width=2)
                # Draw text in the middle of the circle
                self.canvas.create_text(x, y, text=day, fill='white', font=('Helvetica', 16, 'bold'))
            else:
                self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline='blue', width=2)
                # Draw text in the middle of the circle
                self.canvas.create_text(x, y, text=day, fill='black', font=('Helvetica', 16, 'bold'))
            

    def handle_day_date(self, date):
        # method that does something with the date
        has_reflection = self.get_reflection(date)
        has_journal = self.get_journal(date)
        if has_reflection or has_journal:
            return True
        else:    
            return False 

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

    def _on_resize(self, event):
        self.update_image()
        self.draw_circles()
