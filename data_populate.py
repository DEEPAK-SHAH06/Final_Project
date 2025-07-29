import sqlite3

conn = sqlite3.connect('hotel.db')
cur = conn.cursor()

# Insert users
cur.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)", ('Admin', 'admin@example.com', 'admin123', 'admin'))
cur.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)", ('Owner One', 'owner1@example.com', 'owner123', 'owner'))
cur.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)", ('User One', 'user1@example.com', 'user123', 'user'))

# Insert hotels (assuming owner_id 2 is owner)
cur.execute("INSERT INTO hotels (name, location, owner_id, is_approved) VALUES (?, ?, ?, ?)", ('Mountain View', 'Pokhara', 2, 1))
cur.execute("INSERT INTO hotels (name, location, owner_id, is_approved) VALUES (?, ?, ?, ?)", ('Lakeside Hotel', 'Pokhara', 2, 1))

# Insert rooms for hotel_id 1 and 2
cur.execute("INSERT INTO rooms (hotel_id, type, price, is_available) VALUES (?, ?, ?, ?)", (1, 'Standard', 50, 1))
cur.execute("INSERT INTO rooms (hotel_id, type, price, is_available) VALUES (?, ?, ?, ?)", (1, 'Deluxe', 100, 1))
cur.execute("INSERT INTO rooms (hotel_id, type, price, is_available) VALUES (?, ?, ?, ?)", (2, 'Suite', 150, 1))

conn.commit()
conn.close()

print("Sample data inserted successfully!")
