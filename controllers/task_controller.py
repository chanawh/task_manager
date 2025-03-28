import bcrypt
from models.database import (
    get_tasks,
    add_task,
    delete_task,
    update_task_status,
    add_user,  # Correct function name.
    get_user_by_username
)

class TaskController:
    def __init__(self):
        pass

    ### ------------------------ AUTHENTICATION ------------------------
    def add_user(self, username, password):
        # Check if the user already exists
        existing_user = get_user_by_username(username)
        if existing_user:
            return False
        
        # Hash the password before saving
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        add_user(username, hashed_password)
        return True

    def verify_user(self, username, password):
        user = get_user_by_username(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            return user  # Return user object if authentication is successful
        return None

    ### ------------------------ TASK HANDLING ------------------------
    def add_task(self, title, description, due_date, priority, user_id):
    # Check that the title, due date are not empty, and priority is a valid number
        if title and due_date and isinstance(priority, int):
            add_task(title, description, due_date, priority, user_id)
            return True
        return False

    def get_tasks(self, user_id):
        return get_tasks(user_id)

    def delete_task(self, task_id):
        delete_task(task_id)

    def mark_complete(self, task_id):
        update_task_status(task_id, 1)

    ### ------------------------ TASK FILTERING ------------------------
    def filter_tasks(self, filter_type, user_id):
        tasks = self.get_tasks(user_id)
        if filter_type == 'completed':
            return [task for task in tasks if task[5] == 1]
        elif filter_type == 'pending':
            return [task for task in tasks if task[5] == 0]
        elif filter_type == 'high_priority':
            return sorted(tasks, key=lambda x: x[4])
        return tasks
