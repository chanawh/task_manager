import tkinter as tk
from tkinter import messagebox
from controllers.task_controller import TaskController
from controllers.user_controller import UserController

class TaskManagerApp:
    def __init__(self, root, user_controller, task_controller):
        self.root = root
        self.user_controller = user_controller
        self.task_controller = task_controller
        self.root.title("Task Manager")
        self.root.geometry("500x400")

        self.user_id = None  # Track the logged-in user

        # Show login screen first
        self.show_login_screen()

    ### ------------------------ AUTH SCREENS ------------------------
    def show_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Username:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack()
        tk.Button(self.root, text="Signup", command=self.show_signup_screen).pack()

    def show_signup_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Username:").pack()
        self.signup_username_entry = tk.Entry(self.root)
        self.signup_username_entry.pack()

        tk.Label(self.root, text="Password:").pack()
        self.signup_password_entry = tk.Entry(self.root, show="*")
        self.signup_password_entry.pack()

        tk.Button(self.root, text="Register", command=self.signup).pack()
        tk.Button(self.root, text="Back to Login", command=self.show_login_screen).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.user_controller.login_user(username, password)  # Corrected method name
        if user:
            self.user_id = user[0]  # Assuming the user ID is at index 0
            messagebox.showinfo("Login Successful", f"Welcome {username}!")
            self.show_main_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def signup(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()

        if self.user_controller.register_user(username, password):  # Use register_user
            messagebox.showinfo("Signup Successful", "You can now log in!")
            self.show_login_screen()
        else:
            messagebox.showerror("Signup Failed", "Username already exists.")

    ### ------------------------ MAIN SCREEN ------------------------
    def show_main_screen(self):
        self.clear_screen()
        self.create_widgets()
        self.load_tasks()

    def create_widgets(self):
        # Title
        tk.Label(self.root, text="Task Title:").pack()
        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()

        # Description
        tk.Label(self.root, text="Description:").pack()
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.pack()

        # Due Date
        tk.Label(self.root, text="Due Date (YYYY-MM-DD):").pack()
        self.date_entry = tk.Entry(self.root)
        self.date_entry.pack()

        # Priority
        tk.Label(self.root, text="Priority (1-5):").pack()
        self.priority_entry = tk.Entry(self.root)
        self.priority_entry.pack()

        # Add Task Button
        tk.Button(self.root, text="Add Task", command=self.add_task).pack()

        # Task List
        self.task_list = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.task_list.pack(fill=tk.BOTH, expand=True)

        # Mark Complete Button
        tk.Button(self.root, text="Mark Complete", command=self.mark_complete).pack()

        # Delete Task Button
        tk.Button(self.root, text="Delete Task", command=self.delete_task).pack()

        # Logout Button
        tk.Button(self.root, text="Logout", command=self.logout).pack()

    def add_task(self):
        title = self.title_entry.get()
        description = self.desc_entry.get()
        due_date = self.date_entry.get()
        priority = self.priority_entry.get()

        if title and due_date and priority.isdigit():
            self.task_controller.add_task(title, description, due_date, int(priority), self.user_id)
            self.load_tasks()
            messagebox.showinfo("Success", "Task added!")
        else:
            messagebox.showerror("Error", "Please fill in all fields correctly.")

    def load_tasks(self):
        self.task_list.delete(0, tk.END)
        tasks = self.task_controller.get_tasks(self.user_id)
        for task in tasks:
            status = "✅" if task[5] else "❌"
            self.task_list.insert(tk.END, f"{task[1]} | {task[3]} | Priority: {task[4]} | {status}")

    def delete_task(self):
        selected = self.task_list.curselection()
        if selected:
            task_id = self.task_controller.get_tasks(self.user_id)[selected[0]][0]
            self.task_controller.delete_task(task_id)
            self.load_tasks()

    def mark_complete(self):
        selected = self.task_list.curselection()
        if selected:
            task_id = self.task_controller.get_tasks(self.user_id)[selected[0]][0]
            self.task_controller.mark_complete(task_id)
            self.load_tasks()

    def logout(self):
        self.user_id = None
        self.show_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    user_controller = UserController()  # Correct instantiation of UserController
    task_controller = TaskController()  # Correct instantiation of TaskController
    app = TaskManagerApp(root, user_controller, task_controller)  # Initialize the view
    root.mainloop()
