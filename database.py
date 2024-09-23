import sqlite3

def initialize_database():
    conn = sqlite3.connect('healthcare_chatbot.db')  # Updated database name
    c = conn.cursor()

    # Existing tables
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT UNIQUE,
                    phone TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS symptoms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    description TEXT,
                    assessment TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    doctor TEXT,
                    datetime TEXT,
                    status TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS medications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    name TEXT,
                    dosage TEXT,
                    reminder_time TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id))''')

    # New tables for translations and voice interactions
    c.execute('''CREATE TABLE IF NOT EXISTS translations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    text TEXT,
                    language TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS voice_interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    voice_text TEXT,
                    transcription TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id))''')

    conn.commit()
    conn.close()
