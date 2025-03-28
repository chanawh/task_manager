# views/gui.py
import tkinter as tk
from tkinter import messagebox
from controllers.task_manager import TaskController

class TaskManagerApp:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Task Manager")
        self.root.geometry("500x400")

        self.create_widgets()
        self.load_tasks()

    def create_widgets(self):
        # Title
        self.title_label = tk.Label(self.root, text="Task Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()

        # Description
        self.desc_label = tk.Label(self.root, text="Description:")
        self.desc_label.pack()
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.pack()

        # Due Date
        self.date_label = tk.Label(self.root, text="Due Date (YYYY-MM-DD):")
        self.date_label.pack()
        self.date_entry = tk.Entry(self.root)
        self.date_entry.pack()

        # Priority
        self.priority_label = tk.Label(self.root, text="Priority (1-5):")
        self.priority_label.pack()
        self.priority_entry = tk.Entry(self.root)
        self.priority_entry.pack()

        # Add Task Button
        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.pack()

        # Task List
        self.task_list = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.task_list.pack(fill=tk.BOTH, expand=True)

        # Mark Complete Button
        self.complete_button = tk.Button(self.root, text="Mark Complete", command=self.mark_complete)
        self.complete_button.pack()

        # Delete Task Button
        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack()

    def add_task(self):
        title = self.title_entry.get()
        description = self.desc_entry.get()
        due_date = self.date_entry.get()
        priority = self.priority_entry.get()

        if title and due_date and priority.isdigit():
            self.controller.add_task(title, description, due_date, int(priority))
            self.load_tasks()
            messagebox.showinfo("Success", "Task added!")
        else:
            messagebox.showerror("Error", "Please fill in all fields correctly.")

    def load_tasks(self):
        self.task_list.delete(0, tk.END)
        tasks = self.controller.get_tasks()
        for task in tasks:
            status = "✅" if task[5] else "❌"
            self.task_list.insert(tk.END, f"{task[1]} | {task[3]} | Priority: {task[4]} | {status}")

    def delete_task(self):
        selected = self.task_list.curselection()
        if selected:
            task_id = self.controller.get_tasks()[selected[0]][0]
            self.controller.delete_task(task_id)
            self.load_tasks()

    def mark_complete(self):
        selected = self.task_list.curselection()
        if selected:
            task_id = self.controller.get_tasks()[selected[0]][0]
            self.controller.mark_complete(task_id)
            self.load_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    controller = TaskController()
    app = TaskManagerApp(root, controller)
    root.mainloop()
