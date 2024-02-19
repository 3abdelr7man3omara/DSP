import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import matplotlib.figure
import csv
import math



def prepare_data(file_path):
    with open(file_path, 'r') as f:
        csv_f = csv.reader(f)
        x_data = []
        y_data = []

        for row in csv_f:
            try:
                x_value = float(row[0].split()[0])
                y_value = float(row[0].split()[1])
                x_data.append(x_value)
                y_data.append(y_value)
            except (ValueError, IndexError):
                pass

    return x_data, y_data


def encode_combined_x(combined_x,l):
    #max_value = max(combined_x)
    max_bits =math.floor( math.log2(l))
    #max_bits=3
    encoded_x = []
    for i in combined_x:
        # Convert the value to an integer
        int_value = int(i)
        # Convert the integer to a binary string with the maximum number of bits
        binary_string = format(int_value, '0{}b'.format(max_bits))
        # Append the binary string to the encoded_x list
        encoded_x.append(binary_string)
    return encoded_x
def quantization(y, x, l):
    delta = (((np.max(y)) - (np.min(y)))) / l
    print ("delta", delta)
    rangepoints = []
    combined_x = []
    combined_y = []
    midpoint = []
    err =[]
    a =round( (np.min(y)+(delta/2)), 3)
    d = round((delta / 2),2)

    rangepoints.append(a)
    for i in range(l):
        a = round((a + (d*2)),3)
        rangepoints.append(a)
        midpoint.append(round(((rangepoints[i]+rangepoints[i+1])/2),2))
    print("midpoint", midpoint)
    for i in range(len(y)):
        for j in range(len(rangepoints)):
            result = abs(y[i] - rangepoints[j])
            result_rounded = round(result, 3)
            if  result_rounded  < d  :
                combined_y.append(j+1)
                combined_x.append(x[i])
        if y[i] == np.max(y):
                combined_y.append(j )
                combined_x.append(x[i])
        elif y[i] == np.min(y):
            combined_y.append(0)
            combined_x.append(x[i])
def quantization(y, x, l):
    delta = float(((np.max(y)) - (np.min(y))) ) / l
    print ("delta", delta)
    rangepoints = []
    combined_x = []
    combined_y = []
    midpoint = []
    err =[]
    d = (delta / 2)
    print("d", d)
    a = np.min(y) + d
    rangepoints.append(a)
    i=0
    while a <= np.max(y):
        a = float("%0.2f" % float(a))
        print(a)
        a = a +(d*2)
        rangepoints.append(a )
        midpoint.append((((rangepoints[i]+rangepoints[i+1])/2)))
        i = i+1
    print("midpoint", midpoint)
    for i in range(len(y)):
        for j in range(len(rangepoints)):

            if abs(y[i] - rangepoints[j])  <= (delta / 2)  :
                combined_y.append(j)
                combined_x.append(x[i])
                print("now " ,y[i]  )
                err.append(y[i] - rangepoints[j])
            elif abs(y[i] - rangepoints[j]) == (delta / 2):
                           combined_y.append(j)
                           err.append(y[i] - rangepoints[j])
                           combined_x.append(x[i])


                           #result_rounded = round(result, 4)
            """if y[i] == np.max(y):
                combined_y.append(j + 1)
                combined_x.append(x[i])"""
        """if (np.max(y) == y[i]):
            print("max ", y[i])

            combined_y.append(j)
            combined_x.append(x[i])"""


    print("rangepoints:", rangepoints)
    print("combined_x:", combined_x)
    print("combined_y:", combined_y)
    print("err:", err)

    return combined_x, combined_y

def plot_signals(selected_indices, operation, constant):
    ax.clear()
    combined_x = []
    combined_y = []
    for idx in selected_indices:
        x, y = prepare_data(filenames[idx])
        ax.plot(x, y, label=f'Signal {idx + 1}')
        combined_x = x if not combined_x else combined_x  # Use the x values from the  selected signal

        if operation == "add":
            combined_y = [y1 + y2 for y1, y2 in zip(combined_y, y)] if combined_y else y  # Add
        elif operation == "subtract":
            combined_y = [y2 - y1 for y1, y2 in zip(combined_y, y)] if combined_y else y  # Subtract
        elif operation == "multiply":
            combined_y = [y1 * constant for y1 in y]  # Multiply
        elif operation == "square":
            combined_y = [y1 ** 2 for y1 in y]  # Squaring
        elif operation == "shift":
            s = eval(shift.get())
            shifted_x = [x1+s for x1 in x ]
            print(len(shifted_x))
            print(len(y))
            ax.plot(shifted_x, y, label="Combined Signal", linestyle='--', color='k')
            ax.legend()
            canvas.draw()
            combined_x = shifted_x
            combined_y = y
        elif operation == "normalize1":
            x_max = np.max(x)
            x_min = np.min(x)
            combined_x = [((x1 - x_min) / (x_max - x_min))for x1 in x]
            combined_y = y
            ax.clear()
        elif operation == "normalize2":
            x_max = np.max(x)
            x_min = np.min(x)
            combined_x = [((2*(x1 - x_min) / (x_max - x_min)-1))for x1 in x]
            combined_y = y
            ax.clear()
        elif operation =="accumulative":
            combined_y=np.cumsum(x)
            combined_x = x
            ax.clear()
        elif operation =="Quantization":
            print("x" , x)
            print("y" , y)
            var = clicked.get()
            l = eval(level.get())
            if var == "bits":
                l = math.pow(2,l)
            combined_x,combined_y = quantization (y,x,l)
            #combined_x = x
            encodecombined_x = encode_combined_x(combined_y,l)
            print("encodecombined_x",encodecombined_x)

            ax.clear()
    ax.plot(combined_x, combined_y, label="Combined Signal", linestyle='--', color='k')
    ax.legend()
    canvas.draw()


filenames = [
    'C:/Users/SCH/Downloads/input signals/Input Shifting.txt',   # array for all possible file paths
    'C:/Users/SCH/Downloads/input signals/Signal1.txt',   # Add more file paths if needed
    'C:/Users/SCH/Downloads/input signals/Signal2.txt',
    'C:/Users/SCH/Downloads/input signals/signal3.txt',
    'C:/Users/SCH/Downloads/Quan1_input.txt',
    'C:/Users/SCH/Downloads/Quan2_input.txt'

]

root = tk.Tk()
fig = matplotlib.figure.Figure()
ax = fig.add_subplot()

frame = tk.Frame(root)
frame.pack()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()






tk.Label(frame, text="Number of Signals to Plot:").pack()
num_signals_entry = tk.Entry(frame)
num_signals_entry.pack()
num_signals_entry.insert(0, str(len(filenames)))

tk.Label(frame, text="Select Signals to Plot (comma-separated indices):").pack()
selected_indices_entry = tk.Entry(frame)
selected_indices_entry.pack()

tk.Label(frame, text="Constant for Multiplication:").pack()
constant_entry = tk.Entry(frame)
constant_entry.pack()
constant_entry.insert(0, "1")

tk.Label(frame, text="Constant for shift:").pack()
shift = tk.Entry(frame)
shift.pack()
shift.insert(0, "0")

tk.Button(frame, text="Add Signals", command=lambda: plot_signals(
    [int(idx) for idx in selected_indices_entry.get().split(",") if idx.strip()], "add", None)).pack()

tk.Button(frame, text="Subtract Signals", command=lambda: plot_signals(
    [int(idx) for idx in selected_indices_entry.get().split(",") if idx.strip()], "subtract", None)).pack()

tk.Button(frame, text="Multiply Signals", command=lambda: plot_signals(
    [int(idx) for idx in selected_indices_entry.get().split(",") if idx.strip()], "multiply", float(constant_entry.get()
                                                                                                    ))).pack()

tk.Button(frame, text="Square Signal", command=lambda: plot_signals(
    [int(idx) for idx in selected_indices_entry.get().split(",") if idx.strip()], "square", None)).pack()

tk.Button(frame, text="Shift Signal", command=lambda: plot_signals(
    [int(idx) for idx in selected_indices_entry.get().split(",") if idx.strip()], "shift", None)).pack()


tk.Button(frame, text="normalize 0->1", command=lambda: plot_signals(
    [int(idx) for idx in selected_indices_entry.get().split(",") if idx.strip()], "normalize1", None)).pack()

tk.Button(frame, text="normalize -1->1", command=lambda: plot_signals(
    [int(idx) for idx in selected_indices_entry.get().split(",") if idx.strip()], "normalize2", None)).pack()

tk.Button(frame, text="Accumulation of input signal ", command=lambda: plot_signals(
    [int(idx) for idx in selected_indices_entry.get().split(",") if idx.strip()], "accumulative", None)).pack()


tk.Label(frame, text="level").pack()
level = tk.Entry(frame)
level.pack()
level.insert(0, "0")

tk.Button(frame, text="Quantization ", command=lambda: plot_signals(
    [int(idx) for idx in selected_indices_entry.get().split(",") if idx.strip()], "Quantization", None)).pack()
options = ["levels", "bits"]
# datatype of menu text
clicked = tk.StringVar()
# initial menu text
clicked.set(" function ")
drop = tk.OptionMenu(frame, clicked, *options)
drop.pack()

toolbar = NavigationToolbar2Tk(canvas, frame, pack_toolbar=False)
toolbar.pack(anchor="s", fill=tk.X)

root.title('DSP Task3')
root.geometry('750x750')
root.resizable(True, True)
root.mainloop()