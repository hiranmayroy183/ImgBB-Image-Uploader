import sqlite3

def create_db():
    conn = sqlite3.connect('images.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, token_count INTEGER DEFAULT 0, image_count INTEGER DEFAULT 0, is_premium INTEGER DEFAULT 0, token TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS images
                 (id INTEGER PRIMARY KEY, url TEXT, delete_url TEXT, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
