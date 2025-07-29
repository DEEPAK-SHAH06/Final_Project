# db.py
import sqlite3

def create_tables():
    conn = sqlite3.connect("hotel.db")
    cur = conn.cursor()

    # Users
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT CHECK(role IN ('user', 'owner', 'admin'))
        )
    ''')

    # Hotels
    cur.execute('''
        CREATE TABLE IF NOT EXISTS hotels (
            hotel_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            location TEXT,
            owner_id INTEGER,
            is_approved INTEGER DEFAULT 0,
            FOREIGN KEY(owner_id) REFERENCES users(user_id)
        )
    ''')

    # Rooms
    cur.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            room_id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_id INTEGER,
            type TEXT,
            price REAL,
            is_available INTEGER DEFAULT 1,
            FOREIGN KEY(hotel_id) REFERENCES hotels(hotel_id)
        )
    ''')

    # Bookings
    cur.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            room_id INTEGER,
            check_in TEXT,
            check_out TEXT,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(room_id) REFERENCES rooms(room_id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
