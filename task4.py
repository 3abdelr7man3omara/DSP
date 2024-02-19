import numpy as np
import matplotlib.pyplot as plt
import signalcompare
import cmath


def get_freq(N, fs):
    freq = []
    if N  != 0:
        # Concatenate positive and negative frequencies
        # freq = np.float64(freq)
        # Scale frequencies by the sample spacing
        for i in range (N):
            freq.append((((np.pi*fs*2)/N)*(i+1)))

    return freq


def dft(x,d):
        N = len(x)
        n = np.arange(N)
        k = np.arange(N)
        freq = get_freq(N , d)
        #X =[0] * N
        #    reconstructed_signal = np.zeros(N, dtype=complex)
        result =np.zeros(N, dtype=complex)
        X= []
        for i in k :
            e = []
            for j in n:
                e.append(np.exp(-2j * np.pi * i * j/ N))
            sum = np.dot(e , x)
            result[i] = result[i]+ sum
            X.append(sum)
        """ n=0
                for k in range(N):
                    X=sum(x[k]*np.exp(-2j * np.pi * k * n / N))
                    n+=1"""
        return result,freq


def idft(x):
    N = len(x)
    k = np.arange(N)
    n = np.arange(N)
    result = np.zeros(N, dtype=complex)
    X = []
    for i in n:
        e = []
        for j in k:
            e.append(np.exp(2j * np.pi * i * j / N))
        sum = np.dot(e, x)/ N
        result[i] = result[i] + sum
        X.append(sum)
    return result

def main():
    file_paths = [
        "C:/Users/SCH/Downloads/input_Signal_DFT.txt",
        "C:/Users/SCH/Downloads/Input_Signal_IDFT_A,Phase.txt",
        "C:/Users/SCH/Downloads/Output_Signal_DFT_A,Phase.txt",
        "C:/Users/SCH/Downloads/Output_Signal_IDFT.txt",
    ]
    phase = []
    freq = []
    while True:
        selected_index = int(input("Enter the index of the file "))
        if 0 <= selected_index < len(file_paths):
            break
        else:
            print("Invalid index. Please enter a valid index.")


    selected_file_path = file_paths[selected_index]

    with open(selected_file_path, "r") as file:
        inlines = file.readlines()
    out=[]
    # connecting each input file to it's output
    if selected_index == 0 :

            with open("C:/Users/SCH/Downloads/Output_Signal_DFT_A,Phase.txt", "r") as file:
                outlines = file.readlines()
            outlines = [(line.split()) for line in outlines[3:]]

    else :
            with open("C:/Users/SCH/Downloads/Output_Signal_IDFT.txt", "r") as file:
                outlines = file.readlines()
            outlines = [(line.split()) for line in outlines[3:]]

    for i in range (len(outlines)):
            try:
                amplitude = float(outlines[i][0].replace("f", ""))
                phase = float(outlines[i][1].replace("f", ""))
                out.append((amplitude, phase))
            except ValueError:
                # Handle lines that cannot be converted to float (skip them)
                pass

    out_phase = []
    out_ampletude = []
    for i in out:
        out_phase.append(i[1])
        out_ampletude.append(i[0])

    print("out", out)
    data_format = int(inlines[1])
    if data_format == 0:
        data = [float(line.split()[1]) for line in inlines[3:]]

        sampling_frequency = float(input("Enter the sampling frequency in Hz: "))

        # Compute the Fourier coefficients
        fourier_coeffs ,frequencies= dft(data , d= sampling_frequency)

        print("Discrete Fourier Transform:")
        print(fourier_coeffs)
        print("frequencies:")
        print(frequencies)
        # Compute amplitude and phase
        amplitudes = np.abs(fourier_coeffs)
        phases = np.angle(fourier_coeffs)

        print("\nAmplitudes:")
        print(amplitudes)

        print("\nPhases:")
        print(phases)

        # DFT
        N = len(data)
        # Save frequency components (Amplitude && Phase) in polar form (without the frequency column) to a text file
        with open("DFT.txt", "w") as file:
            file.write("Amplitude, Phase (radians)\n")
            file.write(f"0\n")
            file.write(f"1\n")
            file.write(f"{len(inlines[3:])}\n")
            for i in range(len(frequencies)):
                file.write(f"{amplitudes[i]}f {phases[i]}f\n")

        # frequency vs amplitude
        plt.figure(figsize=(10, 10))
        plt.subplot(2, 1, 1)
        plt.scatter(frequencies, amplitudes)
        plt.title("Frequency vs Amplitude")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.axhline(0, color='black', linestyle='-', linewidth=1)
        plt.tight_layout()
        # frequency vs phase
        plt.subplot(2, 1, 2)
        plt.scatter(frequencies, phases)
        plt.title("Frequency vs Phase")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Phase (radians)")
        plt.grid(True)
        plt.axhline(0, color='black', linestyle='-', linewidth=1)
        plt.tight_layout()

    else:
        # Amplitudes and phases
        data = []
        for line in inlines[3:]:
            parts = line.split(",")
            try:
                amplitude = float(parts[0].replace("f", ""))
                phase = float(parts[1].replace("f", ""))
                data.append((amplitude, phase))
            except ValueError:
                # Handle lines that cannot be converted to float (skip them)
                pass

        print("data",data)
        phases = []
        amplitudes = []
        for i in data:
            phases.append(i[1])
            amplitudes.append(i[0])

        # (IDFT)
        N = len(data)
        reconstructed_signal = np.zeros(N, dtype=complex)
        for i in range(N):
            amplitude, phase = data[i]
            real_part =(amplitude * np.cos(phase))
            imaginary_part = amplitude * np.sin(phase)
            reconstructed_signal[i] = complex(real_part, imaginary_part)
            print("reconstructed_signal",reconstructed_signal[i])

        reconstructed_signal = (idft(reconstructed_signal).real)

        print("j,reconstructed_signal",reconstructed_signal)


        # Plot the reconstructed signal
        plt.figure(figsize=(10, 5))
        plt.plot(reconstructed_signal)
        plt.title("Reconstructed Signal")
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.grid(True)  # Add the grid
        plt.axhline(0, color='black', linestyle='-', linewidth=2)
        plt.tight_layout()

    plt.show()

    signalcompare.SignalComapreAmplitude(amplitudes , out_ampletude )
    signalcompare.SignalComaprePhaseShift(phases , out_phase)



if __name__ == "__main__":
    main()