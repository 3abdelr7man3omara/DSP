import numpy as np
import matplotlib.pyplot as plt


def apply_fourier_transform(signal):
    return np.fft.fft(signal)


def display_frequency_amplitude(signal, sampling_frequency):
    frequency = np.fft.fftfreq(len(signal), 1 / sampling_frequency)
    amplitude = np.abs(signal)

    plt.plot(frequency, amplitude)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Frequency vs Amplitude')
    plt.show()


def display_frequency_phase(signal, sampling_frequency):
    frequency = np.fft.fftfreq(len(signal), 1 / sampling_frequency)
    phase = np.angle(signal)

    plt.plot(frequency, phase)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Phase')
    plt.title('Frequency vs Phase')
    plt.show()


def modify_amplitude(signal, factor):
    return signal * factor


def modify_phase(signal, angle):
    return np.abs(signal) * np.exp(1j * angle)


def save_frequency_components(signal, filename):
    amplitude = np.abs(signal)
    phase = np.angle(signal)

    data = np.column_stack((amplitude, phase))
    np.savetxt(filename, data, header='Amplitude Phase', fmt='%.6f')


def reconstruct_signal(frequency_components):
    amplitude = frequency_components[:, 0]
    phase = frequency_components[:, 1]
    signal = amplitude * np.exp(1j * phase)
    return np.fft.ifft(signal).real


def read_frequency_components(filename):
    data = np.loadtxt(filename)
    amplitude = data[:, 0]
    phase = data[:, 1]
    frequency_components = np.column_stack((amplitude, phase))
    return frequency_components


# Main program
sampling_frequency = float(input("Enter the sampling frequency in Hz: "))

# Generate an example signal
time = np.linspace(0, 1, int(sampling_frequency))
frequency = 10  # Example frequency
amplitude = 1  # Example amplitude
phase = np.pi / 4  # Example phase
signal = amplitude * np.sin(2 * np.pi * frequency * time + phase)

# Apply Fourier transform
frequency_components = apply_fourier_transform(signal)

# Display frequency versus amplitude and phase relations
display_frequency_amplitude(frequency_components, sampling_frequency)
display_frequency_phase(frequency_components, sampling_frequency)

# Modify amplitude and phase
factor = float(input("Enter the amplitude modification factor: "))
modified_signal = modify_amplitude(frequency_components, factor)

angle = float(input("Enter the phase modification angle in radians: "))
modified_signal = modify_phase(modified_signal, angle)

# Save frequency components to a text file
filename = "frequency_components.txt"
save_frequency_components(modified_signal, filename)

# Reconstruct signal from frequency components
reconstructed_components = read_frequency_components(filename)
reconstructed_signal = reconstruct_signal(reconstructed_components)

# Display the reconstructed signal
plt.plot(time, reconstructed_signal)
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Reconstructed Signal')
plt.show()