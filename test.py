import numpy as np
from scipy.fft import fft, ifft

def fft_convolution(indices1, samples1, indices2, samples2):
    # Pad the signals to avoid circular convolution
    padded_signal1 = np.pad(samples1, (0, len(samples2) - 1), mode='constant')
    padded_signal2 = np.pad(samples2, (0, len(samples1) - 1), mode='constant')

    # Compute the FFT of the padded signals
    fft_signal1 = fft(padded_signal1)
    fft_signal2 = fft(padded_signal2)

    # Multiply the FFTs element-wise
    fft_result = fft_signal1 * fft_signal2

    # Compute the inverse FFT to get the convolution result
    result = np.real(ifft(fft_result))

    # Trim the result to the appropriate size
    result = result[:len(samples1) + len(samples2) - 1]

    # Combine the indices
    combined_indices = np.arange(indices1[0] + indices2[0], indices1[-1] + indices2[-1] + 1)

    return combined_indices, result

# Test inputs
InputIndicesSignal1 = [-2, -1, 0, 1]
InputSamplesSignal1 = [1, 2, 1, 1]

InputIndicesSignal2 = [0, 1, 2, 3, 4, 5]
InputSamplesSignal2 = [1, -1, 0, 0, 1, 1]

# Calculate convolution using DFT-based method
result_indices, result_samples = fft_convolution(InputIndicesSignal1, InputSamplesSignal1, InputIndicesSignal2, InputSamplesSignal2)

# Expected output
expected_indices = [-2, -1, 0, 1, 2, 3, 4, 5, 6]
expected_samples = [1, 1, -1, 0, 0, 3, 3, 2, 1]

print("Computed Indices:", result_indices)
print("Computed Samples:", result_samples)
print("Expected Indices:", expected_indices)
print("Expected Samples:", expected_samples)
print("Indices Match:", np.array_equal(result_indices, expected_indices))
print("Samples Match:", np.allclose(result_samples, expected_samples))
