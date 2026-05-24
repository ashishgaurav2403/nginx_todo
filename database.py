import sqlite3
import os

# Save the database in a dedicated folder so Docker can persist it
DB_DIR = 'data'
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

DB_NAME = os.path.join(DB_DIR, 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()

def get_all_todos():
    with get_db_connection() as conn:
        todos = conn.execute('SELECT * FROM todos').fetchall()
        return [dict(todo) for todo in todos]

def create_todo(task):
    with get_db_connection() as conn:
        cursor = conn.execute('INSERT INTO todos (task) VALUES (?)', (task,))
        conn.commit()
        return cursor.lastrowid

def toggle_todo_status(todo_id):
    with get_db_connection() as conn:
        todo = conn.execute('SELECT completed FROM todos WHERE id = ?', (todo_id,)).fetchone()
        new_status = not todo['completed']
        conn.execute('UPDATE todos SET completed = ? WHERE id = ?', (new_status, todo_id))
        conn.commit()
        return new_status

def delete_todo_by_id(todo_id):
    with get_db_connection() as conn:
        conn.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
        conn.commit()