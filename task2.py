import math
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import matplotlib.figure
#import chirp

def get_values():
    a = eval(text_result1.get("1.0", "end-1c"))
    analog_frequency = eval(text_result2.get("1.0", "end-1c"))
    sampling_frequency = eval(text_result3.get("1.0", "end-1c"))
    theta = eval(text_result4.get("1.0", "end-1c"))
    var = clicked.get()
    #v= str(drop.current()) + str(var.get())
    print("clicked",clicked.get())
    draw_signal(a, theta, analog_frequency, sampling_frequency,var)


def draw_signal(a, theta, analog_frequency, sampling_frequency,var):
    print(a, theta, analog_frequency, sampling_frequency)

    # Create a time vector
    #t = np.arange(0, sampling_frequency)
    t = np.arange(0,  3.0 ,(analog_frequency/sampling_frequency))
    #t = t = np.arange(0, 12, 1)
    signal = []
    for i in t:
        # Calculate the signal
        # cos signal
        if (var == "cos"):
            signal.append(a * np.cos(2 * np.pi * (analog_frequency/sampling_frequency) * i + (theta))* np.exp(-((i-1.0/sampling_frequency/2)/200)))
        #signal.append(a * np.cos(2 * np.pi * analog_frequency * i + (theta)))
        else :
            # sin signal
            signal.append(a * np.sin((2 * np.pi * (analog_frequency/sampling_frequency) * i) + (theta)))
            #signal.append(chirp(t=i, f0=analog_frequency, fs=sampling_frequency))
            """for i in range(1, len(signal), 2):
                signal[i] = -signal[i]"""


        print("t",i)
        print("s", signal)
    # Plot the signal

    plt.plot(t, signal)
    # Set the plot limits
    plt.xlim([0, t[-1]])
    plt.ylim([-a, a])

    # Add labels and a title
    plt.xlabel("Time (s)")
    plt.ylabel("Signal Amplitude")
    plt.title("Signal with A = {}, Theta = {}, Analog Frequency = {}, Sampling Frequency = {}".format(a, theta, analog_frequency, sampling_frequency))

    # Show the plot
    plt.show()




# Create object
root = Tk()

# Adjust size
root.geometry("550x550")




upperrframe= tk.Frame(root)
upperrframe.columnconfigure(0,weight =1 )
upperrframe.columnconfigure(1,weight =1 )
upperrframe.columnconfigure(2,weight =1 )

label1 = tk.Label(upperrframe,text="magnitude(A)" )
label1.grid(row=0 ,column=0)
label1.pack()

text_result1 = tk.Text(upperrframe, height= 1 , width = 18 ,  font= ("Arial", 12))
#text_result.grid(row=0 ,column=0)
text_result1.pack(padx= 200 , pady=0)
## setting a value


label2 = tk.Label(upperrframe,text="Analog frequancy" )
#label2.grid(row=2 ,column=1)
label2.pack()

text_result2= tk.Text(upperrframe, height= 1 , width = 18 ,  font= ("Arial", 12))
#text_result.grid(row=0 ,column=0)
text_result2.pack(padx= 200 , pady=0)

label3 = tk.Label(upperrframe,text="Sampling frequancy" )
#label3.grid(row=0 ,column=0)
label3.pack()

text_result3 = tk.Text(upperrframe, height= 1 , width = 18 ,  font= ("Arial", 12))
#text_result.grid(row=0 ,column=0)
text_result3.pack(padx= 200 , pady=0)


label4 = tk.Label(upperrframe,text="phase shift " )
#label4.grid(row=0 ,column=0)
label4.pack()

text_result4 = tk.Text(upperrframe, height= 1 , width = 18 ,  font= ("Arial", 12))
#text_result.grid(row=0 ,column=0)
text_result4.pack(padx= 200 , pady=0)


# Dropdown menu options
options = ["sin", "cos"]
# datatype of menu text
clicked = StringVar()
# initial menu text
clicked.set(" function ")
drop = OptionMenu(upperrframe, clicked, *options)
drop.pack()


button = Button(upperrframe, text="show function", command=get_values).pack()
upperrframe.pack(fill='x')
root.mainloop()



# Dropdown menu options

"""
button2 = Button(upperrframe, text="shift", command=(shifting(x,y))).pack()
upperrframe.pack(fill='x')

def show():
    pass

button = Button(root, text="click Me", command=show).pack()

# Change the label text





# Create Dropdown menu


# Create button, it will change label text





#label.pack()

"""
# Execute tkinter
root.mainloop()