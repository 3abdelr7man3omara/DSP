from tkinter import *
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
#import plotly.express as px

root = Tk()
root.geometry("800x500")

AmpMax_var = tk.StringVar()
theta_var = tk.StringVar()
F_var = tk.StringVar()
fs_var = tk.StringVar()

root.title("signal")
file = open('signal1.txt', 'r')
content = file.readlines()
print(content[2:])
list1 = content[2:]
n = list1[0]
x = list1[1:]
print(n)
file.close()
for i in range(int(n) + 1):
    x[i] = x[i].split(' ')[0]
y = list1[1:]
for i in range(int(n) + 1):
    y[i] = float(y[i].split(' ')[1].replace('\n', ' '))
    print(y[i])


def btn_print():
    plt.plot(x, y)
    plt.show()
    plt.plot(x, y, 'o-')
    plt.show()


btn1 = Button(root, command=btn_print, text="show result")

lb1 = Label(root, text="amp")
et1 = Entry(root)
et1.pack()
lb1.pack()

lb2 = Label(root, text="phase shift")
et2 = Entry(root)
et2.pack()
lb2.pack()

lb3 = Label(root, text="analog fre")
et3 = Entry(root)
et3.pack()
lb3.pack()

lb4 = Label(root, text="sampling fre")
et4 = Entry(root)
et4.pack()
lb4.pack()


def hello():
    AmpMax = eval(et1.get())
    theta = eval(et2.get())
    F = eval(et3.get())
    fs = eval(et4.get())
    n = np.arange(1, 10, 1)
    amp=[]
    for i in n:
         amp.append( AmpMax * np.sin(2 * np.pi * i * (F / fs) + theta))
    plt.plot(n / fs, amp)
    plt.show()


checkbtn = tk.Checkbutton(root, text="sin", command=hello)
checkbtn.pack()


def hi():
    AmpMax = eval(et1.get())
    theta = eval(et2.get())
    F = eval(et3.get())
    fs = eval(et4.get())
    n = np.arange(1, 10, 1)
    amp = []
    for i in n:
        amp.append(AmpMax * np.cos(2 * np.pi * i * (F / fs) + theta))
    plt.plot(n / fs, amp)
    plt.show()


checkbtn2 = tk.Checkbutton(root, text="cos", command=hi)
checkbtn2.pack()

btn1.pack()

root.mainloop()