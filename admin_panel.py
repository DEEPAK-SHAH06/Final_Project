import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "hotel.db"


# Database functions (unchanged)
def get_pending_hotels():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT hotel_id, name, location FROM hotels WHERE is_approved = 0")
    data = cur.fetchall()
    conn.close()
    return data

def get_all_hotels():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT hotel_id, name, location, is_approved FROM hotels")
    data = cur.fetchall()
    conn.close()
    return data

def get_all_bookings():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        SELECT b.booking_id, u.name, h.name, r.type, b.check_in, b.check_out, b.status
        FROM bookings b
        JOIN users u ON b.user_id = u.user_id
        JOIN rooms r ON b.room_id = r.room_id
        JOIN hotels h ON r.hotel_id = h.hotel_id
    ''')
    data = cur.fetchall()
    conn.close()
    return data

def get_user_bookings_by_email(email):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        SELECT b.booking_id, u.name, h.name, r.type, b.check_in, b.check_out, b.status
        FROM bookings b
        JOIN users u ON b.user_id = u.user_id
        JOIN rooms r ON b.room_id = r.room_id
        JOIN hotels h ON r.hotel_id = h.hotel_id
        WHERE u.email = ?
    ''', (email,))
    data = cur.fetchall()
    conn.close()
    return data

def approve_hotel(hotel_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE hotels SET is_approved = 1 WHERE hotel_id = ?", (hotel_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Hotel Approved", f"Hotel ID {hotel_id} approved!")

def reject_hotel(hotel_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM hotels WHERE hotel_id = ?", (hotel_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Hotel Rejected", f"Hotel ID {hotel_id} deleted!")

def update_hotel(hotel_id, name, location):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE hotels SET name = ?, location = ? WHERE hotel_id = ?", (name, location, hotel_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Hotel Updated", "Hotel details updated.")


# Admin Panel UI
def show_admin_panel(admin_user):
    root = tk.Tk()
    root.title("Admin Panel")
    root.geometry("900x650")
    root.configure(bg="#f1f3f6")

    title = tk.Label(root, text=f"Welcome {admin_user[1]} (Admin)", font=("Helvetica", 16, "bold"), bg="#3E64FF", fg="white", pady=10)
    title.pack(fill="x")

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
    style.configure("Treeview", font=("Arial", 10), rowheight=25)

    # ---------- Tab 1: Pending Hotels ----------
    tab1 = tk.Frame(notebook, bg="#ffffff")
    notebook.add(tab1, text="Pending Hotels")
    tree1 = ttk.Treeview(tab1, columns=("ID", "Name", "Location"), show="headings")
    for col in ("ID", "Name", "Location"):
        tree1.heading(col, text=col)
        tree1.column(col, width=150)
    tree1.pack(pady=10, padx=10, fill="both", expand=True)

    tk.Button(tab1, text="✅ Approve Selected", bg="#28a745", fg="black",
              command=lambda: approve_hotel(tree1.item(tree1.selection()[0])["values"][0]) if tree1.selection() else None).pack(pady=5)
    tk.Button(tab1, text="❌ Reject Selected", bg="#dc3545", fg="black",
              command=lambda: reject_hotel(tree1.item(tree1.selection()[0])["values"][0]) if tree1.selection() else None).pack(pady=5)

    # ---------- Tab 2: All Bookings ----------
    tab2 = tk.Frame(notebook, bg="#ffffff")
    notebook.add(tab2, text="All Bookings")
    tree2 = ttk.Treeview(tab2, columns=("ID", "User", "Hotel", "Room", "In", "Out", "Status"), show="headings")
    for col in ("ID", "User", "Hotel", "Room", "In", "Out", "Status"):
        tree2.heading(col, text=col)
        tree2.column(col, width=120)
    tree2.pack(pady=10, padx=10, fill="both", expand=True)

    # ---------- Tab 3: Search by Email ----------
    tab3 = tk.Frame(notebook, bg="#ffffff")
    notebook.add(tab3, text="Search User Bookings")
    tk.Label(tab3, text="Enter User Email:", font=("Arial", 11), bg="white").pack(pady=10)
    email_entry = tk.Entry(tab3, width=40)
    email_entry.pack(pady=5)
    tree3 = ttk.Treeview(tab3, columns=("ID", "User", "Hotel", "Room", "In", "Out", "Status"), show="headings")
    for col in ("ID", "User", "Hotel", "Room", "In", "Out", "Status"):
        tree3.heading(col, text=col)
        tree3.column(col, width=110)
    tree3.pack(pady=10, padx=10, fill="both", expand=True)
    tk.Button(tab3, text="🔍 Search Bookings", bg="#007bff", fg="black", command=lambda: search_user_bookings()).pack(pady=5)

    # ---------- Tab 4: Manage All Hotels ----------
    tab4 = tk.Frame(notebook, bg="#ffffff")
    notebook.add(tab4, text="Manage Hotels")
    tree4 = ttk.Treeview(tab4, columns=("ID", "Name", "Location", "Approved"), show="headings")
    for col in ("ID", "Name", "Location", "Approved"):
        tree4.heading(col, text=col)
        tree4.column(col, width=150)
    tree4.pack(pady=10, padx=10, fill="both", expand=True)

    def on_edit_hotel():
        if not tree4.selection():
            return
        hotel = tree4.item(tree4.selection()[0])["values"]
        edit_win = tk.Toplevel()
        edit_win.title("Edit Hotel")
        edit_win.geometry("300x200")
        tk.Label(edit_win, text="Name").pack(pady=5)
        name_entry = tk.Entry(edit_win)
        name_entry.insert(0, hotel[1])
        name_entry.pack(pady=5)
        tk.Label(edit_win, text="Location").pack(pady=5)
        loc_entry = tk.Entry(edit_win)
        loc_entry.insert(0, hotel[2])
        loc_entry.pack(pady=5)
        tk.Button(edit_win, text="Save", command=lambda: [update_hotel(hotel[0], name_entry.get(), loc_entry.get()), edit_win.destroy(), refresh_all_hotels()]).pack(pady=10)

    tk.Button(tab4, text="✏️ Edit Selected", bg="#ffc107", command=on_edit_hotel).pack(pady=5)
    tk.Button(tab4, text="🗑 Delete Selected", bg="#dc3545", fg="black",
              command=lambda: reject_hotel(tree4.item(tree4.selection()[0])["values"][0]) if tree4.selection() else None).pack(pady=5)

    # ---------- Refresh Functions ----------
    def refresh_pending():
        for i in tree1.get_children():
            tree1.delete(i)
        for h in get_pending_hotels():
            tree1.insert("", "end", values=h)

    def refresh_bookings():
        for i in tree2.get_children():
            tree2.delete(i)
        for row in get_all_bookings():
            tree2.insert("", "end", values=row)

    def refresh_all_hotels():
        for i in tree4.get_children():
            tree4.delete(i)
        for h in get_all_hotels():
            approved = "Yes" if h[3] == 1 else "No"
            tree4.insert("", "end", values=(h[0], h[1], h[2], approved))

    def search_user_bookings():
        email = email_entry.get()
        rows = get_user_bookings_by_email(email)
        for i in tree3.get_children():
            tree3.delete(i)
        for row in rows:
            tree3.insert("", "end", values=row)

    refresh_pending()
    refresh_bookings()
    refresh_all_hotels()

    root.mainloop()

