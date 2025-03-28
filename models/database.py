# models/database.py
import sqlite3

DB_FILE = "tasks.db"

# Create a database connection
def create_connection():
    conn = sqlite3.connect(DB_FILE)
    return conn

# Create the tasks table if it doesn't already exist
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            priority INTEGER,
            completed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Add a new task to the database
def add_task(title, description, due_date, priority):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, description, due_date, priority)
        VALUES (?, ?, ?, ?)
    ''', (title, description, due_date, priority))
    conn.commit()
    conn.close()

# Retrieve all tasks from the database
def get_tasks():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY due_date ASC')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Delete a task from the database
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
