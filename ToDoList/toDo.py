import tkinter as tk
from tkinter import messagebox
import json

# Load tasks from a file
def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save tasks to a file
def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)

# Add a task
def add_task():
    task_name = task_entry.get()
    due_date = date_entry.get()
    if task_name and due_date:
        tasks.append({'task_name': task_name, 'due_date': due_date, 'status': 'pending'})
        save_tasks(tasks)
        update_task_list()
        task_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter both task name and due date.")

# Update the task list on the GUI
def update_task_list():
    task_listbox.delete(0, tk.END)
    for idx, task in enumerate(tasks, 1):
        task_listbox.insert(tk.END, f"{idx}. {task['task_name']} - Due: {task['due_date']} - Status: {task['status']}")

# Mark a task as completed
def mark_completed():
    try:
        selected_task_index = task_listbox.curselection()[0]
        task = tasks[selected_task_index]
        task['status'] = 'completed'
        save_tasks(tasks)
        update_task_list()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

# Delete a task
def delete_task():
    try:
        selected_task_index = task_listbox.curselection()[0]
        del tasks[selected_task_index]
        save_tasks(tasks)
        update_task_list()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

# Edit a task
def edit_task():
    try:
        selected_task_index = task_listbox.curselection()[0]
        task = tasks[selected_task_index]
        new_task_name = task_entry.get()
        new_due_date = date_entry.get()
        
        if new_task_name and new_due_date:
            task['task_name'] = new_task_name
            task['due_date'] = new_due_date
            save_tasks(tasks)
            update_task_list()
            task_entry.delete(0, tk.END)
            date_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter both task name and due date.")
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to edit.")

# Set up the main window
root = tk.Tk()
root.title("To-Do List")
root.geometry("600x400")  # Set the window size

# Load tasks
tasks = load_tasks()

# Task input widgets
task_label = tk.Label(root, text="Task:")
task_label.grid(row=0, column=0)
task_entry = tk.Entry(root, width=40)  # Increase width of task entry
task_entry.grid(row=0, column=1)

date_label = tk.Label(root, text="Due Date (YYYY-MM-DD):")
date_label.grid(row=1, column=0)
date_entry = tk.Entry(root, width=40)  # Increase width of date entry
date_entry.grid(row=1, column=1)

# Buttons
add_button = tk.Button(root, text="Add Task", command=add_task, width=20, height=2)  # Larger buttons
add_button.grid(row=2, column=0, columnspan=2, pady=10)

edit_button = tk.Button(root, text="Edit Task", command=edit_task, width=20, height=2)
edit_button.grid(row=3, column=0, columnspan=2, pady=5)

delete_button = tk.Button(root, text="Delete Task", command=delete_task, width=20, height=2)
delete_button.grid(row=4, column=0, columnspan=2, pady=5)

mark_button = tk.Button(root, text="Mark as Completed", command=mark_completed, width=20, height=2)
mark_button.grid(row=5, column=0, columnspan=2, pady=5)

# Task listbox
task_listbox = tk.Listbox(root, width=50, height=15)  # Increase listbox height
task_listbox.grid(row=6, column=0, columnspan=2, pady=10)

# Update the task list in the GUI
update_task_list()

# Run the application
root.mainloop()
