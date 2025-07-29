# main.py
import tkinter as tk
from tkinter import messagebox
from login_register import *
from db import create_tables

def open_login_window():
    show_login_register()

# Initialize main window
root = tk.Tk()
root.title("Hotel Management System")
root.geometry("450x350")
root.configure(bg="#f0f4f7")  # light blue/gray background

create_tables()

# Header Frame
header = tk.Frame(root, bg="#3e64ff", height=80)
header.pack(fill='x')

tk.Label(header, text="🏨 Hotel Booking System", bg="#3e64ff", fg="white",
         font=("Helvetica", 18, "bold")).pack(pady=20)

# Main Content
content = tk.Frame(root, bg="#f0f4f7")
content.pack(expand=True)

tk.Label(content, text="Welcome! Book your perfect stay.",
         font=("Arial", 13), bg="#f0f4f7", fg="#333").pack(pady=25)

tk.Button(content, text="Login / Register", command=open_login_window,
          font=("Arial", 11), width=20, bg="#3e64ff", fg="white",
          relief="raised", bd=2).pack(pady=10)

tk.Label(content, text="Made with ❤️ in Python + Tkinter",
         font=("Arial", 9), bg="#f0f4f7", fg="#555").pack(side="bottom", pady=20)

root.mainloop()
