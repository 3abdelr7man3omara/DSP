import tkinter as tk
import numpy as np
import task4 as dft
import csv
import Shift_Fold_Signal
import comparesignal2
import matplotlib.pyplot as plt
import task62
import ConvTest
import DerivativeSignal
"""
file_paths = [
    "input_fold.txt",
    "Output_fold.txt",
    "Output_ShifFoldedby500.txt",
    "Output_ShiftFoldedby-500.txt",
    "DC_component_input.txt",
    "DC_component_output.txt",
]

class MyGUI:
    def __init__(self, master):
        self.master = master
        # Entries
        self.label_filechoose = tk.Label(master, text="Enter filechoose index:")
        self.label_filechoose.grid(row=0, column=0, padx=10, pady=10)
        self.entry_filechoose = tk.Entry(master)
        self.entry_filechoose.grid(row=0, column=1, padx=10, pady=10)

        self.label_k = tk.Label(master, text="Enter k(advance or delay):")
        self.label_k.grid(row=1, column=0, padx=10, pady=10)
        self.entry_k = tk.Entry(master)
        self.entry_k.grid(row=1, column=1, padx=10, pady=10)

        self.label_f = tk.Label(master, text="Fold or No Fold (1:0):")
        self.label_f.grid(row=2, column=0, padx=10, pady=10)
        self.entry_f = tk.Entry(master)
        self.entry_f.grid(row=2, column=1, padx=10, pady=10)

        self.submit_button = tk.Button(master, text="Submit", command=self.process_data)
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=20)

        # # Entry for sampling frequency
        # self.label_sampling_freq = tk.Label(master, text="Enter sampling frequency:")
        # self.label_sampling_freq.grid(row=3, column=0, padx=10, pady=10)
        # self.entry_sampling_freq = tk.Entry(master)
        # self.entry_sampling_freq.grid(row=3, column=1, padx=10, pady=10)


    def prepare_data(self, file_path):
        with open(file_path, 'r') as f:
            csv_f = csv.reader(f)
            x_data = []
            y_data = []

            for row in csv_f:
                try:
                    x_value = int(row[0].split()[0])
                    y_value = int(row[0].split()[1])
                    x_data.append(x_value)
                    y_data.append(y_value)
                except (ValueError, IndexError):
                    pass

        return x_data, y_data

    def folding(self, k, f, file_index):
        x, y = self.prepare_data(file_paths[file_index])
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
        # Top subplot
        ax1.plot(x, y)
        ax1.set_xlim([-600, 600])
        ax1.grid(True)
        ax1.set_title('BEFORE')
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')

        data = list(zip(x, y))
        if f:
            data_copy = data[:]
            for i in range(len(data_copy)):
                temp_x, temp_y = data_copy[i][0], data_copy[i][1]
                temp_x = int(temp_x * -1)
                data.pop(i)
                data.insert(i, (temp_x, temp_y))

            if k != 0:
                data_copy = data[:]
                for i in range(len(data_copy)):
                    temp_x, temp_y = data_copy[i][0], data_copy[i][1]
                    temp_x = int(temp_x + k)
                    data.pop(i)
                    data.insert(i, (temp_x, temp_y))
        else:
            data_copy = data[:]
            for i in range(len(data_copy)):
                temp_x, temp_y = data_copy[i][0], data_copy[i][1]
                temp_x = int(temp_x - k)
                data.pop(i)
                data.insert(i, (temp_x, temp_y))
        x = []
        y = []
        for t in range(len(data)):
            x.append(data[t][0])
            y.append(data[t][1])
            # Bottom subplot
        ax2.plot(x, y, 'red')
        ax2.grid(True)
        ax2.set_title('AFTER')
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')

        # Adjust spacing between subplots
        plt.tight_layout()

        # Show the plot
        plt.show()

        return data

    def dc_com(self, path_file):
        with open(path_file, "r") as file:
            in_lines = file.readlines()
            data = [float(line.split()[1]) for line in in_lines[3:]]
            sampling_frequency = 4 #float(self.entry_sampling_freq.get())
            fourier_coeffs, frequencies = dft.dft(data, fs=sampling_frequency)
            amplitudes = np.abs(fourier_coeffs)
            phases = np.angle(fourier_coeffs)
            amplitudes[0] = 0
            phases[0] = 0

            N = len(data)
            reconstructed_signal = np.zeros(N, dtype=complex)

            for i in range(N):
                real_part = (amplitudes[i] * np.cos(phases[i]))
                imaginary_part = amplitudes[i] * np.sin(phases[i])
                reconstructed_signal[i] = complex(real_part, imaginary_part)

            reconstructed_signal = dft.idft(reconstructed_signal).real
        return reconstructed_signal

    def process_data(self):
        filechoose = int(self.entry_filechoose.get())
        k = int(self.entry_k.get())
        f = int(self.entry_f.get())
        sampling_freq = 4#float(self.entry_sampling_freq.get())

        # Call your existing functions with the entered values
        if filechoose == 0:
            #while True:
                new_data = self.folding(k, f, filechoose)
                new_data = sorted(new_data)

                # with open("newdata.txt", "w") as file:
                #     file.write("indix, value\n")
                #     file.write(f"0\n")
                #     file.write(f"0\n")
                #     file.write(f"{len(new_data)}\n")
                #     for i in range(len(new_data)):
                #         file.write(f" {new_data[i]}\n")
                indixs = []
                values = []
                for i in range(len(new_data)):
                    indixs.append(new_data[i][0])
                    values.append(new_data[i][1])

                if k == 0:
                    Shift_Fold_Signal.Shift_Fold_Signal(file_paths[1], indixs, values)
                elif k > 0:
                    Shift_Fold_Signal.Shift_Fold_Signal(file_paths[2], indixs, values)
                elif k < 0:
                    Shift_Fold_Signal.Shift_Fold_Signal(file_paths[3], indixs, values)
        elif filechoose == 4:
            dc_data = self.dc_com(file_paths[filechoose])
            print(dc_data)
            comparesignal2.SignalSamplesAreEqual(file_paths[5], dc_data)

root = tk.Tk()
my_gui = MyGUI(root)
root.mainloop()"""


#############
import tkinter as tk
import numpy as np
import task4 as dft
import csv
import Shift_Fold_Signal
import comparesignal2
import matplotlib.pyplot as plt


file_paths = [
    "input_fold.txt",
    "Output_fold.txt",
    "Output_ShifFoldedby500.txt",
    "Output_ShiftFoldedby-500.txt",
    "DC_component_input.txt",
    "DC_component_output.txt",
]

class MyGUI:
    def __init__(self, master):
        self.master = master
        # Entries
        self.label_filechoose = tk.Label(master, text="Enter filechoose index:")
        self.label_filechoose.grid(row=0, column=0, padx=10, pady=10)
        self.entry_filechoose = tk.Entry(master)
        self.entry_filechoose.grid(row=0, column=1, padx=10, pady=10)

        self.label_k = tk.Label(master, text="Enter k(advance or delay):")
        self.label_k.grid(row=1, column=0, padx=10, pady=10)
        self.entry_k = tk.Entry(master)
        self.entry_k.grid(row=1, column=1, padx=10, pady=10)

        self.label_f = tk.Label(master, text="Fold or No Fold (1:0):")
        self.label_f.grid(row=2, column=0, padx=10, pady=10)
        self.entry_f = tk.Entry(master)
        self.entry_f.grid(row=2, column=1, padx=10, pady=10)

        self.submit_button = tk.Button(master, text="Submit", command=self.process_data)
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=20)

        # # Entry for sampling frequency
        # self.label_sampling_freq = tk.Label(master, text="Enter sampling frequency:")
        # self.label_sampling_freq.grid(row=3, column=0, padx=10, pady=10)
        # self.entry_sampling_freq = tk.Entry(master)
        # self.entry_sampling_freq.grid(row=3, column=1, padx=10, pady=10)


    def prepare_data(self, file_path):
        with open(file_path, 'r') as f:
            csv_f = csv.reader(f)
            x_data = []
            y_data = []

            for row in csv_f:
                try:
                    x_value = int(row[0].split()[0])
                    y_value = int(row[0].split()[1])
                    x_data.append(x_value)
                    y_data.append(y_value)
                except (ValueError, IndexError):
                    pass

        return x_data, y_data

    def folding(self, k, f, file_index):
        x, y = self.prepare_data(file_paths[file_index])
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
        # Top subplot
        ax1.plot(x, y)
        ax1.set_xlim([-600, 600])
        ax1.grid(True)
        ax1.set_title('BEFORE')
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')

        data = list(zip(x, y))
        if f:
            data_copy = data[:]
            for i in range(len(data_copy)):
                temp_x, temp_y = data_copy[i][0], data_copy[i][1]
                temp_x = int(temp_x * -1)
                data.pop(i)
                data.insert(i, (temp_x, temp_y))

            if k != 0:
                data_copy = data[:]
                for i in range(len(data_copy)):
                    temp_x, temp_y = data_copy[i][0], data_copy[i][1]
                    temp_x = int(temp_x + k)
                    data.pop(i)
                    data.insert(i, (temp_x, temp_y))
        else:
            data_copy = data[:]
            for i in range(len(data_copy)):
                temp_x, temp_y = data_copy[i][0], data_copy[i][1]
                temp_x = int(temp_x - k)
                data.pop(i)
                data.insert(i, (temp_x, temp_y))
        x = []
        y = []
        for t in range(len(data)):
            x.append(data[t][0])
            y.append(data[t][1])
            # Bottom subplot
        ax2.plot(x, y, 'red')
        ax2.grid(True)
        ax2.set_title('AFTER')
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')

        # Adjust spacing between subplots
        plt.tight_layout()

        # Show the plot
        plt.show()

        return data

    def dc_com(self, path_file):
        with open(path_file, "r") as file:
            in_lines = file.readlines()
            data = [float(line.split()[1]) for line in in_lines[3:]]
            sampling_frequency = 4 #float(self.entry_sampling_freq.get())
            fourier_coeffs, frequencies = dft.dft(data, d= sampling_frequency)
            amplitudes = np.abs(fourier_coeffs)
            phases = np.angle(fourier_coeffs)
            amplitudes[0] = 0
            phases[0] = 0

            N = len(data)
            reconstructed_signal = np.zeros(N, dtype=complex)

            for i in range(N):
                real_part = (amplitudes[i] * np.cos(phases[i]))
                imaginary_part = amplitudes[i] * np.sin(phases[i])
                reconstructed_signal[i] = complex(real_part, imaginary_part)

            reconstructed_signal = dft.idft(reconstructed_signal).real
        return reconstructed_signal

    def process_data(self):
        filechoose = int(self.entry_filechoose.get())
        k = int(self.entry_k.get())
        f = int(self.entry_f.get())
        sampling_freq = 4#float(self.entry_sampling_freq.get())

        # Call your existing functions with the entered values
        if filechoose == 0:
            #while True:
                new_data = self.folding(k, f, filechoose)
                new_data = sorted(new_data)

                # with open("newdata.txt", "w") as file:
                #     file.write("indix, value\n")
                #     file.write(f"0\n")
                #     file.write(f"0\n")
                #     file.write(f"{len(new_data)}\n")
                #     for i in range(len(new_data)):
                #         file.write(f" {new_data[i]}\n")
                indixs = []
                values = []
                for i in range(len(new_data)):
                    indixs.append(new_data[i][0])
                    values.append(new_data[i][1])

                if k == 0:
                    Shift_Fold_Signal.Shift_Fold_Signal(file_paths[1], indixs, values)
                elif k > 0:
                    Shift_Fold_Signal.Shift_Fold_Signal(file_paths[2], indixs, values)
                elif k < 0:
                    Shift_Fold_Signal.Shift_Fold_Signal(file_paths[3], indixs, values)
        elif filechoose == 4:
            dc_data = self.dc_com(file_paths[filechoose])
            print(dc_data)
            comparesignal2.SignalSamplesAreEqual(file_paths[5], dc_data)

root = tk.Tk()
my_gui = MyGUI(root)
root.mainloop()