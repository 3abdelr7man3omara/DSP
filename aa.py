import numpy as np
import matplotlib.pyplot as plt

# Read frequency components from a text file
def read_freq_components(file_path):
    freq_components = []
    with open(file_path, 'r') as file:
        lines = file.readlines()[4:]
        for line in lines:
            print("line", line)
            magnitude, phase_angle = line.strip().split(" ")
            magnitude = magnitude.replace("f", "")
            phase_angle = phase_angle.replace("f", "")

            magnitude = float(magnitude)
            phase_angle = float(phase_angle)
            freq_components.append((magnitude, phase_angle))
    return freq_components

# Reconstruct signal using IDFT
def reconstruct_signal(freq_components):
    num_samples = len(freq_components)
    dft_components = np.zeros(num_samples, dtype=complex)

    for k, (magnitude, phase_angle) in enumerate(freq_components):
        dft_components[k] = magnitude * np.exp(1j * phase_angle)

    # Compute the inverse DFT (IDFT)
    reconstructed_signal = np.fft.ifft(dft_components)

    return reconstructed_signal

# Example usage
file_path = 'DFT.txt'  # Path to the text file containing frequency components
freq_components = read_freq_components(file_path)

# Reconstruct the signal and plot it
reconstructed_signal = reconstruct_signal(freq_components)

# Plot the real part of the reconstructed signal
plt.plot(reconstructed_signal.real)
plt.xlabel('Time')
plt.ylabel('Signal Amplitude')
plt.title('Reconstructed Signal')
plt.show()

"""import math
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from QuanTest1 import QuantizationTest1
from QuanTest2 import QuantizationTest2


def load_file():
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text Files", "*.txt")])
    if file_path:
        x_values, y_values = [], []

        try:

            with open(file_path, 'r') as file:
                l_counter = 0
                for line in file:
                    if l_counter >= 3:
                        x, y = map(float, line.strip().split())
                        x_values.append(x)
                        y_values.append(y)
                    l_counter += 1
            # Plot the discrete points
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            plt.stem(x_values, y_values, 'ro')
            plt.title("Discrete Plot")
            plt.xlabel("X")
            plt.ylabel("Y")

            # Plot the continuous line
            plt.subplot(1, 2, 2)
            plt.plot(x_values, y_values, 'y')
            plt.title("Continuous Plot")
            plt.xlabel("X")
            plt.ylabel("Y")

            # Display the plot
            plt.show()

        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"Error reading file: {str(e)}")

def sinusoidal_signal():
    window = tk.Tk()
    window.title("Signal Generator")

    # Create a figure for the plot with three subplots
    fig, (ax1, ax3) = plt.subplots(1, 2, figsize=(15, 4))
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()

    # Frequency input
    frequency_label = tk.Label(window, text="Frequency (Hz):")
    frequency_label.pack()
    frequency_entry = tk.Entry(window)
    frequency_entry.pack()

    # Amplitude input
    amplitude_label = tk.Label(window, text="Amplitude:")
    amplitude_label.pack()
    amplitude_entry = tk.Entry(window)
    amplitude_entry.pack()

    # Phase shift input
    phase_shift_label = tk.Label(window, text="Phase Shift (radians):")
    phase_shift_label.pack()
    phase_shift_entry = tk.Entry(window)
    phase_shift_entry.pack()

    # Sampling frequency input
    sampling_frequency_label = tk.Label(window, text="Sampling Frequency (Hz):")
    sampling_frequency_label.pack()
    sampling_frequency_entry = tk.Entry(window)
    sampling_frequency_entry.pack()

    # Radio buttons for signal type
    signal_type = tk.StringVar()
    signal_type.set("Sine")
    sine_button = tk.Radiobutton(window, text="Sine", variable=signal_type, value="Sine")
    cosine_button = tk.Radiobutton(window, text="Cosine", variable=signal_type, value="Cosine")
    sine_button.pack()
    cosine_button.pack()



    def generate_signal():
        try:
            # Clear the previous plots
            ax1.clear()
            #ax2.clear()
            ax3.clear()

            # Get user input values
            frequency = float(frequency_entry.get())
            amplitude = float(amplitude_entry.get())
            phase_shift = float(phase_shift_entry.get())
            sampling_frequency = float(sampling_frequency_entry.get())

            # Check if the sampling frequency meets the Nyquist-Shannon condition
            if sampling_frequency < 2 * frequency:
                result_label.config(text="Sampling frequency should be at least twice the signal frequency.")
                return

            # Create a time array with respect to the sampling frequency
            time = np.arange(0, 1, 1 / sampling_frequency)

            if signal_type.get() == "Sine":
                # Calculate the sine wave signal
                signal = amplitude * np.sin(2 * np.pi * frequency * time + phase_shift)
                #cosine_signal = np.zeros_like(sine_signal)  # Generate a zero cosine signal
            else:
                #ax2.clear()
                # Calculate the cosine wave signal
                signal = amplitude * np.cos(2 * np.pi * frequency * time + phase_shift)
                #sine_signal = np.zeros_like(cosine_signal)  # Generate a zero sine signal

            # Plot the new signals
            ax1.plot(time, signal, label='Signal')
            ax1.set_xlabel('Time')
            ax1.set_ylabel('Amplitude')
            ax1.set_title('Sinusiodal Wave Signal')
            ax1.legend()
            ax1.grid(True)

            ax2.plot(time, cosine_signal, label='Cosine Signal', color='orange')
            ax2.set_xlabel('Time')
            ax2.set_ylabel('Amplitude')
            ax2.set_title('Cosine Wave Signal')
            ax2.legend()
            ax2.grid(True)

            sampling_period = 1 / sampling_frequency
            sampled_time = np.arange(0, 1, sampling_period)
            sampled_sine_signal = amplitude * np.sin(2 * np.pi * frequency * sampled_time + phase_shift)
            sampled_cosine_signal = amplitude * np.cos(2 * np.pi * frequency * sampled_time + phase_shift)

            # Plot the sampled signals
            ax3.stem(sampled_time, sampled_sine_signal, label='Sampled Sine Signal', basefmt=' ')
            ax3.stem(sampled_time, sampled_cosine_signal, markerfmt='ro', linefmt='r-', label='Sampled Cosine Signal',
                     basefmt=' ')
            ax3.set_xlabel('Sampled Time')
            ax3.set_ylabel('Amplitude')
            ax3.set_title('Sampled Signals')
            ax3.legend()
            ax3.grid(True)

            # Display the updated plots in the tkinter window
            canvas.draw()
            result_label.config(text="Signal generated and sampled successfully.")

        except ValueError:
                result_label.config(text="Invalid input. Please enter numeric values.")

    calculate_button = tk.Button(window, text="Calculate", command=generate_signal)
    calculate_button.pack()
    # Result label
    result_label = tk.Label(window, text="")
    result_label.pack()
    root.mainloop()

def Addition():
    # Select the first file
    file_path1 = filedialog.askopenfilename(title="Select the first file", filetypes=[("Text Files", "*.txt")])
    if not file_path1:
        return  # No file selected

    x_values1, y_values1 = [], []

    # Read the first file
    try:
        with open(file_path1, 'r') as file:
            l_counter = 0
            for line in file:
                if l_counter >= 3:  # Skip the first three lines if necessary
                    x, y = map(float, line.strip().split())
                    x_values1.append(x)
                    y_values1.append(y)
                l_counter += 1
    except Exception as e:
        print("Error reading the first file:", e)
        return

    # Select the second file
    file_path2 = filedialog.askopenfilename(title="Select the second file", filetypes=[("Text Files", "*.txt")])
    if not file_path2:
        return  # No file selected

    x_values2, y_values2 = [], []  # Initialize with empty lists

    # Read the second file
    try:
        with open(file_path2, 'r') as file:
            l_counter = 0
            for line in file:
                if l_counter >= 3:  # Skip the first three lines if necessary
                    x, y = map(float, line.strip().split())
                    x_values2.append(x)
                    y_values2.append(y)
                l_counter += 1
    except Exception as e:
        print("Error reading the second file:", e)
        return

    # Perform addition of y-values
    len1 = len(y_values1)
    len2 = len(y_values2)
    if len1 != len2:
        max_len = max(len1, len2)
        y_values1 += [0] * (max_len - len1)
        y_values2 += [0] * (max_len - len2)

    y_sum = np.add(y_values1, y_values2)
    print("Sum of Y-values:")
    for y in y_sum:
        print(y)
    # Plot the discrete points
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 3, 1)
    plt.plot(x_values1, y_values1, 'r')
    plt.title("signal1")
    plt.xlabel("X")
    plt.ylabel("Y")

    # Plot the continuous line
    plt.subplot(1, 3, 2)
    plt.plot(x_values2, y_values2, 'y')
    plt.title("signal2 ")
    plt.xlabel("X")
    plt.ylabel("Y")
    # Plot the continuous line
    plt.subplot(1, 3, 3)
    plt.plot(x_values1, y_sum, 'y')
    plt.title("signal Addition ")
    plt.xlabel("X")
    plt.ylabel("Y")

    # Display the plot
    plt.show()



def Subtraction():
    # Select the first file
    file_path1 = filedialog.askopenfilename(title="Select the first file", filetypes=[("Text Files", "*.txt")])
    if not file_path1:
        return  # No file selected

    x_values1, y_values1 = [], []

    # Read the first file
    try:
        with open(file_path1, 'r') as file:
            l_counter = 0
            for line in file:
                if l_counter >= 3:  # Skip the first three lines if necessary
                    x, y = map(float, line.strip().split())
                    x_values1.append(x)
                    y_values1.append(y)
                l_counter += 1
    except Exception as e:
        print("Error reading the first file:", e)
        return

    # Select the second file
    file_path2 = filedialog.askopenfilename(title="Select the second file", filetypes=[("Text Files", "*.txt")])
    if not file_path2:
        return  # No file selected

    x_values2, y_values2 = [], []  # Initialize with empty lists

    # Read the second file
    try:
        with open(file_path2, 'r') as file:
            l_counter = 0
            for line in file:
                if l_counter >= 3:  # Skip the first three lines if necessary
                    x, y = map(float, line.strip().split())
                    x_values2.append(x)
                    y_values2.append(y)
                l_counter += 1
    except Exception as e:
        print("Error reading the second file:", e)
        return

    # Perform addition of y-values
    len1 = len(y_values1)
    len2 = len(y_values2)
    if len1 != len2:
        max_len = max(len1, len2)
        y_values1 += [0] * (max_len - len1)
        y_values2 += [0] * (max_len - len2)

    y_sub = np.subtract(y_values1, y_values2)
    print("Sub of Y-values:")
    for y in y_sub:
        print(y)
    # Plot the discrete points
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 3, 1)
    plt.plot(x_values1, y_values1, 'r')
    plt.title("signal1")
    plt.xlabel("X")
    plt.ylabel("Y")

    # Plot the continuous line
    plt.subplot(1, 3, 2)
    plt.plot(x_values2, y_values2, 'y')
    plt.title("signal2 ")
    plt.xlabel("X")
    plt.ylabel("Y")
    # Plot the continuous line
    plt.subplot(1, 3, 3)
    plt.plot(x_values1, y_sub, 'y')
    plt.title("signal Subtraction ")
    plt.xlabel("X")
    plt.ylabel("Y")

    # Display the plot
    plt.show()

def multiplication():

    file_path1 = filedialog.askopenfilename(title="Select the first file", filetypes=[("Text Files", "*.txt")])
    file = open(file_path1, 'r')
    lines = file.readlines()
    signal = lines[3:]
    x, y, multiplication = [], [], []
    for l in signal:
        row = l.split()
        x.append(float(row[0]))
        y.append(float(row[1]))
    file.close()
    A = float(input("Enter value to amplify or reduce the signal amplitude"))
    for i in range(len(y)):
        multiplication.append(y[i] * A)

    # Create a figure and subplots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(7, 3))

    # Plot the first subplot
    axes[0].plot(x, y)
    axes[0].set_title('Signal 1')

    # Plot the second subplot
    axes[1].plot(x, multiplication)
    axes[1].set_title('multiplication')

    # Adjust the spacing between subplots
    fig.tight_layout()

    # Display the figure
    plt.show()

def squaring():
    file_path1 = filedialog.askopenfilename(title="Select the first file", filetypes=[("Text Files", "*.txt")])
    file = open(file_path1, 'r')
    lines1 = file.readlines()
    signal = lines1[3:]
    x, y, squaring = [], [], []
    for l in signal:
        row = l.split()
        x.append(float(row[0]))
        y.append(float(row[1]))
    file.close()
    for i in range(len(y)):
        squaring.append(y[i] * y[i])

    # Create a figure and subplots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(7, 3))

    # Plot the first subplot
    axes[0].plot(x, y)
    axes[0].set_title('Signal 1')

    # Plot the second subplot
    axes[1].plot(x, squaring)
    axes[1].set_title('squaring')

    # Adjust the spacing between subplots
    fig.tight_layout()

    # Display the figure
    plt.show()

def shifting():
    file_path1 = filedialog.askopenfilename(title="Select the file", filetypes=[("Text Files", "*.txt")])
    if not file_path1:
        return

    x_values1, y_values1 = [], []

    try:
        with open(file_path1, 'r') as file:
            l_counter = 0
            for line in file:
                if l_counter >= 3:
                    x, y = map(float, line.strip().split())
                    x_values1.append(x)
                    y_values1.append(y)
                l_counter += 1
    except Exception as e:
        print("Error reading the file:", e)
        return

    constant = float(constant_entry.get())

    shifted_x = []
    for i in x_values1:
        shifted_x.append(i - constant)
    print("Shifted x-values:")
    for x in shifted_x:
        print(x)

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(x_values1, y_values1, 'r')
    plt.title("Original Signal")
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.subplot(1, 2, 2)
    plt.plot(shifted_x, y_values1, 'g')
    plt.title("Shifted Signal")
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.show()


def normalize():
    file_path1 = filedialog.askopenfilename(title="Select the file", filetypes=[("Text Files", "*.txt")])
    if not file_path1:
        return

    x_values1, y_values1 = [], []

    try:
        with open(file_path1, 'r') as file:
            l_counter = 0
            for line in file:
                if l_counter >= 3:
                    x, y = map(float, line.strip().split())
                    x_values1.append(x)
                    y_values1.append(y)
                l_counter += 1
    except Exception as e:
        print("Error reading the file:", e)
        return

    y_values1 = np.array(y_values1)  # Convert to NumPy array
    mx = np.max(y_values1)
    mn = np.min(y_values1)
    b = int(upper_entry.get())
    a = int(Lower_entry.get())
    Y_normalized = ((y_values1 - mn) / (mx - mn)) * (b - a) + a
    print("normalized  y-values:")
    for y in Y_normalized:
        print(y)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(x_values1, y_values1, 'r')
    plt.title("Original Signal")
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.subplot(1, 2, 2)
    plt.plot(x_values1, Y_normalized, 'g')
    plt.title("Normalized Signal")
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.show()

def Accumulation():
    file_path1 = filedialog.askopenfilename(title="Select the file", filetypes=[("Text Files", "*.txt")])
    if not file_path1:
        return

    x_values1, y_values1 = [], []

    try:
        with open(file_path1, 'r') as file:
            l_counter = 0
            for line in file:
                if l_counter >= 3:
                    x, y = map(float, line.strip().split())
                    x_values1.append(x)
                    y_values1.append(y)
                l_counter += 1
    except Exception as e:
        print("Error reading the file:", e)
        return
    y_accum = []
    c=0
    for y in y_values1:
        c=c+y
        y_accum.append(c)

    for y in y_accum:
        print(y)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(x_values1, y_values1, 'r')
    plt.title("Original Signal")
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.subplot(1, 2, 2)
    plt.plot(x_values1, y_accum, 'g')
    plt.title(" Accumulative  Signal")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

def uploadtxt():
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        return file_path
def quantize():


    def handle_input(choice_var, bits_entry, levels_label, levels_entry, bits_label, encoding_label,
                         quantization_label,
                         root):
            signal_file = uploadtxt()
            with open(signal_file, "r", encoding='utf-8') as file:
                lines = file.readlines()

            ignored_lines = lines[3:]
            y, temp = [], []

            for l in ignored_lines:
                row = l.split()
                temp.append(float(row[1]))

            for i in range(len(temp)):
                y.append(float(format(temp[i], ".2f")))

            choice = choice_var.get()

            k = bits_entry

            if choice == '0':
                #bits = eval(bits_entry.get())
                #bits_entry = float (bits_entry)
                k =( bits_entry)
                max_bits = bits_entry
                bits_entry = int(math.pow(2, k))
                print("l", l)
                levels_label.config(text="Levels = {}".format(bits_entry))
            elif choice == '1':
                #levels = eval(levels_entry.get())
                k = math.log2(levels_entry)
                print(type(levels_entry))
                bits_entry = (levels_entry)
                bits_label.config(text="Bits = {}".format(levels_entry))
                max_bits = math.floor(math.log2(k)) + 1

            minimum = float('inf')
            maximum = float('-inf')

            for i in range(len(y)):
                if y[i] < minimum:
                    minimum = y[i]
                elif y[i] > maximum:
                    maximum = y[i]

            print("l" , l)
            print("bits", type(bits_entry))
            print("bits", (bits_entry))
            print("l", type(l))
            print("min", type(minimum))
            print("max", type(maximum))
            delta = (maximum - minimum) / bits_entry

            ranges, midpoints = [], []
            for i in range(int(bits_entry)):
                range_min = minimum + i * delta
                range_max = range_min + delta
                midpoint = (range_min + range_max) / 2
                ranges.append((format(range_min, ".2f"), format(range_max, ".2f")))
                midpoints.append(format(midpoint, ".2f"))

            interval_indices = []
            for i in range(len(y)):
                for j in range(len(ranges)):
                    if float(ranges[j][0]) <= y[i] <= float(ranges[j][1]):
                        interval_indices.append(j + 1)
                        break

            print("ranges" , ranges)


            q = []
            for i in range(len(y)):
                q.append(float(midpoints[int(interval_indices[i]) - 1]))

            encoding = []

            print("max_bits" , max_bits)
            for i in range(len(y)):
                encoding.append(bin(interval_indices[i] - 1)[2:].zfill(int(max_bits))[-max_bits:])
                #format(int_value, '0{}b'.format(max_bits))

            print("encoding" , encoding)

            error = []
            for i in range(len(y)):
                error.append(q[i] - y[i])

            encoding_label.config(text="Encoding: {}".format(encoding))
            quantization_label.config(text="Quantization: {}".format(q))

            print("interval_indices", interval_indices)
            if choice == '0':
                # Capture the output of QuantizationTest1
                output_text = QuantizationTest1("Quan1_Out.txt", encoding, q)
            else :
                output_text = QuantizationTest2("Quan2_Out.txt",interval_indices, encoding, q ,error)

            # Display the output text in a tkinter label
            output_label = tk.Label(root, text="Output: {}".format(output_text))
            output_label.pack()

    def Task3_test1_window():

                #root2 = tk.Tk()
                root2 = tk.Toplevel(root)
                root2.title("Quantization GUI")
                choice_label = tk.Label(root2, text="Choose an option:")
                choice_label.pack()

                choice_var = tk.StringVar()
                bits_radio = tk.Radiobutton(root2, text="Number of Bits", variable=choice_var, value='0')
                bits_radio.pack()

                levels_radio = tk.Radiobutton(root2, text="Number of Levels", variable=choice_var, value='1')
                levels_radio.pack()

                bits_entry = tk.Entry(root2)
                bits_entry.pack()
                bits_entry.insert(0, "0")

                levels_entry = tk.Entry(root2)
                levels_entry.pack()
                levels_entry.insert(0, "0")

                submit_button = tk.Button(root2, text="Submit",
                                          command=lambda: handle_input(choice_var, eval(bits_entry.get()) , levels_label,
                                                                      eval (levels_entry.get()),
                                                                       bits_label, encoding_label, quantization_label,
                                                                       root))
                submit_button.pack()

                levels_label = tk.Label(root2, text="Levels =")
                levels_label.pack()

                bits_label = tk.Label(root2, text="Bits =")
                bits_label.pack()

                encoding_label = tk.Label(root2, text="Encoding:")
                encoding_label.pack()

                quantization_label = tk.Label(root2, text="Quantization:")
                quantization_label.pack()
                root2.mainloop()
    Task3_test1_window()










root = tk.Tk()
root.geometry("900x700")
root.title("My First GUI")
load_button = tk.Button(root, text="Load File",font=('Arial',16), command=load_file)
load_button.pack()
load_button = tk.Button(root, text="sinusiodal_signal",font=('Arial',16), command=sinusoidal_signal)
load_button.pack()
add_button = tk.Button(root, text="Addition",font=('Arial',16) ,command=Addition)
add_button.pack()
add_button = tk.Button(root, text="ٍSubtraction",font=('Arial',16), command=Subtraction)
add_button.pack()
add_button = tk.Button(root, text="multiplication",font=('Arial',16), command=multiplication)
add_button.pack()

add_button = tk.Button(root, text="squaring",font=('Arial',16), command=squaring)
add_button.pack()
shift_button = tk.Button(root, text="Shift",font=('Arial',16), command=shifting)
shift_button.pack()

constant_label = tk.Label(root, text="Constant:")
constant_label.pack()
constant_entry = tk.Entry(root)
constant_entry.pack()

normalize_button = tk.Button(root, text="normalize",font=('Arial',16), command=normalize)
normalize_button.pack()

upper_entry = tk.Label(root, text=" upper : ")
upper_entry.pack()
upper_entry = tk.Entry(root)
upper_entry.pack()
Lower_entry = tk.Label(root, text=" lower : ")
Lower_entry.pack()
Lower_entry = tk.Entry(root)
Lower_entry.pack()
comulative_button = tk.Button(root, text="accumulative",font=('Arial',16), command=Accumulation)
comulative_button.pack()

quantize_button = tk.Button(root, text="Quantization",font=('Arial',16), command=quantize)
quantize_button.pack()
root.mainloop()


#new

# import libraries
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create the tkinter window
window = tk.Tk()
window.title("Signal Generator")

# Create a figure for the plot with three subplots
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack()


def calculate_and_plot_signal():
    try:
        # Clear the previous plots
        ax1.clear()
        ax2.clear()
        ax3.clear()

        # Get user input values
        frequency = float(frequency_entry.get())
        amplitude = float(amplitude_entry.get())
        phase_shift = float(phase_shift_entry.get())
        sampling_frequency = float(sampling_frequency_entry.get())

        # Check if the sampling frequency meets the Nyquist-Shannon condition
        if sampling_frequency < 2 * frequency:
            result_label.config(text="Sampling frequency should be at least twice the signal frequency.")
            return

        # Create a time array with respect to the sampling frequency
        time = np.arange(0, 1, 1 / sampling_frequency)

        if signal_type.get() == "Sine":
            # Calculate the sine wave signal
            sine_signal = amplitude * np.sin(2 * np.pi * frequency * time + phase_shift)
            cosine_signal = np.zeros_like(sine_signal)  # Generate a zero cosine signal
        else:
            # Calculate the cosine wave signal
            cosine_signal = amplitude * np.cos(2 * np.pi * frequency * time + phase_shift)
            sine_signal = np.zeros_like(cosine_signal)  # Generate a zero sine signal

        # Plot the new signals
        ax1.plot(time, sine_signal, label='Sine Signal')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Amplitude')
        ax1.set_title('Sine Wave Signal')
        ax1.legend()
        ax1.grid(True)

        ax2.plot(time, cosine_signal, label='Cosine Signal', color='orange')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Amplitude')
        ax2.set_title('Cosine Wave Signal')
        ax2.legend()
        ax2.grid(True)

        # Sample the signal
        sampling_period = 1 / sampling_frequency
        sampled_time = np.arange(0, 1, sampling_period)
        sampled_sine_signal = amplitude * np.sin(2 * np.pi * frequency * sampled_time + phase_shift)
        sampled_cosine_signal = amplitude * np.cos(2 * np.pi * frequency * sampled_time + phase_shift)

        # Plot the sampled signals
        ax3.stem(sampled_time, sampled_sine_signal, label='Sampled Sine Signal', basefmt=' ')
        ax3.stem(sampled_time, sampled_cosine_signal, markerfmt='ro', linefmt='r-', label='Sampled Cosine Signal',
                 basefmt=' ')
        ax3.set_xlabel('Sampled Time')
        ax3.set_ylabel('Amplitude')
        ax3.set_title('Sampled Signals')
        ax3.legend()
        ax3.grid(True)

        # Display the updated plots in the tkinter window
        canvas.draw()
        result_label.config(text="Signal generated and sampled successfully.")

    except ValueError:
        result_label.config(text="Invalid input. Please enter numeric values.")


# Frequency input
frequency_label = tk.Label(window, text="Frequency (Hz):")
frequency_label.pack()
frequency_entry = tk.Entry(window)
frequency_entry.pack()

# Amplitude input
amplitude_label = tk.Label(window, text="Amplitude:")
amplitude_label.pack()
amplitude_entry = tk.Entry(window)
amplitude_entry.pack()

# Phase shift input
phase_shift_label = tk.Label(window, text="Phase Shift (radians):")
phase_shift_label.pack()
phase_shift_entry = tk.Entry(window)
phase_shift_entry.pack()

# Sampling frequency input
sampling_frequency_label = tk.Label(window, text="Sampling Frequency (Hz):")
sampling_frequency_label.pack()
sampling_frequency_entry = tk.Entry(window)
sampling_frequency_entry.pack()

# Radio buttons for signal type
signal_type = tk.StringVar()
signal_type.set("Sine")
sine_button = tk.Radiobutton(window, text="Sine", variable=signal_type, value="Sine")
cosine_button = tk.Radiobutton(window, text="Cosine", variable=signal_type, value="Cosine")
sine_button.pack()
cosine_button.pack()

# Calculate button
calculate_button = tk.Button(window, text="Calculate", command=calculate_and_plot_signal)
calculate_button.pack()

# Result label
result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()"""