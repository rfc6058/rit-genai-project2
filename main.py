import tkinter as tk
import sqlite3
from tkinter import messagebox

# Create a database connection
conn = sqlite3.connect('passwords.db')
c = conn.cursor()

# Create the passwords table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS passwords
             (website text, username text, password text)''')

# Function to save a password
def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    # Insert the password into the database
    c.execute("INSERT INTO passwords VALUES (?, ?, ?)", (website, username, password))
    conn.commit()

    messagebox.showinfo("Success", "Password saved successfully!")

    # Clear the input fields
    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def create_password_manager():
    # Create the main window
    window = tk.Tk()
    window.title("Password Manager")

    # Create the labels
    website_label = tk.Label(window, text="Website:")
    website_label.pack()
    username_label = tk.Label(window, text="Username:")
    username_label.pack()
    password_label = tk.Label(window, text="Password:")
    password_label.pack()

    # Create the entry fields
    website_entry = tk.Entry(window)
    website_entry.pack()
    username_entry = tk.Entry(window)
    username_entry.pack()
    password_entry = tk.Entry(window, show="*")
    password_entry.pack()

    # Create the save button
    save_button = tk.Button(window, text="Save", command=save_password)
    save_button.pack()

    # Start the main loop
    window.mainloop()

create_password_manager()
