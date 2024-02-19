"""import task4
import task4 as dft
import numpy as np
import csv


def fast_convol(pathfile1, pathfile2):
    with open(pathfile1, "r") as file:
        inlines = file.readlines()
        data1 = [float(line.split()[1]) for line in inlines[3:]]
        fourier_coeffs1, frequencies1 = dft.dft(data1, d=0)

    with open(pathfile2, "r") as file:
        inlines = file.readlines()
        data2 = [float(line.split()[1]) for line in inlines[3:]]
        fourier_coeffs2, frequencies2 = dft.dft(data2, d=0)

    multiply_res = [fc1 * fc2 for fc1, fc2 in zip(fourier_coeffs1, fourier_coeffs2)]

    amplitudes_res = np.abs(multiply_res)
    phases_res = np.angle(multiply_res)

    N = len(data1)
    reconstructed_signal = np.zeros(N, dtype=complex)

    for i in range(N):
        real_part = amplitudes_res[i] * np.cos(phases_res[i])
        imaginary_part = amplitudes_res[i] * np.sin(phases_res[i])
        reconstructed_signal[i] = complex(real_part, imaginary_part)

    reconstructed_signal = dft.idft(reconstructed_signal).real
    return reconstructed_signal

def prepare_data(file_path):
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
def fast_correlation(path1, path2):
    with open(path1, "r") as file:
        inlines = file.readlines()
        data1 = [float(line.split()[1]) for line in inlines[3:]]
        fourier_coeffs1, frequencies1 = dft.dft(data1, d=0)

    with open(path2, "r") as file:
        inlines = file.readlines()
        data2 = [float(line.split()[1]) for line in inlines[3:]]
        fourier_coeffs2, frequencies2 = dft.dft(data2, d=0)

    #for i in range(len(fourier_coeffs1)):
     #   if fourier_coeffs1[i].imag:
      #      fourier_coeffs1[i] = complex(fourier_coeffs1[i].real, -fourier_coeffs1[i].imag)

    res = [fc1 * np.conj(fc1) for fc1 in fourier_coeffs1]
    N = len(res)
    idf = np.fft.ifft(res)
    # Normalize the PSD
    for i in range(N):
        idf[i] = idf[i] * (1 / N)

    return np.real(idf)


def main():
    conv = fast_convol("Input_conv_Sig1.txt",
                       "Input_conv_Sig2.txt")
    print(conv)
    corr = fast_correlation("Point1 Correlation/Corr_input signal1.txt","Point1 Correlation/Corr_input signal2.txt")
    print(corr)

if __name__ == "__main__":
    main()"""
import task4 as dft
import numpy as np
import ConvTest
import CompareSignal as corr_com
def read_out_file (path):
    index = []
    data2= []
    with open(path, "r") as file:
        inlines = file.readlines()
        print ("inlines", inlines)
        data = inlines[0].split('/')
        print ("data", data)

    for i in range(3, len(data)-1):
            data[i] = data[i].replace("n","")
            print("data[i]", data[i])

            index.append(eval(data[i].split()[0]))
            data2.append(eval(data[i].split()[1]))

            #data[i] = eval(data[i])
    print("data2", data2)
    print("index", index)

    return index , data2


def fast_convol(pathfile1, pathfile2, in1=[], in2=[]):
    if isinstance(pathfile1, str) :
        with open(pathfile1, "r") as file:
            inlines = file.readlines()
            # print("inlines----",inlines)
            ind1 = [float(line.split(" ")[0]) for line in inlines[3:]]
            try:
                data1 = [float(line.split(" ")[1]) for line in inlines[3:]]
            except:
                pass

    else:
        # Assuming the input is a NumPy array
        # Save the array to a text file
        data1 = pathfile1
        ind1 = in1


    if isinstance(pathfile2, str) :
        with open(pathfile2, "r") as file:
            inlines = file.readlines()
            ind2 = [float(line.split(" ")[0]) for line in inlines[3:]]
            data2 = [float(line.split(" ")[1]) for line in inlines[3:]]
        #print("data2", data2)
        if len(data2) == 0:
            ind2, data2 = read_out_file(pathfile2)
        #print("data2", data2)
    else:
        # Assuming the input is a NumPy array
        # Save the array to a text file
        data2 = pathfile2
        ind2 = in2



    if len(data1) != len(data2):
        max_len = len(data2) + len(data1) - 1
        # pad_width1 = (max(0, len(data2) - len(data1)), 0)
        # pad_width2 = (max(0, len(data1) - len(data2)), 0)
        padded_data1 = np.pad(data1, (0, len(data2) - 1), mode='constant')
        padded_data2 = np.pad(data2, (0, len(data1) - 1), mode='constant')
    else:
        padded_data1 = data1
        padded_data2 = data2
    fourier_coeffs1, frequencies1 = dft.dft(padded_data1, d=0)
    fourier_coeffs2, frequencies2 = dft.dft(padded_data2, d=0)
    print(len(padded_data1), len(fourier_coeffs1))
    print(len(padded_data2), len(frequencies2))

    multiply_res = fourier_coeffs1 * fourier_coeffs2 #[fc1 * fc2 for fc1, fc2 in zip(fourier_coeffs1, fourier_coeffs2)]

    amplitudes_res = np.abs(multiply_res)
    phases_res = np.angle(multiply_res)

    N = len(padded_data1)
    reconstructed_signal = np.zeros(N, dtype=complex)

    for i in range(N):
        real_part = amplitudes_res[i] * np.cos(phases_res[i])
        imaginary_part = amplitudes_res[i] * np.sin(phases_res[i])
        reconstructed_signal[i] = complex(real_part, imaginary_part)

    reconstructed_signal = dft.idft(reconstructed_signal).real
    # for k in range(len(reconstructed_signal)) :
    #     reconstructed_signal[k]=round(reconstructed_signal[k])
    # print (ind2)
    print("Length of ind1:", len(ind1))
    print("Length of ind2:", len(ind2))


    res_ind = np.arange(ind1[0] + ind2[0], ind1[-1] + ind2[-1] + 1)
    print("resind",res_ind)
    print("reconstructed_signal",len(reconstructed_signal),reconstructed_signal)
    return res_ind, reconstructed_signal


def fast_correlation(path1, path2):
    with open(path1, "r") as file:
        inlines = file.readlines()
        data1 = [float(line.split()[1]) for line in inlines[3:]]
        fourier_coeffs1, frequencies1 = dft.dft(data1, d=0)

    with open(path2, "r") as file:
        inlines = file.readlines()
        data2 = [float(line.split()[1]) for line in inlines[3:]]
        fourier_coeffs2, frequencies2 = dft.dft(data2, d=0)

    for i in range(len(fourier_coeffs1)):
        if fourier_coeffs1[i].imag:
            fourier_coeffs1[i] = complex(fourier_coeffs1[i].real, -fourier_coeffs1[i].imag)


    new_res= fourier_coeffs1 * fourier_coeffs2
    N = len(new_res)
    idf = np.fft.ifft(new_res)
    idf.real/= N
    indx=[]
    for i in range(len(idf)):
        indx.append(i)
    return indx,np.real(idf)


def main():
    conv_ind,conv = fast_convol("Input_conv_Sig1.txt",
                                "Input_conv_Sig2.txt")
    print(conv)
    ConvTest.ConvTest(conv_ind,conv)

    indxs, corr = fast_correlation("Point1 Correlation/Corr_input signal1.txt","Point1 Correlation/Corr_input signal2.txt")
    print(corr)
    corr_com.Compare_Signals("Point1 Correlation/CorrOutput.txt",indxs,corr)

if __name__ == "_main_":
    main()