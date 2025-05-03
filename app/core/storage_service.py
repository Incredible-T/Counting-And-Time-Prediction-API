import sqlite3

class StorageService:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number_cars INTEGER NOT NULL,
            time_seconds REAL NOT NULL
        )
        """)
        self.conn.commit()

    def store_sensor_data(self, number_cars, time_seconds):
        self.cursor.execute(
            "INSERT INTO sensor_data (number_cars, time_seconds) VALUES (?, ?)",
            (number_cars, time_seconds)
        )
        self.conn.commit()