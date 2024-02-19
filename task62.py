import csv
import matplotlib.pyplot as plt

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


def smothening (x , n_of_points):
    y = []
    for i in range(0,(len(x)-n_of_points+1)):
        sum = 0
        for j in range( n_of_points):
            sum = sum +x[j+i]
        sum = sum / n_of_points
        y.append(sum)
    return y

def sharpening (x):
    y = []
    y_sec_drev = []

    for i in range(1, (len(x))):
        res = x[i]-x[i-1]
        y.append(res)
    for i in range(1, (len(y))):
        res = y[i]-y[i-1]
        y_sec_drev.append(res)
    return y, y_sec_drev



x , y = prepare_data("OutMovAvgTest2.txt")

s = smothening(y , 2)
print("before smoothng", y)
print ("after", s )
print("x", x)

plt.figure(figsize=(10, 10))
plt.subplot(2, 1, 1)
plt.scatter(x, y)
plt.title("before")
plt.grid(True)
plt.axhline(0, color='black', linestyle='-', linewidth=1)
plt.tight_layout()

plt.subplot(2, 1, 2)
plt.scatter(x[:(len(s))] , s)
plt.title("after")
plt.grid(True)
plt.axhline(0, color='black', linestyle='-', linewidth=1)
plt.tight_layout()

plt.show()

first_drev , sec_drev = sharpening(y)



