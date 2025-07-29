# utils.py
import sqlite3
import re
from tkinter import messagebox

DB_NAME = "hotel.db"

# ----------------------
# 1. USER AUTH FUNCTIONS
# ----------------------

def login_user(email, password):
    """Verifies user credentials and returns user tuple or None."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cur.fetchone()
    conn.close()
    return user

def register_user(name, email, password, role):
    """Registers a new user after basic validation."""
    if not name or not email or not password:
        messagebox.showerror("Error", "All fields are required.")
        return None

    if not is_valid_email(email):
        messagebox.showerror("Error", "Invalid email format.")
        return None

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                    (name, email, password, role))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
        return cur.lastrowid
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Email already exists.")
        return None
    finally:
        conn.close()

# ----------------------
# 2. VALIDATION HELPERS
# ----------------------

def is_valid_email(email):
    """Returns True if email matches pattern."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def is_strong_password(password):
    """Check for strong password: min 6 chars (add more rules if needed)."""
    return len(password) >= 6

# ----------------------
# 3. SESSION-LIKE UTILITY
# ----------------------

current_user = None  # Can be updated after login, if needed

def set_current_user(user):
    global current_user
    current_user = user

def get_current_user():
    return current_user
