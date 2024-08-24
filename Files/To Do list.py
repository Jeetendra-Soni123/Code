import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime
today=str(datetime.today())

root=tk.Tk()

root.geometry("600x700")

#Functions
def add_task():
	description = simpledialog.askstring("Task", "Enter task description:")
	task=f"{description}        added({today[:19]})"
	#tk.Label(root,text=f"{task}",font=("bold",15)).grid(padx=3)
	print(task)
	listbox.insert('end',task)

def delete_task():
	value=listbox.curselection()
	#tk.Label(root,text=f"{value}",font=("bold",15)).grid(padx=3)
	listbox.delete(value)
	
def edit_task():
	value=listbox.curselection()
	description = simpledialog.askstring("Task", "Enter new description:")
	task=f"{description}        edited ({today[:19]})"
	tk.Label(root,text=f"{value},  {description}",font=("bold",15)).grid(padx=3)
	listbox.delete(value)
	listbox.insert(value,task)
	

deleteTask=tk.Button(root,text="Delete Task",command=delete_task)
deleteTask.grid(sticky='nw')

editTask=tk.Button(root,text="Edit Task",command=edit_task)
editTask.grid(sticky='nw')

listbox=tk.Listbox(root,height=10,width=100)
listbox.grid(sticky='nw',pady=10, padx=10)

addTask=tk.Button(root,text="+ Add Task",command=add_task,bg="#118afa",font=('bold',20))
addTask.grid(sticky='se')



root.mainloop()