# main.py
from models.database import create_table
from views.gui import TaskManagerApp
import tkinter as tk
from controllers.task_manager import TaskController

if __name__ == "__main__":
    create_table()  # Ensure the database table is created
    root = tk.Tk()
    controller = TaskController()  # Initialize the controller
    app = TaskManagerApp(root, controller)  # Initialize the view
    root.mainloop()
