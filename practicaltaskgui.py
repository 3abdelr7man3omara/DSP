import tkinter as tk
from tkinter import ttk
import practicaltask
import numpy as np
from tkinter import filedialog
import CompareSignal_1
import task8
import matplotlib.pyplot as plt

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    entry8.delete(0, tk.END)  # Clear the current content in the Entry widget
    entry8.insert(0, file_path)  # Insert the selected file path into the Entry widget

def browse1_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    entry9.delete(0, tk.END)    # Clear the current content in the Entry widget
    entry9.insert(0, file_path)

def on_button_click(filter, window , signalpath,signalcompare):
    print("filter", filter)
    print("window", window)
    fs = eval(entry1.get())
    stopband = eval(entry2.get())
    fc = eval(entry3.get())
    tw = eval(entry4.get())

    # Display the chosen choices when the button is clicked
    f = []
    w = []
    N = 0
    #"rectangular","hamming", "blackman"
    # first the window
    if window =="rectangular":
        N, w = practicaltask.rectangular(fs=fs, tw=tw)
    elif window =="hanning" :
        N, w = practicaltask.hanning(fs=fs, tw=tw)
    elif window == "hamming":
        N, w = practicaltask.hamming(fs=fs, tw=tw)
    else:
        N, w = practicaltask.blackman(fs=fs, tw=tw)

    #"BSF","LPF", "HPF" , "BPF"
    #second the filter
    if filter == "BSF":
        fc2 = eval(entry7.get())
        Hn = practicaltask.BSF(fs=fs,fc1=fc, fc2=fc2, tw=tw, N=N)
    elif filter == "BPF":
        fc2 = eval(entry7.get())
        Hn = practicaltask.BPF(fs=fs, fc1=fc, fc2=fc2, tw=tw, N=N)
    elif filter =="LPF":
        Hn = practicaltask.LPF(fs=fs, fc=fc, tw=tw, N=N)
    else :
        Hn = practicaltask.HPF(fs=fs, fc=fc, tw=tw, N=N)

    Hn = np.array(Hn)
    w = np.array(w)
    resault = Hn * w
    symmetric_res = np.concatenate((resault[::-1], resault[1:]))
    indix = []

    for i in range(-int(len(symmetric_res) / 2), int(len(symmetric_res) / 2)+1):
        indix.append(i)
    # print(len(symmetric_res), symmetric_res)
    # print(len(indix), indix)

    practicaltask.save_list_to_txt(indix,symmetric_res, "conv.txt")
    ind,symmetric= task8.fast_convol(signalpath, "conv.txt")
    # print(len(symmetric), symmetric)

    CompareSignal_1.Compare_Signals(signalcompare, ind, symmetric)

    return indix, symmetric_res


def on_button2_click(signalpath,signalcompare):
    fs = eval(entry1.get())
    stopband = eval(entry2.get())
    fc = eval(entry3.get())
    tw = eval(entry4.get())
    L = eval(entry5.get())
    M = eval(entry6.get())
    # Display the chosen choices when the button is clicked

    indx, resault = practicaltask.resampling(signalpath, L, M, fs, stopband, fc, tw)

    practicaltask.save_list_to_txt(indx, resault, "resamble.txt")

    CompareSignal_1.Compare_Signals(signalcompare, indx, resault)

    return indx,resault




# Function to update the chosen choice in the corresponding variable
def on_dropdown_change(index, value):
    print("drop_var", drop_var)
    chosen_choices[index] = value

# Create the main window
root = tk.Tk()
root.title("PRACTICAL 1")

# Variables to store the chosen choices

# Create and place entries, text boxes, and drop-down lists
#1
label1 = tk.Label(root, text="FS")
label1.grid(row=0, column=0, padx=5, pady=5)

entry1 = tk.Entry(root)
entry1.grid(row=0, column=1, padx=5, pady=5)

label2 = tk.Label(root, text="StopBandAttenuation")
label2.grid(row=1, column=0, padx=5, pady=5)

entry2 = tk.Entry(root)
entry2.grid(row=1, column=1, padx=5, pady=5)

label3 = tk.Label(root, text="FC")
label3.grid(row=2, column=0, padx=5, pady=5)

entry3 = tk.Entry(root)
entry3.grid(row=2, column=1, padx=5, pady=5)

label4 = tk.Label(root, text="TransitionBand")
label4.grid(row=3, column=0, padx=5, pady=5)

entry4 = tk.Entry(root)
entry4.grid(row=3, column=1, padx=5, pady=5)

label5 = tk.Label(root, text="L")
label5.grid(row=4, column=0, padx=5, pady=5)

entry5 = tk.Entry(root)
entry5.grid(row=4, column=1, padx=5, pady=5)

label6 = tk.Label(root, text="M")
label6.grid(row=5, column=0, padx=5, pady=5)

entry6 = tk.Entry(root)
entry6.grid(row=5, column=1, padx=5, pady=5)

label7 = tk.Label(root, text="FC2 (in BPF or BSF)")
label7.grid(row=6, column=0, padx=5, pady=5)

entry7 = tk.Entry(root)
entry7.grid(row=6, column=1, padx=5, pady=5)

label8 = tk.Label(root, text="Path for signal tests")
label8.grid(row=7, column=0, padx=5, pady=5)

entry8 = tk.Entry(root)
entry8.grid(row=7, column=1, padx=5, pady=5)

label8 = tk.Label(root, text="Path for compare tests")
label8.grid(row=8, column=0, padx=5, pady=5)

entry9 = tk.Entry(root)
entry9.grid(row=8, column=1, padx=5, pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=7, column=2, padx=5, pady=5)

browse_button = tk.Button(root, text="Browse", command=browse1_file)
browse_button.grid(row=8, column=2, padx=5, pady=5)

chosen_choices = [tk.StringVar() for _ in range(6)]


drop_var = chosen_choices[5]
drop_values = ["BSF","LPF", "HPF" , "BPF"]  # Customize options as needed
dropdown = ttk.Combobox(root, values=drop_values, textvariable=drop_var)
dropdown.current(0)  # Set default value
dropdown.grid(row=9, column=0, padx=5, pady=5)
#dropdown.bind("<<ComboboxSelected>>", lambda event, var=drop_var: on_dropdown_change(1, var.get()))

# window types
drop_values2 = ["rectangular", "hanning",  "hamming", "blackman"]
drop_var2 = drop_values2[2]
dropdown2 = ttk.Combobox(root, values=drop_values2, textvariable=drop_var2)
dropdown2.current(0)  # Set default value
dropdown2.grid(row=9, column=1, padx=5, pady=5)
#dropdown2.bind("<<ComboboxSelected>>", lambda event, index=1, var=drop_var: on_dropdown_change(index, var.get()))

chosen_choices = [tk.StringVar() for _ in range(6)]

# Create and place a button
button1 = tk.Button(root, text="fir", command=lambda : on_button_click(dropdown.get(), dropdown2.get(), entry8.get(),entry9.get()))
button1.grid(row=10, columnspan=3, pady=10)

button2 = tk.Button(root, text="resamble", command=lambda : on_button2_click(entry8.get(),entry9.get()))
button2.grid(row=11, columnspan=3, pady=10)
# Create a label to display the chosen choices
result_label = tk.Label(root, text="")
result_label.grid(row=12, columnspan=3, pady=10)

# Run the Tkinter main loop
root.mainloop()
