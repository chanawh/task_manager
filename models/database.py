import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_FILE = "tasks.db"

# Create a database connection
def create_connection():
    conn = sqlite3.connect(DB_FILE)
    return conn

# Create the tasks table if it doesn't already exist
def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    # Create tasks table
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            priority INTEGER,
            completed INTEGER DEFAULT 0,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Create users table
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Add a new user (for signup)
def add_user(username, password_hash):
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False  # Username already exists
    conn.close()
    return True

# Get user by username
def get_user_by_username(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Add a new task linked to a specific user
def add_task(title, description, due_date, priority, user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(''' 
        INSERT INTO tasks (title, description, due_date, priority, user_id) 
        VALUES (?, ?, ?, ?, ?) 
    ''', (title, description, due_date, priority, user_id))
    conn.commit()
    conn.close()

# Get tasks for a specific user
def get_tasks(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE user_id = ? ORDER BY due_date ASC', (user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Delete a task
def delete_task(task_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

# Update the completion status of a task
def update_task_status(task_id, status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (status, task_id))
    conn.commit()
    conn.close()
