import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta

FILE_NAME = "todo_app/tasks.json"
DAYS = ["Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun"]

# --- Data Model ---
def get_week_range(date=None):
    if date is None:
        date = datetime.today()
    start = date - timedelta(days=date.weekday())
    end = start + timedelta(days=6)
    return start, end

def week_range_str(start, end):
    return f"{start.strftime('%B %d')} - {end.strftime('%B %d')}"

def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return {}

def save_tasks(tasks):
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=4)

# --- Main App ---
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weekly To-Do List")
        self.root.configure(bg="#181818")
        self.tasks = load_tasks()
        self.today = datetime.today()
        self.week_start, self.week_end = get_week_range(self.today)
        self.week_key = self.week_start.strftime('%Y-%m-%d')
        if self.week_key not in self.tasks:
            self.tasks[self.week_key] = {day: [] for day in DAYS}
        self.setup_ui()
        self.load_task_list()

    def setup_ui(self):
        # --- Styles ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#181818", foreground="#f0f0f0", font=("Arial", 12))
        style.configure("Day.TLabel", background="#232323", foreground="#f0f0f0", font=("Arial", 14, "bold"))
        style.configure("TButton", background="#232323", foreground="#f0f0f0", font=("Arial", 11))
        style.configure("TCheckbutton", background="#181818", foreground="#f0f0f0", font=("Arial", 12))
        style.map("TButton", background=[('active', '#333333')])

        # --- Week Header ---
        self.header = tk.Label(self.root, text=week_range_str(self.week_start, self.week_end),
                              bg="#181818", fg="#f0f0f0", font=("Arial", 24, "bold"), anchor="w")
        self.header.pack(fill="x", padx=30, pady=(20, 0))

        self.divider = tk.Frame(self.root, bg="#333333", height=2)
        self.divider.pack(fill="x", padx=30, pady=(8, 16))

        # --- Add Task ---
        add_frame = tk.Frame(self.root, bg="#181818")
        add_frame.pack(fill="x", padx=30, pady=(0, 16))
        tk.Label(add_frame, text="Task:", bg="#181818", fg="#f0f0f0").pack(side="left")
        self.task_entry = tk.Entry(add_frame, width=30, bg="#232323", fg="#f0f0f0", insertbackground="#f0f0f0",
                                   highlightbackground="#232323", highlightcolor="#444444", relief="flat")
        self.task_entry.pack(side="left", padx=(8, 16))
        tk.Label(add_frame, text="Day:", bg="#181818", fg="#f0f0f0").pack(side="left")
        self.day_var = tk.StringVar(value=DAYS[0])
        self.day_box = ttk.Combobox(add_frame, values=DAYS, state="readonly", width=7, textvariable=self.day_var)
        self.day_box.pack(side="left", padx=(8, 16))
        self.add_button = ttk.Button(add_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side="left")

        # --- Weekly Columns ---
        self.week_frame = tk.Frame(self.root, bg="#181818")
        self.week_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        self.day_frames = {}
        for i, day in enumerate(DAYS):
            col = tk.Frame(self.week_frame, bg="#181818")
            col.grid(row=0, column=i, sticky="nsew", padx=6)
            self.week_frame.columnconfigure(i, weight=1)
            # Day label
            day_label = ttk.Label(col, text=day, style="Day.TLabel", anchor="center")
            day_label.pack(fill="x", pady=(0, 8))
            # Task list frame
            task_list = tk.Frame(col, bg="#181818")
            task_list.pack(fill="both", expand=True)
            self.day_frames[day] = task_list

    def add_task(self):
        title = self.task_entry.get().strip()
        day = self.day_var.get()
        if not title:
            messagebox.showwarning("Error", "Task title cannot be empty.")
            return
        task = {"title": title, "done": False}
        self.tasks[self.week_key][day].append(task)
        save_tasks(self.tasks)
        self.task_entry.delete(0, tk.END)
        self.load_task_list()

    def load_task_list(self):
        for day in DAYS:
            frame = self.day_frames[day]
            for widget in frame.winfo_children():
                widget.destroy()
            for idx, task in enumerate(self.tasks[self.week_key][day]):
                self.add_task_widget(frame, day, idx, task)

    def add_task_widget(self, parent, day, idx, task):
        var = tk.BooleanVar(value=task["done"])
        def on_toggle():
            self.tasks[self.week_key][day][idx]["done"] = var.get()
            save_tasks(self.tasks)
            self.load_task_list()
        cb = tk.Checkbutton(parent, variable=var, command=on_toggle,
                            bg="#181818", activebackground="#181818",
                            highlightthickness=0, bd=0)
        cb.grid(row=idx, column=0, sticky="w")
        # Strikethrough if done
        font = ("Arial", 12, "overstrike" if task["done"] else "normal")
        fg = "#888888" if task["done"] else "#f0f0f0"
        label = tk.Label(parent, text=task["title"], font=font, fg=fg, bg="#181818", anchor="w")
        label.grid(row=idx, column=1, sticky="w", padx=(0, 2))
        del_btn = tk.Button(parent, text="✕", command=lambda: self.delete_task(day, idx),
                            bg="#181818", fg="#888888", bd=0, highlightthickness=0,
                            activebackground="#232323", activeforeground="#ff5555", font=("Arial", 10, "bold"))
        del_btn.grid(row=idx, column=2, sticky="e", padx=(2, 0))

    def delete_task(self, day, idx):
        del self.tasks[self.week_key][day][idx]
        save_tasks(self.tasks)
        self.load_task_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop() 