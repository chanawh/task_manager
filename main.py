from models.database import create_table
from views.gui import TaskManagerApp
import tkinter as tk
from controllers.user_controller import UserController
from controllers.task_controller import TaskController

if __name__ == "__main__":
    create_table()  # Ensure the database table is created
    root = tk.Tk()
    user_controller = UserController()  # Initialize the user controller
    task_controller = TaskController()  # Initialize the task controller
    app = TaskManagerApp(root, user_controller, task_controller)  # Pass both controllers
    root.mainloop()
