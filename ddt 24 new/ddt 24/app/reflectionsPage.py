import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from tkcalendar import DateEntry
import os
from pathlib import Path
from userSession import UserSession
from utils import create_button_image
  
class ReflectionsPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.script_dir = Path(__file__).parent

        session = UserSession()
        self.user = session.get_user()

        #Create a frame to hold everything
        self.wrapper = tk.Frame(self)
        #Create a canvas in the frame as a frame doesn't support scrolling
        self.canvas = tk.Canvas(self.wrapper)
        #Make the canvas the width of the screen
        self.canvas.pack(side="left", fill="both", expand=True)

        #Add a scrollbar and set it's command to change the canvas view size
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        #Link the scrollbar to the canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)

        #Create a Frame to add the widgets to and scroll
        self.scrollable_frame = tk.Frame(self.canvas)
        #Add the Frame into the canvas as a window
        self.canvas_frame = self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")

        #Set the events on the frame and canvas to control the widgets expanding
        self.scrollable_frame.bind("<Configure>", self.OnFrameConfigure)
        self.canvas.bind('<Configure>', self.FrameWidth)

        #Add the wrapper frame
        self.wrapper.pack(fill="both", expand=True, padx=10, pady=10)

        label_reflection_date = ttk.Label(
            font="arial",
            text="Reflection date",
            master=self.scrollable_frame
        )
        label_reflection_date.pack(fill=tk.X, pady=5)

        # Create a StringVar to hold the text in the Entry widget
        self.entry_reflection_date_text = tk.StringVar()
       
        self.entry_reflection_date = DateEntry(
            font="arial",
            text="Reflections Date DD/MM/YY",
            date_pattern='dd/mm/yyyy',
            format='dd/mm/yyyy',
            master=self.scrollable_frame,
            textvariable=self.entry_reflection_date_text
        )
        self.entry_reflection_date.pack(fill=tk.X, pady=5, expand=True)
        
        # The callback function to the StringVar using the trace method
        self.entry_reflection_date_text.trace_add("write", self.on_date_entry_change)

        label_grateful = ttk.Label(
            font="arial",
            text="Today I am grafeful for...",
            master=self.scrollable_frame
        )
        label_grateful.pack(fill=tk.X, pady=5)

        self.text_grateful = tk.Text(
            master=self.scrollable_frame,
            borderwidth=1, relief="sunken",
            height=10
        )
        self.text_grateful.pack(fill=tk.BOTH, pady=5, expand=True)
       
        label_high = ttk.Label(
            font="arial",
            text="My high of today was...",
            master=self.scrollable_frame
        )
        label_high.pack(fill=tk.X, pady=5)

        self.text_high = tk.Text(
            master=self.scrollable_frame,
            borderwidth=1, relief="sunken",
            height=10
        )
        self.text_high.pack(fill=tk.BOTH, pady=5, expand=True)
        
        label_low = ttk.Label(
            font="arial",
            text="My low of today was...",
            master=self.scrollable_frame
        )
        label_low.pack(fill=tk.X, pady=5)

        self.text_low = tk.Text(
            master=self.scrollable_frame,
            borderwidth=1, relief="sunken",
            height=10
        )
        self.text_low.pack(fill=tk.BOTH, pady=5, expand=True)

        label_plans = ttk.Label(
            font="arial",
            text="What are my plans for tomorrow...",
            master=self.scrollable_frame
        )
        label_plans.pack(fill=tk.X, pady=5)

        self.text_plans = tk.Text(
            master=self.scrollable_frame,
            borderwidth=1, relief="sunken",
            height=10
        )
        self.text_plans.pack(fill=tk.BOTH, pady=5, expand=True)

        self.save_image = create_button_image(self.script_dir / "img/save.png")
        self.btn_submit = ttk.Button(self.scrollable_frame, text="Save", image=self.save_image, compound="left", style='Flat.TButton', command=self.save)
        self.btn_submit.pack(pady=20)

        #Do a search of the reflection for the current date
        self.search_reflection()

    def FrameWidth(self, event):
      new_width = event.width - 4  
      new_height = event.height - 4

      # The new dimensions are not smaller than the scrollable frame's minimum size
      min_width = self.scrollable_frame.winfo_reqwidth()
      min_height = self.scrollable_frame.winfo_reqheight()
      new_width = max(new_width, min_width)
      new_height = max(new_height, min_height)

      self.canvas.itemconfig(self.canvas_frame, width=new_width, height=new_height)

    def OnFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Function to save user data
    def save(self):
        date = self.entry_reflection_date.get()
        grateful = self.text_grateful.get("1.0", tk.END)
        high = self.text_high.get("1.0", tk.END)
        low = self.text_low.get("1.0", tk.END)
        plans = self.text_plans.get("1.0", tk.END)
        
        if date and grateful and high and low and plans:
            conn = sqlite3.connect(self.script_dir / "database/database.db")
            cursor = conn.cursor()
            
            try:
                #Try to find the journal entry
                print(f"Username = {self.user.username}")
                cursor.execute('''
                SELECT * FROM reflection WHERE date = ? AND username = ?
                ''', (date,self.user.username))
                reflection = cursor.fetchone()
                if reflection:
                    cursor.execute('''
                    UPDATE reflection SET grateful = ?, high = ?, low = ?, plans = ? WHERE date = ? AND username = ?
                    ''', (grateful, high, low, plans, date, self.user.username))
                    conn.commit()
                else:    
                    cursor.execute('''
                    INSERT INTO reflection (date, grateful, high, low, plans, username) VALUES (?, ?, ?, ?, ?, ?)
                    ''', (date, grateful, high, low, plans, self.user.username))
                    conn.commit()
                messagebox.showinfo("Success", "Save successful!")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "Please enter all fields")

    def on_date_entry_change(self, *args):
        self.search_reflection()

    def search_reflection(self):
        # Get the current value of the Entry widget
        date = self.entry_reflection_date_text.get()
        print(f"Entry value changed: {date}")

        conn = sqlite3.connect(self.script_dir / "database/database.db")
        cursor = conn.cursor()

        cursor.execute('''
        SELECT * FROM reflection WHERE date = ? AND username = ?
        ''', (date,self.user.username))
        reflection = cursor.fetchone()
        if reflection:
            print(f"Test = {reflection[2]}")
            self.set_text(self.text_grateful, reflection[2])
            self.set_text(self.text_high, reflection[3])
            self.set_text(self.text_low, reflection[4])
            self.set_text(self.text_plans, reflection[5])
        else:
            self.text_grateful.delete("1.0", tk.END)
            self.text_high.delete("1.0", tk.END)
            self.text_low.delete("1.0", tk.END)
            self.text_plans.delete("1.0", tk.END)

    def set_text(self, text_entry, text):
        # Clear the current text in the Text widget
        text_entry.delete("1.0", tk.END)
        
        # Insert new text at the beginning
        text_entry.insert("1.0", text)

