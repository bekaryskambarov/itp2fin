import sqlite3

def init_db():
    conn = sqlite3.connect('astana_bot.db')
    cursor = conn.cursor()
    # Create table for favorites
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            user_id INTEGER,
            place_name TEXT,
            UNIQUE(user_id, place_name)
        )
    ''')
    conn.commit()
    conn.close()

def add_favorite(user_id, place_name):
    conn = sqlite3.connect('astana_bot.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO favorites (user_id, place_name) VALUES (?, ?)", (user_id, place_name))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # Already in favorites
    finally:
        conn.close()

def get_favorites(user_id):
    conn = sqlite3.connect('astana_bot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT place_name FROM favorites WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]