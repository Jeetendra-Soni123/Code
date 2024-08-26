import tkinter as tk
from tkinter import messagebox as msgbox
from tkinter import ttk
from datetime import datetime

today = str(datetime.today())

root = tk.Tk()
root.geometry("700x900")

def delete_task():
    selected_index = taskbox.curselection()
    if selected_index:
        taskbox.delete(selected_index)
        save_tasks()  # Save after deletion
        newWindow.destroy()


def edit_task():
    selected_index = taskbox.curselection()
    if selected_index:
        add_window(is_edit=True, selected_task_index=selected_index[0])

def add_window(is_edit=False, selected_task_index=None):
    newWindow = tk.Toplevel(root)
    newWindow.title("New Task Window" if not is_edit else "Edit Task Window")
    newWindow.geometry("500x700")
    if is_edit:
        def delete_task():
            selected_index = taskbox.curselection()
            if selected_index:
                taskbox.delete(selected_index)
                save_tasks()  # Save after deletion
                newWindow.destroy()
        delete=tk.Button(newWindow, text="Delete", command=delete_task, width=10)
        delete.grid(row=16, column=0, padx=120, pady=20, sticky='w')


    # Variables
    task_var = tk.StringVar()
    priority_var = tk.StringVar()

    # Default values for date and time
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    now = datetime.now()
    current_day = now.day
    current_month = now.month
    current_year = now.year
    current_hour = now.hour
    current_minute = now.minute
    current_am_pm = "AM" if current_hour < 12 else "PM"
    current_hour_12 = current_hour if 1 <= current_hour <= 12 else current_hour - 12
    if current_hour_12 == 0:
        current_hour_12 = 12

    # If editing, pre-fill with existing data
    if is_edit and selected_task_index is not None:
        task_details = taskbox.get(selected_task_index)
        details_parts = task_details.split("    (Due: ")
        if len(details_parts) > 1:
            task_part = details_parts[0].strip()
            due_part = details_parts[1][:-1]  # Remove the closing parenthesis

            # Extract priority and task description
            if "] " in task_part:
                task_priority = task_part.split("] ")[0][1:].strip()
                task_content = task_part.split("] ")[1].strip()
                task_var.set(task_content)
                priority_var.set(task_priority)
            else:
                task_var.set(task_part.strip())
                priority_var.set("")

            # Extract date and time
            try:
                date_part, time_part = due_part.split(" time: ")
                day, month, year = map(int, date_part.split('-'))
                hour_minute, am_pm = time_part.split(' ')
                hour, minute = map(int, hour_minute.split(':'))

                # Convert 24-hour time to 12-hour format if needed
                if hour == 0:
                    hour = 12
                    am_pm = "AM"
                elif hour > 12:
                    hour -= 12
                    am_pm = "PM"
                elif hour == 12:
                    am_pm = "PM"
                else:
                    am_pm = "AM"

            except ValueError:
                # Default to current date and time in case of parse error
                day, month, year, hour, minute, am_pm = current_day, current_month, current_year, current_hour_12, current_minute, current_am_pm
        else:
            # Default to current date and time
            day, month, year, hour, minute, am_pm = current_day, current_month, current_year, current_hour_12, current_minute, current_am_pm
    else:
        # Default to current date and time
        day, month, year, hour, minute, am_pm = current_day, current_month, current_year, current_hour_12, current_minute, current_am_pm

    # New Window Functions
    def dis_win():
        newWindow.destroy()

    def event_ok():
        # Get values
        priority = priority_var.get()
        task = task_var.get()
        day = int(day_combobox.get())
        month_name = month_combobox.get()
        year = int(year_combobox.get())
        hour = int(hour_combobox.get())
        minute = int(minute_combobox.get())
        am_pm = am_pm_var.get()

        # Convert month name to month number
        month = months.index(month_name) + 1

        # Convert 12-hour format to 24-hour format
        if am_pm == "PM" and hour != 12:
            hour += 12
        elif am_pm == "AM" and hour == 12:
            hour = 0

        # Validate that the selected date and time are in the future
        if task == "" or priority == "":
            if task == "":
                msgbox.showerror("Invalid", "Please enter a Task")
            elif priority == "":
                msgbox.showerror("Invalid", "Please select a priority")
        else:
            try:
                selected_date_time = datetime(year, month, day, hour, minute)
                current_date_time = datetime.now()

                if selected_date_time > current_date_time:
                    time = f"date: {selected_date_time.strftime('%d-%m-%Y')} time: {selected_date_time.strftime('%I:%M %p')}"
                    task_details = f"[{priority}] {task}    (Due: {time})"

                    if is_edit and selected_task_index is not None:
                        taskbox.delete(selected_task_index)
                        taskbox.insert(selected_task_index, task_details)
                    else:
                        taskbox.insert('end', task_details)

                    save_tasks()  # Save after adding or editing a task
                    dis_win()

                else:
                    msgbox.showerror("Invalid", "The selected date and time must be in the future.")
            except ValueError:
                msgbox.showerror("Invalid", "The selected date and time are not valid.")

    # New window layout Entry
    tk.Label(newWindow, text="Enter the Task Description").grid(row=0, column=0, columnspan=2, padx=10, pady=1, sticky='nw')
    task_entry = tk.Entry(newWindow, width=40, textvariable=task_var)
    task_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nw")

    # Priority layout
    tk.Label(newWindow, text="Choose your priority").grid(row=8, column=0, sticky="sw")
    low = tk.Radiobutton(newWindow, text="Low", variable=priority_var, value="low")
    mid = tk.Radiobutton(newWindow, text="Medium", variable=priority_var, value="mid")
    high = tk.Radiobutton(newWindow, text="High", variable=priority_var, value="high")

    low.grid(row=9, column=0, sticky="sw")
    mid.grid(row=10, column=0, sticky="sw")
    high.grid(row=11, column=0, sticky="sw")

    # Configure grid layout for date and time selection

    # Date
    tk.Label(newWindow, text="Day:", font=('Arial', 10)).grid(row=2, column=0, padx=2, pady=5, sticky='w')
    day_combobox = ttk.Combobox(newWindow, values=list(range(1, 32)), width=5)
    day_combobox.grid(row=3, column=0, padx=2, pady=8, sticky='w')
    day_combobox.set(day)

    tk.Label(newWindow, text="Month:", font=('Arial', 10)).grid(row=2, column=0, padx=105, pady=5, sticky='w')
    month_combobox = ttk.Combobox(newWindow, values=months, width=10)
    month_combobox.grid(row=3, column=0, padx=105, pady=8, sticky='w')
    month_combobox.set(months[month - 1])

    tk.Label(newWindow, text="Year:", font=('Arial', 10)).grid(row=2, column=0, padx=278, pady=5, sticky='w')
    year_combobox = ttk.Combobox(newWindow, values=list(range(current_year, current_year + 101)), width=5)
    year_combobox.grid(row=3, column=0, padx=278, pady=8, sticky='w')
    year_combobox.set(year)

    # Time
    tk.Label(newWindow, text="Hour:", font=('Arial', 10)).grid(row=4, column=0, padx=2, pady=5, sticky='w')
    hour_combobox = ttk.Combobox(newWindow, values=list(range(1, 13)), width=5)
    hour_combobox.grid(row=5, column=0, padx=2, pady=8, sticky='w')
    hour_combobox.set(hour)

    tk.Label(newWindow, text="Minute:", font=('Arial', 10)).grid(row=4, column=0, padx=105, pady=5, sticky='w')
    minute_combobox = ttk.Combobox(newWindow, values=list(range(0, 60)), width=5)
    minute_combobox.grid(row=5, column=0, padx=105, pady=8, sticky='w')
    minute_combobox.set(minute)

    tk.Label(newWindow, text="AM/PM:", font=('Arial',10)).grid(row=6, column=0, padx=10, pady=5, sticky='w')
    am_pm_var = tk.StringVar()
    am_pm_var.set(am_pm)
    am_pm_combobox = ttk.Combobox(newWindow, textvariable=am_pm_var, values=["AM", "PM"], width=5)
    am_pm_combobox.grid(row=6, column=0, padx=130, pady=8, sticky='w')

    # Buttons for Cancel and OK
    cancel = tk.Button(newWindow, text="Cancel", command=dis_win, width=10)
    cancel.grid(row=15, column=0, padx=10, pady=20, sticky='w')

    ok = tk.Button(newWindow, text="OK", command=event_ok, width=10)
    ok.grid(row=15, column=0, padx=250, pady=20, sticky='w')


def save_tasks():
    with open("tasks.txt", "w") as file:
        for i in range(taskbox.size()):
            file.write(taskbox.get(i) + "\n")

def load_tasks():
    try:
        with open("tasks.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                taskbox.insert('end', line.strip())
    except FileNotFoundError:
        pass  # No tasks file exists, nothing to load

# Initialize taskbox
taskbox = tk.Listbox(root, height=25, width=70)
taskbox.grid(row=0, column=0, sticky='nw', pady=10, padx=10, columnspan=5)

# Add button to add tasks
addTask = tk.Button(root, text="+ Add Task", command=lambda: add_window(is_edit=False), bg="#118afa", font=('bold', 20))
addTask.grid(row=3, column=4, sticky='se')

# Bind Listbox Select Event
taskbox.bind('<<ListboxSelect>>', lambda e: edit_task() if taskbox.curselection() else None)

# Load tasks when the program starts
load_tasks()

# Monitor changes in the Listbox and save tasks when necessary
def on_listbox_change(event):
    save_tasks()

taskbox.bind('<Configure>', on_listbox_change)  # Save tasks when the Listbox is resized

root.mainloop()