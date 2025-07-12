import json
import os

FILE_NAME = "tasks.json"

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

def show_tasks(tasks):
    if not tasks:
        print("No tasks found.")
    else:
        for i, task in enumerate(tasks, 1):
            status = "✓" if task["done"] else "✗"
            print(f"{i}. [{status}] {task['title']}")

def add_task(tasks):
    title = input("Enter task title: ")
    tasks.append({
        "title": title,
        "done": False
    })
    print("Task added!")

def complete_task(tasks):
    show_tasks(tasks)
    try:
        i = int(input("Enter task number to complete: ")) - 1
        if 0 <= i < len(tasks):
            tasks[i]["done"] = True
            print("Task marked as completed!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a number.")

def delete_task(tasks):
    show_tasks(tasks)
    try:
        i = int(input("Enter task number to delete: ")) - 1
        if 0 <= i < len(tasks):
            tasks.pop(i)
            print("Task deleted!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a number.")

def menu():
    tasks = load_tasks()
    while True:
        print("\n--- To Do List ---")
        print("1. Show tasks")
        print("2. Add task")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            save_tasks(tasks)
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    menu()