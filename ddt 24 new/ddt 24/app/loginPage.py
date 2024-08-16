import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from user import User
from userSession import UserSession
import os
from pathlib import Path
  
class LoginPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.script_dir = Path(__file__).parent

        self.app = app
        # Username label and entry
        self.label_username = tk.Label(self, text="Username")
        self.label_username.pack(pady=5)
        self.entry_username = tk.Entry(self)
        self.entry_username.pack(pady=5)

        # Password label and entry
        self.label_password = tk.Label(self, text="Password")
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=5)

        # Signup button
        self.btn_login = tk.Button(self, text="Login", command=self.login)
        self.btn_login.pack(pady=20)
    
    # Function to save user data
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if username and password:
            conn = sqlite3.connect(self.script_dir / 'database/database.db')
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                SELECT * FROM users WHERE username = ?
                ''', (username,))
                user = cursor.fetchone()
                if user:
                    if user[2] ==  password:
                        session = UserSession()
                        session.set_user(User(user[1], user[3], user[4]))
                        self.app.logged_in.set(True)
                        self.app.show_homepage()

                        self.master.destroy() 
                    else:
                        messagebox.showinfo("Error", "Login unsuccessful!")    
                else:
                    messagebox.showinfo("Error", "Login unsuccessful!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "Please enter both username and password")


        