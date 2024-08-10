import tkinter as tk
from tkinter import ttk
import sqlite3

global user__name

conn = sqlite3.connect('game_stats.db')
cursor = conn.cursor()
# Create the users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
''')
conn.commit()
conn.close()


# Connect to the database
def connect_db():
    conn = sqlite3.connect('game_stats.db')
    return conn


def add_user(name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()


# Fetch usernames from the database
def fetch_names():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users")
    names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return names


# Main Application
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("User selection")
        self.geometry("300x400")

        self.current_frame = None
        self.switch_frame(UserListPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack()


# Page 1: List of Users and Add User Entry
class UserListPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Label
        label = ttk.Label(self, text="User List", font=('Helvetica', 16))
        label.pack(pady=10)

        # Listbox to display user names
        self.listbox = tk.Listbox(self, height=10, width=30)
        self.listbox.pack(pady=10)
        self.populate_listbox()

        # Entry box to add a new user
        self.new_user_entry = tk.Entry(self, width=25)
        self.new_user_entry.pack(pady=10)

        # Button to add a new user
        add_button = ttk.Button(self, text="Add User", command=self.add_user)
        add_button.pack(pady=10)

        # Button to select a user and go to the next page
        select_button = ttk.Button(self, text="Select User", command=self.select_user)
        select_button.pack(pady=10)

    def populate_listbox(self):
        names = fetch_names()
        for name in names:
            self.listbox.insert(tk.END, name)

    def add_user(self):
        user_name = self.new_user_entry.get()
        if user_name:  # Check if the entry is not empty
            add_user(user_name)
            self.new_user_entry.delete(0, tk.END)
            self.listbox.insert(tk.END, user_name)
            self.master.switch_frame(UserPage)
            user__name = user_name

    def select_user(self):
        selected_name = self.listbox.get(tk.ACTIVE)
        if selected_name:
            self.master.switch_frame(UserPage)
            user__name = selected_name


# Page 2: Next Page After Selection or Addition
class UserPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        label = ttk.Label(self, text="Next Page", font=('Helvetica', 16))
        label.pack(pady=10)




# Run the application
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()