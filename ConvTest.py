#import task62
def ConvTest(Your_indices,Your_samples):
    """
    Test inputs
    InputIndicesSignal1 =[-2, -1, 0, 1]
    InputSamplesSignal1 = [1, 2, 1, 1 ]
    
    InputIndicesSignal2=[0, 1, 2, 3, 4, 5 ]
    InputSamplesSignal2 = [ 1, -1, 0, 0, 1, 1 ]
    """
    
    expected_indices=[-2, -1, 0, 1, 2, 3, 4, 5, 6]
    expected_samples = [1, 1, -1, 0, 0, 3, 3, 2, 1 ]

    
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Conv Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Conv Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Conv Test case failed, your signal have different values from the expected one") 
            return
    print("Conv Test case passed successfully")


InputIndicesSignal1 = [-2, -1, 0, 1]
InputSamplesSignal1 = [1, 2, 1, 1]

InputIndicesSignal2 = [0, 1, 2, 3, 4, 5]
InputSamplesSignal2 = [1, -1, 0, 0, 1, 1]

def convolve_signals(signal1_indices, signal1_samples, signal2_indices, signal2_samples):
    m = len(signal1_samples)
    n = len(signal2_samples)
    result = [0] * (m + n - 1)  # Initialize the result array with zeros
    result_indices = [0] * (m + n - 1)  # Initialize the result indices array

    for i in range(m):
        for j in range(n):
            result[i + j] += signal1_samples[i] * signal2_samples[j]
            result_indices[i + j] = signal1_indices[i] + signal2_indices[j]


    return result_indices, result

indecies  , samples = convolve_signals(InputIndicesSignal1,InputSamplesSignal1,InputIndicesSignal2,InputSamplesSignal2)
ConvTest(indecies  , samples)