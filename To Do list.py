import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime
today=str(datetime.today())

root=tk.Tk()

root.geometry("200x300")

#Functions
def add_task():
	task=taskName.get()
	#tk.Label(root,text=f"{task}",font=("bold",15)).pack(padx=3)
	print(task)
	listbox.insert('end',task)

def delete_task():
	value=listbox.curselection()
	#tk.Label(root,text=f"{value}",font=("bold",15)).pack(padx=3)
	listbox.delete(value)
	
def edit_task():
	value=listbox.curselection()
	description = simpledialog.askstring("Task", "Enter new description:")
	task=f"{description}        edited ({today[:19]})"
	tk.Label(root,text=f"{value},  {description}",font=("bold",15)).pack(padx=3)
	listbox.delete(value)
	listbox.insert(value,task)
	


taskName=tk.Entry(root)
taskName.pack(pady=20,ipady=10)

addTask=tk.Button(root,text="Add Task",command=add_task)
addTask.pack(anchor='center')

deleteTask=tk.Button(root,text="Delet Task",command=delete_task)
deleteTask.pack(anchor='center')

editTask=tk.Button(root,text="Edit Task",command=edit_task)
editTask.pack(anchor='center')

listbox=tk.Listbox(root,height=10,width=40)
listbox.pack(anchor='center',pady=30)



root.mainloop()