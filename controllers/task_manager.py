# controllers/task_manager.py
from models.database import get_tasks, add_task, delete_task, update_task_status

class TaskController:
    def __init__(self):
        pass

    # Add a task to the database
    def add_task(self, title, description, due_date, priority):
        if title and due_date and priority.isdigit():
            add_task(title, description, due_date, int(priority))
            return True
        return False

    # Retrieve all tasks
    def get_tasks(self):
        return get_tasks()

    # Delete a task
    def delete_task(self, task_id):
        delete_task(task_id)

    # Mark a task as complete
    def mark_complete(self, task_id):
        update_task_status(task_id, 1)

    # Filter tasks by different criteria
    def filter_tasks(self, filter_type):
        tasks = self.get_tasks()
        if filter_type == 'completed':
            return [task for task in tasks if task[5] == 1]
        elif filter_type == 'pending':
            return [task for task in tasks if task[5] == 0]
        elif filter_type == 'high_priority':
            return sorted(tasks, key=lambda x: x[4])
        return tasks
