import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

FILE_NAME = "todo_app/tasks.json"

# --- Data Model ---
def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            data = json.load(f)
            # Handle migration from old weekly format to new simple format
            if isinstance(data, dict):
                # Old format: {"week_key": {"day": [tasks]}}
                # Convert to new format: [tasks]
                all_tasks = []
                for week_data in data.values():
                    if isinstance(week_data, dict):
                        for day_tasks in week_data.values():
                            if isinstance(day_tasks, list):
                                all_tasks.extend(day_tasks)
                return all_tasks
            elif isinstance(data, list):
                # Already in new format
                return data
            else:
                return []
    return []

def save_tasks(tasks):
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=4)

# --- Main App ---
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.configure(bg="#181818")
        self.tasks = load_tasks()
        self.setup_ui()
        self.load_task_list()

    def setup_ui(self):
        # --- Styles ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#181818", foreground="#f0f0f0", font=("Arial", 12))
        style.configure("TButton", background="#232323", foreground="#f0f0f0", font=("Arial", 11))
        style.configure("TCheckbutton", background="#181818", foreground="#f0f0f0", font=("Arial", 12))
        style.map("TButton", background=[('active', '#333333')])

        # --- Header ---
        self.header = tk.Label(self.root, text="To-Do List",
                              bg="#181818", fg="#f0f0f0", font=("Arial", 30, "bold"), anchor="w")
        self.header.pack(fill="x", padx=30, pady=(20, 0))

        self.divider = tk.Frame(self.root, bg="#333333", height=2)
        self.divider.pack(fill="x", padx=30, pady=(8, 16))

        # --- Add Task ---
        add_frame = tk.Frame(self.root, bg="#181818")
        add_frame.pack(fill="x", padx=30, pady=(0, 16))
        tk.Label(add_frame, text="Task:", bg="#181818", fg="#f0f0f0").pack(side="left")
        self.task_entry = tk.Entry(add_frame, width=40, bg="#232323", fg="#f0f0f0", insertbackground="#f0f0f0",
                                   highlightbackground="#232323", highlightcolor="#444444", relief="flat")
        self.task_entry.pack(side="left", padx=(8, 16))
        self.add_button = ttk.Button(add_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side="left")

        # --- Task List ---
        self.task_frame = tk.Frame(self.root, bg="#181818")
        self.task_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))

    def add_task(self):
        title = self.task_entry.get().strip()
        if not title:
            messagebox.showwarning("Error", "Task title cannot be empty.")
            return
        task = {"title": title, "done": False}
        self.tasks.append(task)
        save_tasks(self.tasks)
        self.task_entry.delete(0, tk.END)
        self.load_task_list()

    def load_task_list(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()
        for idx, task in enumerate(self.tasks):
            self.add_task_widget(self.task_frame, idx, task)

    def add_task_widget(self, parent, idx, task):
        var = tk.BooleanVar(value=task["done"])
        def on_toggle():
            self.tasks[idx]["done"] = var.get()
            save_tasks(self.tasks)
            self.load_task_list()
        cb = tk.Checkbutton(parent, variable=var, command=on_toggle,
                            bg="#181818", activebackground="#181818",
                            highlightthickness=0, bd=0)
        cb.grid(row=idx, column=0, sticky="w")
        # Strikethrough if done
        font = ("Arial", 18, "overstrike" if task["done"] else "normal")
        fg = "#888888" if task["done"] else "#f0f0f0"
        label = tk.Label(parent, text=task["title"], font=font, fg=fg, bg="#181818", anchor="w")
        label.grid(row=idx, column=1, sticky="w", padx=(0, 2))
        del_btn = tk.Button(parent, text="✕", command=lambda: self.delete_task(idx),
                            bg="#181818", fg="#888888", bd=0, highlightthickness=0,
                            activebackground="#232323", activeforeground="#ff5555", font=("Arial", 15, "bold"))
        del_btn.grid(row=idx, column=2, sticky="e", padx=(2, 0))

    def delete_task(self, idx):
        del self.tasks[idx]
        save_tasks(self.tasks)
        self.load_task_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop() 