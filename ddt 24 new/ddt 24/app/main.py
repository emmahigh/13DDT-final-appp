import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
#import sqlite for database functionality
import sqlite3
#import sqlite to work with files and folders
from pathlib import Path
from userSession import UserSession
from homePage import HomePage
from journalPage import JournalPage
from reflectionsPage import ReflectionsPage
from signupPage import SignupPage 
from loginPage import LoginPage
from calendarPage import CalendarPage 
import os
from pathlib import Path
import sv_ttk
from utils import create_button_image 
from ttkthemes import ThemedTk

class App(ThemedTk):
    def __init__(self):
        super().__init__()

        self.script_dir = Path(__file__).parent

        # Set the initial theme
        #self.tk.call("source", self.script_dir / "azure.tcl")
        #self.tk.call("set_theme", "light")

        #sv_ttk.set_theme("light")

        self.set_theme("breeze")

        self.title("Journal Application")
        self.geometry("800x600")

        #create a global variable to check whether the user is logged in
        self.logged_in = tk.BooleanVar(value=False)  # Default to False for example

        self.logged_in.trace_add("write", self.update_button_state)

        self.create_database()

        self.create_widgets()

    def create_database(self):
        # Connect to the database 

        Path(self.script_dir / "database").mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.script_dir / "database" / "database.db")

        # Create a cursor object
        cursor = conn.cursor()

        # Create a table for user data
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL
        )
        ''')

        # Create a table for journal data
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            entry TEXT NOT NULL,
            username TEXT NOT NULL
        )
        ''')

        # Create a table for reflections data
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS reflection (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            grateful TEXT NOT NULL,
            high TEXT NOT NULL,
            low TEXT NOT NULL,
            plans TEXT NOT NULL,
            username TEXT NOT NULL
        )
        ''')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    def create_widgets(self):
        global logged_in
        # Configure the main frame to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create the main frame
        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure the main frame to expand
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Create the sidebar frame
        sidebar_frame = ttk.Frame(main_frame, width=50, )
        sidebar_frame.grid(row=0, column=0, sticky="ns")

        # Create the content frame
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        
        # Add buttons to the sidebar
        self.home_image=create_button_image(self.script_dir / "img/home.png")
        btn_home = ttk.Button(sidebar_frame, width=10,text="Homepage", image=self.home_image, compound="left", style='Flat.TButton', command=self.show_homepage)
        btn_home.pack(fill=tk.X, pady=5,)
        
       
        self.journal_image=create_button_image(self.script_dir / "img/journal.png")
        self.btn_journal = ttk.Button(sidebar_frame, text="Journal", image=self.journal_image, compound="left", style='Flat.TButton', state=tk.DISABLED, command=self.show_journal)
        self.btn_journal.pack(fill=tk.X, pady=5)

        self.reflections_image=create_button_image(self.script_dir / "img/reflections.png")
        self.btn_reflections = ttk.Button(sidebar_frame, text="Reflections", image=self.reflections_image, compound="left", style='Flat.TButton', state=tk.DISABLED, command=self.show_reflections)
        self.btn_reflections.pack(fill=tk.X, pady=5)

        self.calendar_image=create_button_image(self.script_dir / "img/calendar2.png")
        self.btn_calendar = ttk.Button(sidebar_frame, text="Calendar",image=self.calendar_image, compound="left", style='Flat.TButton', state=tk.DISABLED, command=self.show_calendar)
        self.btn_calendar.pack(fill=tk.X, pady=5)
        
        
        self.login_image=create_button_image(self.script_dir / "img/login.png")
        self.btn_login = ttk.Button(sidebar_frame, text="Login",image=self.login_image, compound="left", command=self.show_login)
        self.btn_login.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        self.signup_image=create_button_image(self.script_dir / "img/signup.png")
        self.btn_signup = ttk.Button(sidebar_frame, text="Signup",image=self.signup_image, compound="left", command=self.show_signup)
        self.btn_signup.pack(side=tk.BOTTOM,fill=tk.X, pady=5)
        

        self.user_image = create_button_image(self.script_dir / "img/user.png")
        self.btn_logout = ttk.Button(sidebar_frame, text="Log out", image=self.user_image, compound="left", style='Flat.TButton', command=self.logout)
    
        self.btn_logout.pack_forget()

        self.label_welcome = tk.Label(sidebar_frame, text="Welcome!")
        
        self.label_welcome.pack_forget()

        # Display the initial content
        self.show_homepage()

    def create_button_image(self, image_file):
        img_btn = Image.open(image_file)
        img_btn = img_btn.resize((24, 24), Image.Resampling.LANCZOS) 
        img_btn = ImageTk.PhotoImage(img_btn)
        return img_btn
    
    def show_page(self, page_class):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        page = page_class(self.content_frame, self)
        page.pack(fill=tk.BOTH, expand=True)

    def open_login_window(self):
       login_window = tk.Toplevel(self)
       login_window.title("Login")
       login_window.geometry("400x300")

       # Create the login page inside the new window
       login_page = LoginPage(login_window, self)
       login_page.pack(fill=tk.BOTH, expand=True)

    def show_homepage(self):
        self.show_page(HomePage)

    def show_journal(self):
        self.show_page(JournalPage)

    def show_reflections(self):
        self.show_page(ReflectionsPage)
    
    def show_signup(self):
        self.show_page(SignupPage)
    
    def show_calendar(self):
        self.show_page(CalendarPage)

    def show_login(self):
        self.open_login_window()

    def logout(self):
        self.show_homepage()
        self.logged_in.set(False)

    def update_button_state(self, *args):
        # Update the button state based on the global variable
        if self.logged_in.get() == False:
            self.btn_reflections.config(state=tk.DISABLED)
            self.btn_journal.config(state=tk.DISABLED)
            self.btn_calendar.config(state=tk.DISABLED)
            self.btn_login.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
            self.btn_signup.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
            self.btn_logout.pack_forget()
            self.label_welcome.pack_forget()
        else:
            session = UserSession()
            self.user = session.get_user()
            self.btn_reflections.config(state=tk.NORMAL)
            self.btn_journal.config(state=tk.NORMAL)
            self.btn_calendar.config(state=tk.NORMAL)
            self.btn_login.pack_forget()
            self.btn_signup.pack_forget()
            self.btn_logout.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
            self.label_welcome.config(text=f"Welcome {self.user.firstname}!")
            self.label_welcome.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

app = App()

app.mainloop()
