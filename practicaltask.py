import numpy as np
import task8
import matplotlib.pyplot as plt


################################################################
####################window######################################
################################################################


def rectangular(fs, tw):
    N = round((fs * 0.9) / tw)

    if N % 2 == 0:
        N += 1
    Wn = []
    lenth = (N - 1) / 2
    for n in range(int(lenth) + 1):
        Wn.append(1)

    return N, Wn


def hanning(fs, tw):
    N = round((fs * 3.1) / tw)

    if N % 2 == 0:
        N += 1
    Wn = []
    lenth = (N - 1) / 2
    for n in range(int(lenth) + 1):
        Wn.append(0.5 + 0.5 * np.cos((2 * np.pi * n) / N))

    return N, Wn


def hamming(fs, tw):
    N = round((fs * 3.3) / tw)

    if N % 2 == 0:
        N += 1
    Wn = []
    lenth = (N - 1) / 2
    for n in range(int(lenth) + 1):
        Wn.append(0.54 + 0.46 * np.cos((2 * np.pi * n) / N))

    return N, Wn


def blackman(fs, tw):
    N = round((fs * 5.5) / tw)

    if N % 2 == 0:
        N += 1
    Wn = []
    lenth = (N - 1) / 2
    for n in range(int(lenth) + 1):
        Wn.append(0.42 + 0.5 * np.cos(2 * np.pi * n / (N - 1)) + 0.08 * np.cos(4 * np.pi * n / (N - 1)))

    return N, Wn


#########################################################
############################filters######################
#########################################################


def LPF(fs, fc, tw, N):
    new_Fc = (fc + (0.5 * tw)) / fs
    Wc = 2 * np.pi * new_Fc

    Hn = []
    Hn.append(2 * new_Fc)

    for n in range(1, int(N / 2) + 1):
        Hn.append((2 * new_Fc * np.sin(n * Wc)) / (n * Wc))

    return Hn


def HPF(fs, fc, tw, N):
    new_Fc = (fc - (0.5 * tw)) / fs
    Wc = 2 * np.pi * new_Fc

    Hn = []
    Hn.append(1 - (2 * new_Fc))

    for n in range(1, int(N / 2) + 1):
        Hn.append((-2 * new_Fc * np.sin(n * Wc)) / (n * Wc))

    return Hn


def BPF(fs, fc1, fc2, tw, N):
    if fc1 > fc2:
        fc1, fc2 = fc2, fc1

    new_Fc1 = (fc1 - (0.5 * tw)) / fs
    new_Fc2 = (fc2 + (0.5 * tw)) / fs
    Wc1 = 2 * np.pi * new_Fc1
    Wc2 = 2 * np.pi * new_Fc2

    Hn = []
    Hn.append(2 * (new_Fc2 - new_Fc1))

    for n in range(1, int(N / 2) + 1):
        Hn.append(((2 * new_Fc2 * np.sin(n * Wc2)) / (n * Wc2)) + ((-2 * new_Fc1 * np.sin(n * Wc1)) / (n * Wc1)))

    return Hn


def BSF(fs, fc1, fc2, tw, N):
    if fc1 > fc2:
        fc1, fc2 = fc2, fc1

    new_Fc1 = (fc1 + (0.5 * tw)) / fs
    new_Fc2 = (fc2 - (0.5 * tw)) / fs
    Wc1 = 2 * np.pi * new_Fc1
    Wc2 = 2 * np.pi * new_Fc2

    Hn = []
    Hn.append(1 - (2 * (new_Fc2 - new_Fc1)))

    for n in range(1, int(N / 2) + 1):
        Hn.append(((2 * new_Fc1 * np.sin(n * Wc1)) / (n * Wc1)) + ((-2 * new_Fc2 * np.sin(n * Wc2)) / (n * Wc2)))

    return Hn


def save_list_to_txt(indx, values, txt):
    with open(txt, "w") as file:
        file.write(f"0\n")
        file.write(f"0\n")
        file.write(f"{len(indx)}\n")
        for i in range(len(indx)):
            file.write(f"{indx[i]} {values[i]}\n")


def calculate_res():
    N, win = blackman(1000, 50)

    fir = BSF(1000, 150, 250, 50, N)
    win = np.array(win)
    fir = np.array(fir)

    res = win * fir

    symmetric_res = np.concatenate((res[::-1], res[1:]))
    indix = []

    # for i in range(len(symmetric_res)):
    #     symmetric_res[i] = np.round(symmetric_res[i], 7)

    for i in range(-int(len(symmetric_res) / 2), int(len(symmetric_res) / 2) + 1):
        indix.append(i)

    # Create pairs of indices and rounded values
    # pairs = list(zip(indix, symmetric_res))
    #
    # # Print the pairs
    # for pair in pairs:
    #     print(pair)

    save_list_to_txt(indix, symmetric_res)
    return indix, symmetric_res


# calculate_res()
# indx, valu =task8.fast_convol("FIR test cases/Testcase 8/ecg400.txt",
#                               "output.txt")

# pairs = list(zip(indx, valu))

# # Print the pairs
# for pair in pairs:
#    print(pair)


# resampling
def upsample(signal, factor, original_indices):
    # sample
    upsampled_x = np.zeros(len(signal) * factor)
    upsampled_x[::factor] = signal
    # indecies
    upsampled_indices = np.zeros(len(signal) * factor)
    # print("original_indices",original_indices)
    for i in range(0, len(upsampled_x)):
        upsampled_indices[i] = i + int(original_indices[0])

    return upsampled_x, upsampled_indices  # x ={1,2,3} # x= {1,0,0,2,0,0,3,0,0}


def downsample(signal, factor, original_indices):
    signal = signal[::factor]
    # downsampled_indices =np.linspace(original_indices[0], original_indices[-1], len(signal))
    downsampled_indices = original_indices[::factor]
    return downsampled_indices, signal


def apply_lowpass_filter(signal, fs, stopband, cutoff_frequency, tw, signal_index):
    if stopband < 21:
        N, window = rectangular(fs, tw)
        fir = LPF(fs, cutoff_frequency, tw, N)
        window = np.array(window)
        fir = np.array(fir)
        res = window * fir
        symmetric_res = np.concatenate((res[::-1], res[1:]))
        indix = []
        for i in range(-int(len(symmetric_res) / 2), int(len(symmetric_res) / 2) + 1):
            indix.append(i)
        save_list_to_txt(indix, symmetric_res, "stopband.txt")
        indx, filtered_signal = task8.fast_convol(signal, "stopband.txt")

    elif 21 < stopband < 44:
        N, window = hanning(fs, tw)
        fir = LPF(fs, cutoff_frequency, tw, N)
        window = np.array(window)
        fir = np.array(fir)
        res = window * fir
        symmetric_res = np.concatenate((res[::-1], res[1:]))
        indix = []
        for i in range(-int(len(symmetric_res) / 2), int(len(symmetric_res) / 2) + 1):
            indix.append(i)
        save_list_to_txt(indix, symmetric_res, "hanning.txt")
        indx, filtered_signal = task8.fast_convol(signal, "hanning.txt", in1=signal_index)

    elif 44 < stopband < 53:
        N, window = hamming(fs, tw)
        fir = LPF(fs, cutoff_frequency, tw, N)
        window = np.array(window)
        fir = np.array(fir)
        res = window * fir
        symmetric_res = np.concatenate((res[::-1], res[1:]))
        indix = []
        for i in range(-int(len(symmetric_res) / 2), int(len(symmetric_res) / 2) + 1):
            indix.append(i)
        save_list_to_txt(indix, symmetric_res, "hamming.txt")
        indx, filtered_signal = task8.fast_convol(signal, "hamming.txt", in1=signal_index)
    else:
        N, window = blackman(fs, tw)
        fir = LPF(fs, cutoff_frequency, tw, N)
        window = np.array(window)
        fir = np.array(fir)
        res = window * fir
        symmetric_res = np.concatenate((res[::-1], res[1:]))
        indix = []
        for i in range(-int(len(symmetric_res) / 2), int(len(symmetric_res) / 2) + 1):
            indix.append(i)
        save_list_to_txt(indix, symmetric_res, "blackman.txt")
        indx, filtered_signal = task8.fast_convol(signal, "blackman.txt")

    return indx, filtered_signal


def resampling(signal, L, M, fs, stopband, cutoff_frequency, tw):
    with open(signal, "r") as file:
        inlines = file.readlines()
        ind1 = [float(line.split()[0]) for line in inlines[3:]]
        data1 = [float(line.split()[1]) for line in inlines[3:]]

    if L == 0 and M == 0:
        return "Error: Both L and M cannot be zero."

    elif M == 0 and L != 0:
        # Upsample by L
        upsampled_signal, ind = upsample(data1, L, ind1)
        print("ind1backfrom up sample", len(ind), ind)
        # Apply low-pass filter
        indx, filtered_signal = apply_lowpass_filter(upsampled_signal, fs, stopband, cutoff_frequency, tw, ind)
        plt.subplot(1, 2, 1)  # 1 row, 2 columns, plot 1
        plt.scatter(ind1, data1)
        plt.title('Plot 1')

        # Create the second plot
        plt.subplot(1, 2, 2)  # 1 row, 2 columns, plot 2
        plt.scatter(indx[:len(filtered_signal)], filtered_signal)
        plt.title('Plot 2')

        plt.tight_layout()
        plt.show()
    elif M != 0 and L == 0:
        # Apply low-pass filter
        indx, filtered_signal = apply_lowpass_filter(signal, fs, stopband, cutoff_frequency, tw, ind1)
        # Downsample by M
        indx, filtered_signal = downsample(filtered_signal, M, indx)
        # ind = ind1[::M]
        # Create the first plot
        plt.subplot(1, 2, 1)  # 1 row, 2 columns, plot 1
        plt.scatter(ind1, data1)
        plt.title('Plot 1')

        # Create the second plot
        plt.subplot(1, 2, 2)  # 1 row, 2 columns, plot 2
        plt.scatter(indx[:len(filtered_signal)], filtered_signal)
        plt.title('Plot 2')

    else:
        # Upsample by L, apply low-pass filter, and downsample by M
        upsampled_signal, ind = upsample(data1, L, ind1)
        ind, filtered_signal = apply_lowpass_filter(upsampled_signal, fs, stopband, cutoff_frequency, tw, ind1)

        indx, filtered_signal = downsample(filtered_signal, M, ind)
        plt.subplot(1, 2, 1)  # 1 row, 2 columns, plot 1
        plt.scatter(ind1, data1)
        plt.title('Plot 1')

        # Create the second plot
        plt.subplot(1, 2, 2)  # 1 row, 2 columns, plot 2
        plt.scatter(indx, filtered_signal[:len(indx)])
        plt.title('Plot 2')

        plt.tight_layout()
        plt.show()

    """print("indx",indx)
    print(len(indx))
    print("resambled",filtered_signal)
    print(len(filtered_signal))"""
    # Create the first plot

    return indx, filtered_signal

# Example usage:
# input_signal = np.random.rand(100)
# L_factor = 0
# M_factor = 2
# cutoff_frequency =1500

# output_signal = resampling("Sampling test cases/Testcase 1/ecg400.txt"
#                            , L_factor, M_factor,8000,50, 1500,500)
# print(output_signal)