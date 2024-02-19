import tkinter as tk


#function that takes button name to see which task will open
def import_tasks(s):
        if s == 'task1.1':
                import main # importing files names
        elif s == 'task2':
                import task2
        elif s == 'task3' :
                import task3
        elif s == "task4":
                import task4
        elif s == "task5":
                import task5
        elif s == "task7":
                import task7

# For example, you can import and execute your project's main script

root = tk.Tk()

welcome_label = tk.Label(root, text="Welcome to Your Project")
welcome_label.pack(pady=20)  # Adds padding to separate the label and button
############################ any name for button ################names below should be like the names in the Fun.
button1 = tk.Button(root, text="Open task 1", command=lambda: import_tasks("task1.1"))
button1.pack()

button2 = tk.Button(root, text="Open task 2", command=lambda: import_tasks("task2"))
button2.pack()

button3 = tk.Button(root, text="Open task 3", command=lambda: import_tasks("task3"))
button3.pack()

button4 = tk.Button(root, text="Open task 4", command=lambda: import_tasks("task4"))
button4.pack()

button5 = tk.Button(root, text="Open task 5", command=lambda: import_tasks("task5"))
button5.pack()

button7 = tk.Button(root, text="Open task 7", command=lambda: import_tasks("task7"))
button7.pack()

root.title("DSP TASKS")
root.geometry('400x400')
root.resizable(True, True)

root.mainloop()