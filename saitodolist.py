import json
import os

FILE_NAME = "tasks.json"
CATEGORIES = ["work", "study", "personal"]
PRIORITIES = ["high", "medium", "low"]
PRIORITY_ORDER = {"high": 1, "medium": 2, "low": 3}

def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return json.load(file)
        
def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)
        
def get_priority_rank(task):
    return PRIORITY_ORDER[task["priority"]]

def sort_tasks(tasks):
    tasks.sort(key=get_priority_rank)

def ask_choice(question, options, default=None):
    while True:
        answer = input(f"{question} ({'/'.join(options)}): ").strip().lower()
        if answer == "" and default is not None:
            return default
        if answer in options:
            return answer
        print("Invalid choice, try again.")

def ask_task_number(tasks):
    if len(tasks) == 0:
        print("No tasks yet.")
        return None
    try:
        number = int(input("Enter task number: "))
    except ValueError:
        print("Please enter a number.")
        return None
    if number < 1 or number > len(tasks):
        print("That task number does not exist.")
        return None
    return number - 1

def print_task(number, task):
    status = "Completed" if task["done"] else "Incomplete"
    print(f"{number}. [{status}] {task['title']} ({task['category']}, {task['priority']})")
    if task["description"]:
        print(f" Description: {task['description']}")

def add_task(tasks):
    title = input("Title: ").strip()
    if title == "":
        print("Title cannot be empty.")
        return
    description = input("Description (optional, press Enter to skip): ").strip()
    category = ask_choice("Category", CATEGORIES)
    priority = ask_choice("Priority", PRIORITIES)

    task = {
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "done": False,
    }
    tasks.append(task)
    sort_tasks(tasks)
    save_tasks(tasks)
    print("Task added.")

def view_tasks(tasks):
    if len(tasks) == 0:
        print("No tasks yet.")
        return
    print("\n--- All Tasks ---")
    for i, task in enumerate(tasks, start=1):
        print_task(i, task)

def filter_tasks(tasks):
    category = ask_choice("Show which category", CATEGORIES)
    print(f"\n--- {category.title()} Tasks ---")
    found = False
    for i, task in enumerate(tasks, start=1):
        if task["category"] == category:
            print_task(i, task)
            found = True
    if not found:
        print("No tasks in this category.")

def complete_task(tasks):
    index = ask_task_number(tasks)
    if index is None:
        return
    tasks[index]["done"] = True
    save_tasks(tasks)
    print("Task marked as completed.")

def edit_task(tasks):
    index = ask_task_number(tasks)
    if index is None:
        return
    task = tasks[index]
    print("Press Enter to keep the current value.")

    new_title = input(f"Title [{task['title']}]: ").strip()
    if new_title != "":
        task["title"] = new_title

    new_description = input(f"Description [{task['description']}]: ").strip()
    if new_description != "":
        task["description"] = new_description

    task["category"] = ask_choice(f"Category [{task['category']}]", CATEGORIES, task["category"])
    task["priority"] = ask_choice(f"Priority [{task['priority']}]", PRIORITIES, task["priority"])

    sort_tasks(tasks)
    save_tasks(tasks)
    print("Task updated.")

def delete_task(tasks):
    index = ask_task_number(tasks)
    if index is None:
        return
    removed = tasks.pop(index)
    save_tasks(tasks)
    print(f"Deleted: {removed['title']}")

def show_summary(tasks):
    completed = 0
    for task in tasks:
        if task["done"]:
            completed += 1
    pending = len(tasks) - completed
    print("\n--- Summary ---")
    print(f"Total:     {len(tasks)}")
    print(f"Pending:   {pending}")
    print(f"Completed: {completed}")

def show_menu():
    print("\n===== TODO LIST =====")
    print("1. Add task")
    print("2. View all tasks")
    print("3. Filter by category")
    print("4. Mark task as done")
    print("5. Edit task")
    print("6. Delete task")
    print("7. Summary")
    print("8. Exit")

def main():
    tasks = load_tasks()
    sort_tasks(tasks)

    while True:
        show_menu()
        choice = input("Choose an option (1-8): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            filter_tasks(tasks)
        elif choice == "4":
            complete_task(tasks)
        elif choice == "5":
            edit_task(tasks)
        elif choice == "6":
            delete_task(tasks)
        elif choice == "7":
            show_summary(tasks)
        elif choice == "8":
            print("Thank You ! See You Soon...")
            break
        else:
            print("Invalid option, choose 1-8.")
main()
