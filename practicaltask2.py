import practicaltask
import numpy as np
import math
import task7
import csv
lags = range(10)


def prepare_data_for_template(file_path):
    with open(file_path, 'r') as f:
        csv_f = csv.reader(f)
        y_data = []
        for row in csv_f:
            y_value = int(row[0])
            y_data.append(y_value)
    return y_data
def DCT (x ):
    y = []
    N = len(x)
    for k in range(N):
        res = 0
        for n in range(N):
            s = ((np.pi / (4 * N)) * ((2 * n) - 1) * ((2 * k) - 1))
            res = res + (math.sqrt(2 / N) * x[n] * math.cos(s))
        y.append(res)
    print(y)
    return y
def auto_corr(data):
    # Pre-allocate autocorrelation table
    acorr = len(lags) * [0]

    # Mean
    mean = sum(data) / len(data)

    # Variance
    var = sum([(x - mean) ** 2 for x in data]) / len(data)

    # Normalized data
    ndata = [x - mean for x in data]

    # Go through lag components one-by-one
    for l in lags:
        c = 1  # Self correlation

        if (l > 0):
            tmp = [ndata[l:][i] * ndata[:-l][i]
                   for i in range(len(data) - l)]

            c = sum(tmp) / len(data) / var

        acorr[l] = c
    return acorr

def normalize (x):
    x_max = np.max(x)
    x_min = np.min(x)
    combined_x = [((x1 - x_min) / (x_max - x_min)) for x1 in x]
    return combined_x


def remove_dc(x , N):
    mean = np.mean(x)
    print("mean", mean)

    dc_removed = []
    # component removal
    for i in range(N):
        dc_removed.append(x[i] - mean)
    # Create the figure and subplots
    return dc_removed


def template_match (test,class1,class2):
        corr1 = task7.Corr(test, class1)
        corr2 = task7.Corr(test, class2)
        if np.max(corr1) > np.max(corr2):
            print("\ntst is down movement of EOG signal(CLASS_1)\n")
            return 0
        elif np.max(corr1) < np.max(corr2):
            print("\ntst is up movement of EOG signal(CLASS_2)\n")
            return 0
        else:
            print("Correlation is the same with tow classes\n")
        return 0

class_1_path = [
            "pythonProject8/A/ASeg1.txt",
            "pythonProject8/A/ASeg2.txt",
            "pythonProject8/A/ASeg3.txt",
            "pythonProject8/A/ASeg4.txt",
            "pythonProject8/A/ASeg5.txt",
            "pythonProject8/A/ASeg6.txt"]
class_2_path = [
            "pythonProject8/B/BSeg1.txt",
            "pythonProject8/B/BSeg2.txt",
            "pythonProject8/B/BSeg3.txt",
            "pythonProject8/B/BSeg4.txt",
            "pythonProject8/B/BSeg5.txt",
            "pythonProject8/B/BSeg6.txt"
        ]

tests = [
            "pythonProject8/Test Folder/ATest1.txt",
            "pythonProject8/Test Folder/BTest1.txt",
        ]

class_1 = []
class_2 = []
for i in range(len(prepare_data_for_template(class_1_path[0]))):
            temp_1=0
            temp_2=0
            for j in range(len(class_1_path)):
                temp_1 += prepare_data_for_template(class_1_path[j])[i]
                temp_2 += prepare_data_for_template(class_2_path[j])[i]
            class_1.append(temp_1/6)
            class_2.append(temp_2/6)



def all (signal , index ,fs, fc1, fc2, tw, N , new_fs ,maxF , M , L ,stopband, cutoff_frequency):
    sig  = practicaltask.BPF(fs, fc1, fc2, tw, N)
    if new_fs >= 2 *maxF:
        sig = practicaltask.resampling(sig, L , M, fs ,stopband,cutoff_frequency,tw)
    else :
        print ("new_fs is not right")

    # remove dc component
    sig = remove_dc(sig, len(sig))
    # normalize
    sig = normalize(sig)
    #auto correlation
    corr = auto_corr(sig)
    #DCT
    y = DCT(sig)

    template_match(y,class_1 , class_2)





