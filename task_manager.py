
import datetime
import json

all_tasks = []
tasks_done = []
tasks_in_progress = []
tasks_todo = []
task_id_counter = 0


def load_tasks():
    global all_tasks, tasks_done, tasks_in_progress, tasks_todo, task_id_counter

    try:
        with open('task_store.json', 'r') as file:
            data = json.load(file)  
            all_tasks = data.get('all_tasks', [])
            tasks_done = data.get('tasks_done', [])
            tasks_in_progress = data.get('tasks_in_progress', [])
            tasks_todo = data.get('tasks_todo', [])
            task_id_counter = data.get('task_id_counter', 0)

        for task in all_tasks:
                task['createdAt'] = datetime.datetime.fromisoformat(task['createdAt'])
                task['updatedAt'] = datetime.datetime.fromisoformat(task['updatedAt'])

        print("Tasks loaded successfully.")

    except FileNotFoundError:
        print("No previous task data found. Starting fresh.")
    except json.JSONDecodeError:
        print("Error decoding JSON. Starting fresh.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}. Starting fresh.")


def save_tasks():
    global all_tasks, tasks_done, tasks_in_progress, tasks_todo, task_id_counter
    try:
        for task in all_tasks:
            task['createdAt'] = task['createdAt'].isoformat()
            task['updatedAt'] = task['updatedAt'].isoformat()

        with open('task_store.json', 'w') as file:
            data = {
                'all_tasks': all_tasks,
                'tasks_done': tasks_done,
                'tasks_in_progress': tasks_in_progress,
                'tasks_todo': tasks_todo,
                'task_id_counter': task_id_counter
            }

            json.dump(data, file, indent=4)
            print("Tasks saved successfully.")
    except Exception as e:
        print(f"Error saving tasks to file: {e}")


def show_info(id, description, status, created, updated):
    print("\nTask Information:")
    print(f"Task ID: {id}")
    print(f"Task description: {description}")
    print(f"Task status: {status}")
    print(f"Task created at: {created}")
    print(f"Task updated at: {updated}")


def add_task():
    print("\nAdd a task")
    
    global task_id_counter
    task_id = task_id_counter
    task_id_counter += 1

    description = input("Task description: ")
    status = input("Task status (todo, in-progress, done): ").lower() 

    while status not in ['todo', 'in-progress', 'done']:
        print("\nInvalid status! Please enter 'todo', 'in-progress', or 'done'.")
        status = input("Task status (todo, in-progress, done): ").lower()

    created = datetime.datetime.now()
    updated = datetime.datetime.now()

    task = {
    "id": task_id,
    "description": description,
    "status": status,
    "createdAt": created,
    "updatedAt": updated,
    }
    all_tasks.append(task)

    if status == 'done':
        tasks_done.append(task) 
    elif status == 'in-progress':
        tasks_in_progress.append(task)
    elif status == 'todo':
        tasks_todo.append(task)
    
    save_tasks()
    print("Task added successfully")

    return task_id, description, status, created, updated
    

def update_task():
    print("\nUpdate a task")   

    if all_tasks:
        print("\nHere are the current tasks:")
        for task in all_tasks:
            show_info(task['id'], task['description'], task['status'], task['createdAt'], task['updatedAt'])
    else:
        print("\nNo tasks available to update.")

    try:
        task_id = int(input("\nEnter the Task ID to update: "))
    except ValueError:
        print("\nInvalid input! Task ID must be a number.")
        return

    task = None  
    for t in all_tasks:
        if t['id'] == task_id:  
            task = t  
            break  

    if task:
        print("\nTask found:")
        show_info(task['id'], task['description'], task['status'], task['createdAt'], task['updatedAt'])

        update_choice = input("\nWhat would you like to update? (description/status/both): ").lower()
        
        while update_choice not in ['description', 'status', 'both']:
            print("\nInvalid choice! Please enter 'description', 'status', or 'both'.")
            update_choice = input("\nWhat would you like to update? (description/status/both): ").lower()

        if update_choice == 'description' or update_choice == 'both':
            new_description = input("Enter new description: ")
            task['description'] = new_description

        if update_choice == 'status' or update_choice == 'both':
            new_status = input("Enter new status (todo, in-progress, done): ").lower()

            while new_status not in ['todo', 'in-progress', 'done']:
                print("\nInvalid status! Please enter 'todo', 'in-progress', or 'done'.")
                new_status = input("Enter new status (todo, in-progress, done): ").lower()

            task['status'] = new_status
        
        if new_status == 'done':
            tasks_done.append(task) 
        elif new_status == 'in-progress':
            tasks_in_progress.append(task)
        elif new_status == 'todo':
            tasks_todo.append(task)



        task['updatedAt'] = datetime.datetime.now()  
        save_tasks()
        print("\nTask updated successfully!")
    else:
        print("\nTask with that ID not found.")


def delete_task():
    print("\nDelete a task")       

    if all_tasks:
        print("\nHere are the current tasks:")
        for task in all_tasks:
            show_info(task['id'], task['description'], task['status'], task['createdAt'], task['updatedAt'])
    else:
        print("\nNo tasks available to delete.")
    
    try:
        task_id = int(input("\nEnter the Task ID to delete: "))  
    except ValueError:
        print("\nInvalid input! Task ID must be a number.")
        return
    
    task = None
    for t in all_tasks:
        if t['id'] == task_id:  
            task = t  

    if task:
        print("\nTask found:")
        show_info(task['id'], task['description'], task['status'], task['createdAt'], task['updatedAt'])

        all_tasks.remove(task)  
        tasks_done.remove(task) if task in tasks_done else None
        tasks_in_progress.remove(task) if task in tasks_in_progress else None
        tasks_todo.remove(task) if task in tasks_todo else None

        save_tasks()
        print("\nTask deleted successfully!")
    else:
        print("\nTask with that ID not found.")


def list_all_tasks():
    print("\nList all tasks")   

    if all_tasks:
        print("\nAll tasks:")
        for task in all_tasks:
            show_info(task['id'], task['description'], task['status'], task['createdAt'], task['updatedAt'])
    else:
        print("\nNo tasks found.")


def list_done_tasks():
    print("\nList done tasks")  

    if tasks_done:
        print("\nDone tasks:")
        for task in tasks_done:
            show_info(task['id'], task['description'], task['status'], task['createdAt'], task['updatedAt'])
    else:
        print("\nNo done tasks found.")


def list_in_progress_tasks():
    print("\nList in-progress tasks")

    if tasks_in_progress:
        print("\nIn-progress tasks:")
        for task in tasks_in_progress:
            show_info(task['id'], task['description'], task['status'], task['createdAt'], task['updatedAt'])
    else:
        print("\nNo in-progress tasks found.")


def list_todo_tasks():
    print("\nList todo tasks")

    if tasks_todo:
        print("\nTodo tasks:")
        for task in tasks_todo:
            show_info(task['id'], task['description'], task['status'], task['createdAt'], task['updatedAt'])
    else:
        print("\nNo todo tasks found.")

"""
def reset_task_id_counter():
    print("\nReset Task ID Counter")
    print("Make sure you delete all tasks before resetting the ID counter.")

    confirmation = input("Are you sure you want to reset the task ID counter? (yes/no): ").lower()

    while confirmation not in ['yes', 'no']:
        print("\nInvalid input! Please enter 'yes' or 'no'.")
        confirmation = input("Are you sure you want to reset the task ID counter? (yes/no): ").lower()

    if confirmation == 'yes':
        global task_id_counter
        task_id_counter = 0
        print("\nTask ID counter has been reset to 0.")
    else:
        print("\nTask ID counter reset cancelled.")
"""

def main_menu():
    load_tasks()

    while True:
        print("\nTask Manager Menu:")
        print("1. Add Task")
        print("2. Update Task")
        print("3. Delete Task")
        print("4. List All Tasks")
        print("5. List Done Tasks")
        print("6. List In-Progress Tasks")
        print("7. List Todo Tasks")
       # print("8. Reset Task ID Counter")
        print("8. Exit")

        choice = input("\nEnter your choice (1-8): ")

        if choice == '1':
            add_task()
        elif choice == '2':
            update_task()
        elif choice == '3':
            delete_task()
        elif choice == '4':
            list_all_tasks()
        elif choice == '5':
            list_done_tasks()
        elif choice == '6':
            list_in_progress_tasks()
        elif choice == '7':
            list_todo_tasks()
        #elif choice == '8':
            #reset_task_id_counter()
        elif choice == '8':
            print("\nExiting Task Manager.")
            break
        else:
            print("\nInvalid choice. Please try again.")
        print("\n")


main_menu()

