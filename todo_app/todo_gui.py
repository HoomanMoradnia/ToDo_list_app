import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
import os

FILE_NAME = "tasks.json"

def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=4)

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.tasks = load_tasks()
        self.setup_ui()
        self.load_task_list()

    def setup_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        # Input Fields
        tk.Label(frame, text="Task").grid(row=0, column=0)
        self.task_entry = tk.Entry(frame, width=30)
        self.task_entry.grid(row=0, column=1, columnspan=2)

        tk.Label(frame, text="Deadline").grid(row=1, column=0)
        self.deadline_entry = DateEntry(frame, width=12, background='darkblue',
                                        foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.deadline_entry.grid(row=1, column=1)

        tk.Label(frame, text="Priority").grid(row=1, column=2)
        self.priority_box = ttk.Combobox(frame, values=["low", "medium", "high"], state="readonly")
        self.priority_box.grid(row=1, column=3)
        self.priority_box.set("medium")

        self.add_button = tk.Button(frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=2, column=0, columnspan=4, pady=5)

        # Task List
        self.task_list_frame = tk.Frame(self.root)
        self.task_list_frame.pack()

    def add_task(self):
        title = self.task_entry.get().strip()
        deadline = self.deadline_entry.get()
        priority = self.priority_box.get()

        if not title:
            messagebox.showwarning("Error", "Task title cannot be empty.")
            return

        self.tasks.append({"title": title, "deadline": deadline, "priority": priority, "done": False})
        save_tasks(self.tasks)
        self.task_entry.delete(0, tk.END)
        self.load_task_list()

    def load_task_list(self):
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()

        for index, task in enumerate(self.tasks):
            var = tk.BooleanVar(value=task["done"])
            cb = tk.Checkbutton(self.task_list_frame, text=f"{task['title']} | {task['deadline']} | {task['priority']}",
                                variable=var, command=lambda i=index, v=var: self.mark_complete(i, v))
            cb.grid(row=index, column=0, sticky="w")

            del_btn = tk.Button(self.task_list_frame, text="Delete", command=lambda i=index: self.delete_task(i))
            del_btn.grid(row=index, column=1)

    def mark_complete(self, index, var):
        self.tasks[index]["done"] = var.get()
        save_tasks(self.tasks)

    def delete_task(self, index):
        del self.tasks[index]
        save_tasks(self.tasks)
        self.load_task_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop() 