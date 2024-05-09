import sqlite3


# Путь к файлу базы данных SQLite
DB_FILE = 'bot_database.db'

# Функция для создания таблицы пользователей, если она не существует
def create_users_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        chat_id INTEGER UNIQUE,
                        username TEXT,
                        onboarding_stage INTEGER DEFAULT 0
                    )''')
    conn.commit()
    conn.close()

# Функция для добавления пользователя в базу данных
def add_user(chat_id, username, first_name, last_name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (chat_id, username) VALUES (?, ?)", (chat_id, username))
    conn.commit()
    conn.close()

# Функция для обновления этапа онбординга пользователя
def update_onboarding_stage(chat_id, stage):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET onboarding_stage = ? WHERE chat_id = ?", (stage, chat_id))
    conn.commit()
    conn.close()
