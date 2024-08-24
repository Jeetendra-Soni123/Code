import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime

class Task:
    def __init__(self, description, deadline=None, priority=None):
        self.description = description
        self.deadline = deadline
        self.priority = priority

    def __str__(self):
        return f"[{self.priority}] {self.description} (Due: {self.deadline})"

class ToDoApp:
    def __init__(self, newWindow):
        self.newWindow = newWindow
        self.newWindow.title("To-Do List Application")

        self.tasks = []

        # Create the GUI components
        self.task_listbox = tk.Listbox(newWindow, height=15, width=50)
        self.task_listbox.pack(pady=10)

        self.add_button = tk.Button(newWindow, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.edit_button = tk.Button(newWindow, text="Edit Task", command=self.edit_task)
        self.edit_button.pack(pady=5)

        self.delete_button = tk.Button(newWindow, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)

    def add_task(self):
        description = simpledialog.askstring("Task", "Enter task description:")
        deadline = simpledialog.askstring("Deadline", "Enter deadline (YYYY-MM-DD):")
        priority = simpledialog.askstring("Priority", "Enter priority level (High, Medium, Low):")

        if description and deadline and priority:
            task = Task(description, deadline, priority)
            self.tasks.append(task)
            self.update_task_listbox()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    def edit_task(self):
        selected_task_index = self.task_listbox.curselection()

        if selected_task_index:
            task_id = selected_task_index[0]

            description = simpledialog.askstring("Task", "Enter new description:", initialvalue=self.tasks[task_id].description)
            deadline = simpledialog.askstring("Deadline", "Enter new deadline (YYYY-MM-DD):", initialvalue=self.tasks[task_id].deadline)
            priority = simpledialog.askstring("Priority", "Enter new priority level (High, Medium, Low):", initialvalue=self.tasks[task_id].priority)

            if description and deadline and priority:
                self.tasks[task_id].description = description
                self.tasks[task_id].deadline = deadline
                self.tasks[task_id].priority = priority
                self.update_task_listbox()
            else:
                messagebox.showwarning("Input Error", "Please fill all fields.")
        else:
            messagebox.showwarning("Selection Error", "Please select a task to edit.")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()

        if selected_task_index:
            task_id = selected_task_index[0]
            del self.tasks[task_id]
            self.update_task_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.tasks):
            self.task_listbox.insert(tk.END, f"{i+1}. {task}")

if __name__ == "__main__":
    newWindow = tk.Tk()
    app = ToDoApp(newWindow)
    newWindow.mainloop()