import sqlite3

class DatabaseManager:
    def __init__(self, db_path='astana_bot.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Table for user feedback
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                place_name TEXT,
                feedback TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_review(self, place_name, feedback):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO reviews (place_name, feedback) VALUES (?, ?)",
                       (place_name, feedback))
        self.conn.commit()

    def get_reviews_by_place(self, place_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT feedback FROM reviews WHERE place_name = ?", (place_name,))
        return [row[0] for row in cursor.fetchall()]