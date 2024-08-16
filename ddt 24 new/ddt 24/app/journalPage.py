import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import os
from pathlib import Path
from tkcalendar import DateEntry
from userSession import UserSession
from utils import create_button_image

class JournalPage(ttk.Frame):
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

        self.label_journal_date = ttk.Label(
            font="arial",
            text="Journal Date DD/MM/YY",
            master=self.scrollable_frame
        )
        self.label_journal_date.pack(side="top", anchor="w", pady=5)
         # Create a StringVar to hold the text in the Entry widget
        self.entry_journal_date_text = tk.StringVar()
       
        self.entry_journal_date = DateEntry(
            font="arial",
            text="Journal Date DD/MM/YY",
            date_pattern='dd/mm/yyyy',
            master=self.scrollable_frame,
            textvariable=self.entry_journal_date_text
        )
        self.entry_journal_date.pack(side="top", fill=tk.X, pady=5, expand=False)
        
        # Attach the callback function to the StringVar using the trace method
        self.entry_journal_date_text.trace_add("write", self.on_date_entry_change)

        self.label_journal = ttk.Label(
            font="arial",
            text="Journal Entry",
            master=self.scrollable_frame
        )
        self.label_journal.pack(side="top", anchor="w", pady=5)

        self.entry_journal_text = tk.Text(
            borderwidth=1, relief="sunken",
            master=self.scrollable_frame
        )
        self.entry_journal_text.pack(side="top", fill=tk.X, pady=5)

        self.save_image = create_button_image(self.script_dir / "img/save.png")
        self.btn_submit = ttk.Button(self.scrollable_frame, text="Save", image=self.save_image, compound="left", style='Flat.TButton', command=self.save)
        self.btn_submit.pack(side="top", pady=20)

        self.search_journal()

    def FrameWidth(self, event):
      new_width = event.width - 4  # Adjust for padding 
      new_height = event.height - 4

     
      min_width = self.scrollable_frame.winfo_reqwidth()
      min_height = self.scrollable_frame.winfo_reqheight()
      new_width = max(new_width, min_width)
      new_height = max(new_height, min_height)

      self.canvas.itemconfig(self.canvas_frame, width=new_width, height=new_height)

    def OnFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Function to save user data
    def save(self):
        date = self.entry_journal_date.get()
        entry = self.entry_journal_text.get("1.0", tk.END)
        
        if date and entry:
            conn = sqlite3.connect(self.script_dir / 'database/database.db')
            cursor = conn.cursor()
            
            try:
                #Find the journal entry
                cursor.execute('''
                SELECT * FROM journal WHERE date = ? AND username = ?
                ''', (date, self.user.username))
                journal = cursor.fetchone()
                if journal:
                    cursor.execute('''
                    UPDATE journal SET entry = ? WHERE date = ? AND username = ?
                    ''', (entry, date, self.user.username))
                    conn.commit()
                else:    
                    cursor.execute('''
                    INSERT INTO journal (date, entry, username) VALUES (?, ?, ?)
                    ''', (date, entry, self.user.username))
                    conn.commit()
                messagebox.showinfo("Success", "Save successful!")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "Please enter both date and an entry")
    
    def on_date_entry_change(self, *args):
        self.search_journal()

    def search_journal(self):
        # Get the current value of the Entry widget
        date = self.entry_journal_date_text.get()
        print(f"Entry value changed: {date}")

        conn = sqlite3.connect(self.script_dir / "database/database.db")
        cursor = conn.cursor()

        cursor.execute('''
        SELECT * FROM journal WHERE date = ? AND username = ?
        ''', (date,self.user.username))
        journal = cursor.fetchone()
        if journal:
            print(f"Test = {journal[2]}")
            self.set_text(self.entry_journal_text, journal[2])
        else:
            self.entry_journal_text.delete("1.0", tk.END)
      

    def set_text(self, text_entry, text):
        # Clear the current text in the Text widget
        text_entry.delete("1.0", tk.END)
        
        # Insert new text at the beginning
        text_entry.insert("1.0", text)

