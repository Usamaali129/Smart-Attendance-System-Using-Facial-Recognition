import sqlite3
import os

# Connect to the SQLite database
def connect_database():
    db_path = os.path.join(os.getcwd(), 'db', 'attendance.db')
    conn = sqlite3.connect(db_path)
    return conn

# Create the attendance table if it doesn't exist
def create_table(conn):
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance_log (
            id INTEGER PRIMARY KEY,
            name TEXT,
            date TEXT,
            time TEXT,
            attendance TEXT
        )
    ''')

    conn.commit()

# Insert a new attendance record into the table
def insert_record(conn, name, date, time, attendance):
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO attendance_log (name, date, time, attendance)
        VALUES (?, ?, ?, ?)
    ''', (name, date, time, attendance))

    conn.commit()

# Delete a record from the table based on a specific field value
def delete_record(conn, record_id):
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM attendance_log
        WHERE id = ?
    ''', (record_id,))

    rows_affected = cursor.rowcount
    print(f"Rows affected: {rows_affected}")

    conn.commit()

# Close the database connection
def close_connection(conn):
    conn.close()

if __name__ == "__main__":
    conn = connect_database()
    create_table(conn)

    # Example usage: Insert a record
    insert_record(conn, "John Doe", "2023-07-15", "09:00:00", "Present")

    # Example usage: Delete a record based on the record ID
    delete_record(conn, 10)

    close_connection(conn)