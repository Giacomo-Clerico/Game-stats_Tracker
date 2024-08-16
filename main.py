import tkinter as tk
from tkinter import ttk
import sqlite3
import json


user__name = "admin"
game__name = "generalGame"

conn = sqlite3.connect("game_stats.db")
cursor = conn.cursor()
# Create the users table
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
"""
)
conn.commit()
conn.close()


# Connect to the database
def connect_db():
    conn = sqlite3.connect("game_stats.db")
    return conn


def add_user(name):
    conn = connect_db()
    cursor = conn.cursor()
    tableName = name + "Games"
    cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS "
        + tableName
        + """(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
    )"""
    )
    conn.commit()
    conn.close()


# Load the JSON file
with open('fields.json', 'r') as file:
    fields = json.load(file)

# Extract the 'name' list (keys of the JSON)
names_list = list(fields.keys())


def fieldAdder(keys, sql_definitions):
    # Create an empty list to store the corresponding SQL columns
    columns_list = []
    message = ""

    for key in keys:
        # Get the corresponding SQL column definition from the sql_definitions dictionary
        column_definition = sql_definitions.get(key)
        if column_definition:
            columns_list.append(column_definition)

    message = ",\n\t".join(columns_list)
    # for i in columns_list:
    #     message += i + ",\n\t"

    # debug output
    # print(message)
    return message


# Optionally, create a list of 'name sql_description' strings
sql_definitions = fields


def add_game(fields):
    conn = connect_db()
    cursor = conn.cursor()
    userGameTableName = user__name + "Games"

    tableName = user__name + game__name
    # add the game name to the table that tracks the games for a specific user

    cursor.execute(
        "INSERT INTO " + userGameTableName +
        " (name) VALUES (?)", (game__name,)
    )

    # create the game table for the game
    fieldsForQuery = fieldAdder(fields, sql_definitions)
    tableQuery = f"""CREATE TABLE {tableName} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        {fieldsForQuery} );
    """
    # debug query
    # print(tableQuery)
    cursor.execute(tableQuery)
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


def fetch_games():
    conn = connect_db()
    cursor = conn.cursor()
    tableName = user__name + "Games"
    cursor.execute("SELECT name FROM " + tableName)
    games = [row[0] for row in cursor.fetchall()]
    conn.close()
    return games


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

    def switch_frameEntry(self, frame_class):
        new_frame = frame_class(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill=tk.BOTH, expand=True)


# Page 1: List of Users and Add User Entry
class UserListPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Label
        label = ttk.Label(self, text="User List", font=("Helvetica", 16))
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
        select_button = ttk.Button(
            self, text="Select User", command=self.select_user)
        select_button.pack(pady=10)

    def populate_listbox(self):
        names = fetch_names()
        for name in names:
            self.listbox.insert(tk.END, name)

    def add_user(self):
        user_name = self.new_user_entry.get()
        if user_name:  # Check if the entry is not empty
            global user__name
            user__name = user_name

            add_user(user_name)
            self.new_user_entry.delete(0, tk.END)
            self.listbox.insert(tk.END, user_name)
            self.master.switch_frame(UserPage)

    def select_user(self):
        selected_name = self.listbox.get(tk.ACTIVE)
        if selected_name:
            global user__name
            user__name = selected_name
            self.master.switch_frame(UserPage)


# Page 2: Next Page After User Selection or Addition
class UserPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        label = ttk.Label(self, text="Select game", font=("Helvetica", 16))
        label.pack(pady=10)

        # Listbox to display game names
        self.listbox = tk.Listbox(self, height=10, width=30)
        self.listbox.pack(pady=10)
        self.populate_listbox()

        # Entry box to add a new game
        self.new_user_entry = tk.Entry(self, width=25)
        self.new_user_entry.pack(pady=10)

        # Button to add a new game
        add_button = ttk.Button(self, text="Add Game", command=self.add_game)
        add_button.pack(pady=10)

        # Button to select a game and go to the next page
        select_button = ttk.Button(
            self, text="Select Game", command=self.select_game)
        select_button.pack(pady=10)

    def populate_listbox(self):
        games = fetch_games()
        for game in games:
            self.listbox.insert(tk.END, game)

    def select_game(self):
        selected_game = self.listbox.get(tk.ACTIVE)
        if selected_game:
            global game__name
            game__name = selected_game
            self.master.switch_frameEntry(GamePage)

    def add_game(self):
        game_name = self.new_user_entry.get()
        if game_name:  # Check if the entry is not empty
            global game__name
            game__name = game_name
            self.new_user_entry.delete(0, tk.END)
            self.master.switch_frame(CreateGamePage)


class CreateGamePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        label = ttk.Label(self, text="Create a new game",
                          font=("Helvetica", 16))
        label.pack(pady=10)

        self.checkbox_labels = []  # Store the labels of the checkboxes
        self.checkbox_vars = []

        # Database Fields Selection
        self.create_widgets()

    def create_widgets(self):
        # Options for checkboxes
        options = names_list

        # Create checkboxes within the CreateGamePage frame
        for option in options:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(self, text=option, variable=var)
            checkbox.pack(anchor="w")
            self.checkbox_vars.append(var)
            self.checkbox_labels.append(option)

        # Button to check which checkboxes are selected
        check_button = tk.Button(
            self, text="Check Selected", command=self.check_selected
        )
        check_button.pack()

    def check_selected(self):
        selected = [
            label
            for var, label in zip(self.checkbox_vars, self.checkbox_labels)
            if var.get()
        ]
        # debug checkbox output
        # print("Selected Checkboxes:", selected)
        add_game(selected)
        self.master.switch_frameEntry(GamePage)


class GamePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        columns = ['Name', 'Age', 'Email']
        self.columns = columns
        self.entries = {}

        label = ttk.Label(self, text="Add an entry",
                          font=("Helvetica", 16))
        label.pack(pady=10)

        self.create_entries()

    def create_entries(self):
        # Define starting coordinates
        x_position = 10
        y_position = 40

        for column_name in self.columns:
            # Create and place a Label
            label = tk.Label(self, text=column_name)
            label.place(x=x_position, y=y_position)

            # Create and place an Entry widget next to the Label
            entry = tk.Entry(self)
            entry.place(x=x_position + 100, y=y_position)

            # Store the Entry widget in the dictionary
            self.entries[column_name] = entry

            # Update y_position for the next row
            y_position += 30


# Run the application
if __name__ == "__main__":
    app = MainApp()
    # page = GamePage()
    # page.pack(fill=tk.BOTH, expand=True)
    app.mainloop()
