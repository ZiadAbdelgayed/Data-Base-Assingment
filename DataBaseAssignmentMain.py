######################################### imports #########################################
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import sqlite3
import database
######################################### imports #########################################



######################################### Var #########################################
connection = database.connect()
database.create_tables(connection)
options = [
    "Diff ASC", 
    "Diff DSC",
    "None",
] 
######################################### Var #########################################



######################################### Window Config #########################################
window = Tk()
window.geometry("900x680")
window.configure(bg='dark slate gray')
window.title("To-DO List")  
######################################### Window Config #########################################



######################################### Classes #########################################
class TaskWidget:
    numOfTaskWidgets = []
    
    def __init__(self, text):
        self.text = text
        self.frame = Frame(canvas,
                           width=270,
                           height=100,
                           bg="mistyrose3")     
        self.taskLabel = Text(self.frame, 
                              height=3,  
                              width=30,
                              bg="mistyrose3",
                              wrap="word",
                              state='normal')  
        self.taskLabel.insert("1.0", text[3])
        self.nameLabel = Label(self.frame, 
                           text=text[1], 
                           bg="lavender", 
                           width = 30,
                           height=1,
                           justify = LEFT,
                           anchor="w")
        self.diffLabel = Label(self.frame, 
                           text=text[2], 
                           bg="lavender")
        self.button = Button(self.frame,
                             bg="white",
                             height=1,
                             width=2,
                             text="X",
                             command=lambda: self.delWidget())

        
    def delWidget(self):
        getId = self.text[0]
        database.deleteTask(connection, getId)
        self.numOfTaskWidgets.remove(self)
        self.frame.destroy()
        hideAllWidgets()
        displayTask()

    def grid(self, **kwargs):
        self.frame.grid(kwargs, padx=7, pady=7)
        self.nameLabel.place(y=5,x=30)
        self.diffLabel.place(y=5,x=250)
        self.taskLabel.place(y=32,x=5)
        self.button.place(y=5,x=5)
    
    def color(self, color):
        self.frame.config(bg=color)
        self.taskLabel.config(bg=color)

    

class Task:
    listOfTasks = []
    def __init__(self, name, difficulty, task):
        self.name = name
        self.difficulty = difficulty
        self.task = task
    
    def printTasks():
        for task in Task.listOfTasks:
            print(f"Name: {task.name}, Diff: {task.difficulty}, Task: {task.task}")
        print("DataBase: ")
        tasks = database.getAllTasks(connection)
        for task in tasks:
            print(f"{task[1]}, {task[2]}, {task[3]}")
    

    @classmethod
    def addTask(cls, name, diff, do):
        task1 = Task(name, diff, do)
        Task.listOfTasks.append(task1)
        database.addTask(connection, name, diff, do)
######################################### Classes #########################################



######################################### Functions #########################################
def submit(): 
    name = nameInputBox.get().strip()
    difficulty = difficultyInputBox.get()
    task = taskInputBox.get("1.0",'end-1c')
    try:
        if len(name) != 0:
            if int(difficulty) < 100:
                difficulty = int(difficulty)
                Task.addTask(name, difficulty, task)
                displayTask()
            else:
                difficultyInputBox.config(bg="red")
                window.after(500, lambda: difficultyInputBox.config(bg="white"))
                messagebox.showerror('Python Error', 'Error: Please Enter a Number Between 1-99!')
        else:
            nameInputBox.config(bg="red")
            window.after(500, lambda: nameInputBox.config(bg="white"))
            messagebox.showerror('Python Error', 'Error: Please Enter a Name')
    except ValueError:
        difficultyInputBox.config(bg="red")
        window.after(500, lambda: difficultyInputBox.config(bg="white"))
        messagebox.showerror('Python Error', 'Error: Please Enter a Number!')
    
    


def refreshTasks(list):
    hideAllWidgets()
    x, y = 0,0
    for task in list:
        Task.listOfTasks.append(task)
        widget =  TaskWidget(task)
        TaskWidget.numOfTaskWidgets.append(widget)
        widget.grid(row=y, column=x)
        x += 1
        if x == 2:
            y += 1
            x = 0
    canvas.update_idletasks() 
    canvas.configure(scrollregion=canvas.bbox("all"))

def checkDropDown(*args):
    x = clicked.get()
    if x == "Diff ASC":
        orderAsc()
    elif x == "Diff DSC":
        orderDsc()
    else:
        displayTask()

def orderAsc():
    refreshTasks(database.orderAscOrder(connection))
    

def orderDsc():
    refreshTasks(database.orderDscOrder(connection))


def displayTask():
    refreshTasks(database.getAllTasks(connection))


def tempTextDel(e):
    searchBar.delete("1.0","end")

def tempTextIns(e):
    searchBar.delete("1.0","end")
    searchBar.insert("1.0", "🔍 Search")

def hideAllWidgets():
    for tasks in TaskWidget.numOfTaskWidgets:
        hideWidget(tasks)

def hideWidget(widget):
    widget.frame.grid_forget()

def checkText(e):
    inputText = searchBar.get("1.0",'end-1c').lower()
    hideAllWidgets()   
    if inputText:
        x, y = 0, 0
        VisibleTasks = []
        for tasks in TaskWidget.numOfTaskWidgets:
            LabelText = tasks.text
            if len(LabelText) > 1 and inputText in LabelText[1].lower():
                VisibleTasks.append(tasks)
        for tasks in VisibleTasks:
            tasks.grid(row=y, column=x)
            x += 1
            if x == 2:
                y += 1
                x = 0
    else:
        TaskWidget.numOfTaskWidgets.clear()
        tasks = database.getAllTasks(connection)
        x, y = 0, 0
        for task in tasks:
            widget = TaskWidget(task)
            TaskWidget.numOfTaskWidgets.append(widget)
            widget.grid(row=y, column=x)
            x += 1
            if x == 2:
                y += 1
                x = 0

def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

def checkColorDropDown(*args):
    selectedColor = colorClicked.get()
    tasks = TaskWidget.numOfTaskWidgets
    for task in tasks:
        task.color(selectedColor)
######################################### Functions #########################################



######################################### Widgets #########################################
frame = Frame(window, width=500, height=570, bg='dark slate gray')
canvas = Canvas(frame, width=540, height=570, bg="slate gray", scrollregion=(0,0,540,570))
scrollbar = Scrollbar(frame)
scrollbar.config(command=canvas.yview)
canvas.config(yscrollcommand=scrollbar.set)


canvas.bind_all("<MouseWheel>", on_mouse_wheel)
scrollbar.pack(side = LEFT, fill=Y)
canvas.pack(expand=True, fill=BOTH)
frame.place(x=10,y=10)


buttonsFrame = Frame(window, width=280, height=600,bg='grey')
buttonsFrame.place(x=600,y=10)

searchBar = Text(buttonsFrame, width=20, height=2)
searchBar.insert("1.0", "🔍 Search")
searchBar.bind("<FocusIn>", tempTextDel)
searchBar.bind("<FocusOut>", tempTextIns)
searchBar.bind("<KeyRelease>", checkText)


clicked = StringVar() 
clicked.set("None")
dropDown = OptionMenu(buttonsFrame, clicked , *options)
dropDown.place(x=200,y=10)
clicked.trace("w", checkDropDown)

nameInputLbl = Label(buttonsFrame, font=("Arial", 12), width=25, bg="grey", fg="black", text="Name Of Task", justify = LEFT, anchor="w")
nameInputBox = Entry(buttonsFrame, font=("Arial", 12), width=25, bg="white", fg="black")
difficultyInputLbl = Label(buttonsFrame, font=("Arial", 12), width=25, bg="grey", fg="black", text="Difficulty Of Task (0-99)", justify = LEFT, anchor="w")
difficultyInputBox = Entry(buttonsFrame, font=("Arial", 12), width=25, bg="white", fg="black")
taskInputLbl = Label(buttonsFrame, font=("Arial", 12), width=25, bg="grey", fg="black", text="Task Discreption", justify = LEFT, anchor="w")
taskInputBox = Text(buttonsFrame, font=("Arial", 12), width=25, height=5, bg="white", fg="black")

searchBar.place(x=10, y=10)
nameInputLbl.place(x=10, y=100)
nameInputBox.place(x=10, y=125)
difficultyInputLbl.place(x=10, y=160)
difficultyInputBox.place(x=10, y=185)
taskInputLbl.place(x=10, y=220)
taskInputBox.place(x=10, y=245)

inputButton = Button(buttonsFrame, text="Submit Task", width = 15, command=submit, font=("Arial", 12), bg="lightblue", fg="black")
inputButton.place(x=10, y=360)

    
colorClicked = StringVar() 
colorClicked.set("None")
colorDropDown = OptionMenu(buttonsFrame, colorClicked , *database.colorOptions)
colorDropDown.place(x=10,y=500)
colorClicked.trace("w", checkColorDropDown)
######################################### Widgets #########################################



######################################### AppLoop #########################################
displayTask()
window.mainloop()
######################################### AppLoop #########################################