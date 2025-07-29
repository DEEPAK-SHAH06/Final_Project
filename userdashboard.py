import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "hotel.db"

def fetch_approved_hotels():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT hotel_id, name, location FROM hotels WHERE is_approved = 1")
    hotels = cur.fetchall()
    conn.close()
    return hotels

def search_hotels(query):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT hotel_id, name, location 
        FROM hotels 
        WHERE is_approved = 1 AND 
              (name LIKE ? OR location LIKE ?)""", 
              (f"%{query}%", f"%{query}%"))
    hotels = cur.fetchall()
    conn.close()
    return hotels

def fetch_available_rooms(hotel_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT room_id, type, price FROM rooms WHERE hotel_id = ? AND is_available = 1", (hotel_id,))
    rooms = cur.fetchall()
    conn.close()
    return rooms

def book_room(user_id, room_id, check_in, check_out):
    if not (check_in and check_out):
        messagebox.showerror("Error", "Check-in and Check-out dates are required.")
        return
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO bookings (user_id, room_id, check_in, check_out, status) VALUES (?, ?, ?, ?, 'pending')",
                (user_id, room_id, check_in, check_out))
    cur.execute("UPDATE rooms SET is_available = 0 WHERE room_id = ?", (room_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Booking Request Sent successfully!")

def show_rooms_window(user_id, hotel_id):
    room_win = tk.Toplevel()
    room_win.title("Available Rooms")
    room_win.geometry("400x300")

    rooms = fetch_available_rooms(hotel_id)
    if not rooms:
        tk.Label(room_win, text="No available rooms.").pack(pady=10)
        return

    tree = ttk.Treeview(room_win, columns=('Room ID', 'Type', 'Price'), show='headings')
    tree.heading('Room ID', text='Room ID')
    tree.heading('Type', text='Type')
    tree.heading('Price', text='Price')
    for room in rooms:
        tree.insert('', 'end', values=room)
    tree.pack(pady=10)

    tk.Label(room_win, text="Check-in:").pack()
    check_in_entry = tk.Entry(room_win)
    check_in_entry.pack()

    tk.Label(room_win, text="Check-out:").pack()
    check_out_entry = tk.Entry(room_win)
    check_out_entry.pack()

    def on_book():
        selected = tree.selection()
        if selected:
            room_id = tree.item(selected[0])['values'][0]
            book_room(user_id, room_id, check_in_entry.get(), check_out_entry.get())
            room_win.destroy()
        else:
            messagebox.showwarning("Select Room", "Please select a room first.")

    tk.Button(room_win, text="Book Room", command=on_book).pack(pady=10)

def show_user_dashboard(user):
    dash = tk.Tk()
    dash.title("User Dashboard")
    dash.geometry("600x500")
    dash.configure(bg="#f5f5f5")

    tk.Label(dash, text=f"Welcome {user[1]}!", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=10)
    tk.Label(dash, text="Search Hotel by Name or Location", bg="#f5f5f5", font=("Arial", 11)).pack()

    search_entry = tk.Entry(dash, width=40)
    search_entry.pack(pady=5)

    tree = ttk.Treeview(dash, columns=('Hotel ID', 'Name', 'Location'), show='headings')
    tree.heading('Hotel ID', text='Hotel ID')
    tree.heading('Name', text='Hotel Name')
    tree.heading('Location', text='Location')
    tree.pack(pady=10, fill='both', expand=True)

    def load_hotels(hotels):
        tree.delete(*tree.get_children())
        for hotel in hotels:
            tree.insert('', 'end', values=hotel)

    def on_search():
        query = search_entry.get().strip()
        if query:
            hotels = search_hotels(query)
        else:
            hotels = fetch_approved_hotels()
        load_hotels(hotels)

    def on_view_rooms():
        selected = tree.selection()
        if selected:
            hotel_id = tree.item(selected[0])['values'][0]
            show_rooms_window(user[0], hotel_id)
        else:
            messagebox.showwarning("Select Hotel", "Please select a hotel first.")

    def on_exit():
        from login_register import show_login_register
        dash.destroy()
        show_login_register()

    tk.Button(dash, text="Search", command=on_search, width=20, bg="#2196F3", fg="black").pack(pady=2)
    tk.Button(dash, text="View Rooms", command=on_view_rooms, width=20, bg="#4CAF50", fg="black").pack(pady=2)
    tk.Button(dash, text="Exit", command=on_exit, width=20, bg="#f44336", fg="black").pack(pady=10)

    load_hotels(fetch_approved_hotels())
    dash.mainloop()
