# Updated owner_panel.py with Booking Approval/Reject Feature

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "hotel.db"

# ----------------------------------------
# Data Functions
# ----------------------------------------


def get_owner_hotels(owner_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "SELECT hotel_id, name, location, is_approved FROM hotels WHERE owner_id = ?", (owner_id,))
    hotels = cur.fetchall()
    conn.close()
    return hotels


def get_owner_bookings(owner_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        SELECT b.booking_id, u.name, h.name, r.type, b.check_in, b.check_out, b.status
        FROM bookings b
        JOIN users u ON b.user_id = u.user_id
        JOIN rooms r ON b.room_id = r.room_id
        JOIN hotels h ON r.hotel_id = h.hotel_id
        WHERE h.owner_id = ?
    ''', (owner_id,))
    data = cur.fetchall()
    conn.close()
    return data


def approve_booking(booking_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "UPDATE bookings SET status = 'approved' WHERE booking_id = ?", (booking_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", f"Booking ID {booking_id} approved.")


def reject_booking(booking_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "UPDATE bookings SET status = 'rejected' WHERE booking_id = ?", (booking_id,))
    # free the room
    cur.execute(
        "SELECT room_id FROM bookings WHERE booking_id = ?", (booking_id,))
    room = cur.fetchone()
    if room:
        cur.execute(
            "UPDATE rooms SET is_available = 1 WHERE room_id = ?", (room[0],))
    conn.commit()
    conn.close()
    messagebox.showinfo("Rejected", f"Booking ID {booking_id} rejected.")

# ----------------------------------------
# Hotel/Room Functions
# ----------------------------------------


def add_hotel(name, location, owner_id):
    if not name or not location:
        messagebox.showwarning(
            "Input Error", "Hotel name and location are required.")
        return
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO hotels (name, location, owner_id) VALUES (?, ?, ?)",
                (name, location, owner_id))
    conn.commit()
    conn.close()
    messagebox.showinfo(
        "Success", "Hotel added successfully. Awaiting admin approval.")


def add_room(hotel_id, room_type, price):
    if not room_type or not price:
        messagebox.showwarning(
            "Input Error", "Room type and price are required.")
        return
    try:
        price = float(price)
    except ValueError:
        messagebox.showwarning("Input Error", "Price must be a number.")
        return
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO rooms (hotel_id, type, price) VALUES (?, ?, ?)",
                (hotel_id, room_type, price))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Room added successfully.")

# ----------------------------------------
# GUI Helpers
# ----------------------------------------


def show_add_hotel_window(owner_id, refresh_callback):
    win = tk.Toplevel()
    win.title("Add Hotel")
    win.geometry("300x200")

    tk.Label(win, text="Hotel Name").pack()
    name_entry = tk.Entry(win)
    name_entry.pack()

    tk.Label(win, text="Location").pack()
    loc_entry = tk.Entry(win)
    loc_entry.pack()

    def on_add():
        add_hotel(name_entry.get(), loc_entry.get(), owner_id)
        win.destroy()
        refresh_callback()

    tk.Button(win, text="Add Hotel", command=on_add).pack(pady=10)


def show_add_room_window(hotel_id):
    win = tk.Toplevel()
    win.title("Add Room")
    win.geometry("300x200")

    tk.Label(win, text="Room Type").pack()
    type_entry = tk.Entry(win)
    type_entry.pack()

    tk.Label(win, text="Price").pack()
    price_entry = tk.Entry(win)
    price_entry.pack()

    def on_add():
        add_room(hotel_id, type_entry.get(), price_entry.get())
        win.destroy()

    tk.Button(win, text="Add Room", command=on_add).pack(pady=10)

# ----------------------------------------
# MAIN PANEL
# ----------------------------------------


def show_owner_panel(owner):
    root = tk.Tk()
    root.title("Hotel Owner Panel")
    root.geometry("750x600")

    tk.Label(root, text=f"Welcome {owner[1]} (Owner)", font=(
        "Arial", 14)).pack(pady=10)

    # ----------- Hotel Table -----------
    tk.Label(root, text="Your Hotels").pack()
    hotel_tree = ttk.Treeview(root, columns=(
        'ID', 'Name', 'Location', 'Approved'), show='headings')
    for col in ('ID', 'Name', 'Location', 'Approved'):
        hotel_tree.heading(col, text=col)
    hotel_tree.pack(pady=5, fill='x')

    def refresh_hotels():
        for i in hotel_tree.get_children():
            hotel_tree.delete(i)
        for h in get_owner_hotels(owner[0]):
            approved = "Yes" if h[3] else "No"
            hotel_tree.insert('', 'end', values=(h[0], h[1], h[2], approved))

    def on_add_hotel():
        show_add_hotel_window(owner[0], refresh_hotels)

    def on_add_room():
        selected = hotel_tree.selection()
        if selected:
            hotel_id = hotel_tree.item(selected[0])['values'][0]
            show_add_room_window(hotel_id)
        else:
            messagebox.showwarning(
                "Select Hotel", "Please select a hotel first!!")

    tk.Button(root, text="Add Hotel", command=on_add_hotel).pack(pady=2)
    tk.Button(root, text="Add Room to Selected Hotel",
              command=on_add_room).pack(pady=2)

    # ----------- Booking Approval Section -----------
    tk.Label(root, text="Room Booking Requests").pack(pady=10)
    booking_tree = ttk.Treeview(root, columns=(
        'ID', 'User', 'Hotel', 'Room', 'CheckIn', 'CheckOut', 'Status'), show='headings')
    for col in ('ID', 'User', 'Hotel', 'Room', 'CheckIn', 'CheckOut', 'Status'):
        booking_tree.heading(col, text=col)
    booking_tree.pack(pady=5, fill='both', expand=True)

    def refresh_bookings():
        for i in booking_tree.get_children():
            booking_tree.delete(i)
        for b in get_owner_bookings(owner[0]):
            booking_tree.insert('', 'end', values=b)

    def on_approve_booking():
        selected = booking_tree.selection()
        if selected:
            booking_id = booking_tree.item(selected[0])['values'][0]
            approve_booking(booking_id)
            refresh_bookings()

    def on_reject_booking():
        selected = booking_tree.selection()
        if selected:
            booking_id = booking_tree.item(selected[0])['values'][0]
            reject_booking(booking_id)
            refresh_bookings()

    tk.Button(root, text="✅Approve Selected Booking",
              command=on_approve_booking).pack(pady=2)
    tk.Button(root, text="❌Reject Selected Booking",
              command=on_reject_booking).pack(pady=2)

    def on_exit():
        from login_register import show_login_register
        root.destroy()
        show_login_register()

    tk.Button(root, text="Exit", command=on_exit).pack(pady=10)

    refresh_hotels()
    refresh_bookings()
    root.mainloop()
