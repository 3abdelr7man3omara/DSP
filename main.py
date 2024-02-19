
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import matplotlib.figure

# task 1
import csv
f = open("signal1.txt")

# this function prepares the text file values to be ready for plotting
def prepare_data(f):
        csv_f=csv.reader(f)
        X= []
        Y = []
        # saperating x and y to
        for row in csv_f:
             print(row[0].split())# to get the second and third columns
             X.append(row[0].split()[0])
             try :
                  Y.append(row[0].split()[1])
             except:
                  Y.append('0')
        f.close()
        ## now X , Y are strings so we need to turn them into float
        x = [eval(i) for i in X]
        y = [eval(i) for i in Y]
        return x , y


def plot (x,y):
    ax.clear()
    ax.plot(x, y)
    canvas.draw()
    idx = []
    for i in range(3, len(x) - 1):
        if y[i - 1] <= y[i]or   y[i]>= y[i + 1]:
            idx.append(i)
    for k in idx:
        ax.plot(x[k], y[k], 'ro')
    canvas.draw()



root = tk.Tk()
fig =  matplotlib.figure.Figure()
ax = fig.add_subplot()




frame = tk.Frame(root)
frame.pack()
canvas = FigureCanvasTkAgg(fig, master= root)
canvas.get_tk_widget().pack()

toolbar = NavigationToolbar2Tk(canvas,frame ,pack_toolbar=False)
toolbar.pack(anchor="se", fill=tk.X)
#call prepare data
x,y = prepare_data(f)

tk.Button(frame, text = "plot Signal",command= plot(x,y)).pack()
root.title('DSP Task 1')
root.geometry('750x750')
root.resizable(False, False)
#root.iconbitmap('./assets/pythontutorial.ico')

root.mainloop()

"""
np.random.seed(0)

dt = 0.01 # sampling interval
Fs = 1 / dt # sampling frequency
t = np.arange(0, 10, dt)

# generate noise:
nse = np.random.randn(len(t))
r = np.exp(-t / 0.05)
cnse = np.convolve(nse, r) * dt
cnse = cnse[:len(x)]
s = []
for i in x :
     s = 0.1 * np.sin(4 * np.pi * i) + cnse
fig, axs = plt.subplots()
axs.set_title("Signal")
axs.plot(x, s, color='C0')
axs.set_xlabel("Time")
axs.set_ylabel("Amplitude")

plt.show()

import numpy as np
import matplotlib.pyplot as plt
np.random.seed(2016)


plt.plot(x, s)
start = 0
temp = []
for i in range(len(s)): #ys is my range of y values on the chart
    for j in range(start,len(s)): #Brute forcing peak detection
        temp.append(s[j])
        xval = temp.index(max(temp)) #getting the index
        plt.plot(x[xval+start], max(temp),"ro")
    start =  start + 1
    temp = []
plt.show()
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(2016)

N = 100
ys = (np.random.random(N)-0.5).cumsum()
xs = np.linspace(0, 100, len(s))

plt.plot(x, s)
idx = []
for i in range(1, len(s)-1):
    if s[i-1] <= s[i] >= s[i+1]:
        idx.append(i)
for k in idx:
     plt.plot(x[k], s[k], 'ro')
plt.show()"""


# task 2

