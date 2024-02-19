import csv
import CompareSignal
import numpy as np
import matplotlib.pyplot as plt

def main():
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


    def Corr (X1,X2):
    #correlation
        x1 = X1
        x2 = X2
        N = len(x1)
        sum_X1 = 0
        sum_X2 = 0
        for i in range(len(x1)):
            sum_X1 += x1[i] ** 2
        for i in range(len(x2)):
            sum_X2 += x2[i] ** 2

        bottom_Num = ((sum_X1*sum_X2) ** 0.5)/N

        corr = []
        for j in range(N):
            Cur_Res = 0
            for i in range(N):
                Cur_Res += (x1[i]*x2[i])

            tem = x2[0]
            x2.pop(0)
            x2.append(tem)
            corr.append(((Cur_Res)/N)/bottom_Num)

        return corr
    # corr=[]
    indix1, X1 = prepare_data("Point1 Correlation/Corr_input signal1.txt")
    indix2, X2 = prepare_data("Point1 Correlation/Corr_input signal2.txt")
    corr = Corr(X1, X2)

    CompareSignal.Compare_Signals("Point1 Correlation/CorrOutput.txt", indix1, corr)

    ################## point 3  #############################point 3#########################
    def prepare_data_for_template(file_path):
        with open(file_path, 'r') as f:
            csv_f = csv.reader(f)
            y_data = []
            for row in csv_f:
                y_value = int(row[0])
                y_data.append(y_value)
        return y_data


    def template_match (test,class1,class2):
        corr1 = Corr(test, class1)
        corr2 = Corr(test, class2)
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
        "point3 Files/Class 1/down1.txt",
        "point3 Files/Class 1/down2.txt",
        "point3 Files/Class 1/down3.txt",
        "point3 Files/Class 1/down4.txt",
        "point3 Files/Class 1/down5.txt",
    ]
    class_2_path = [
        "point3 Files/Class 2/up1.txt",
        "point3 Files/Class 2/up2.txt",
        "point3 Files/Class 2/up3.txt",
        "point3 Files/Class 2/up4.txt",
        "point3 Files/Class 2/up5.txt",
    ]

    tests = [
        "point3 Files/Test Signals/Test1.txt",
        "point3 Files/Test Signals/Test2.txt",
    ]

    class_1 = []
    class_2 = []
    for i in range(len(prepare_data_for_template(class_1_path[0]))):
        temp_1=0
        temp_2=0
        for j in range(len(class_1_path)):
            temp_1 += prepare_data_for_template(class_1_path[j])[i]
            temp_2 += prepare_data_for_template(class_2_path[j])[i]
        class_1.append(temp_1/5)
        class_2.append(temp_2/5)

    def Time_analysis(signal1, signal2, fs):
        if len(signal1) < len(signal2):
            for i in range(len(signal1)):
                signal1.append(signal1[i])
        elif len(signal2) < len(signal1):
            for i in range(len(signal2)):
                signal2.append(signal2[i])
        print ("signal1",signal1)
        print ("signal2",signal2)

        cor = Corr(signal1, signal2)
        print ("cor",cor)
        m= max(cor)
        ind= 0
        for i in range (len(cor)):
            if cor[i] == m :
                ind = i
        #max_corr_index = cor.index(max(cor))
        print("max_corr_index",ind)
        ts =  ind/ fs
        return ts
    pathes = ["Point2 Time analysis/TD_input signal1.txt",
              "Point2 Time analysis/TD_input signal2.txt"]
    sindex1, value1 = prepare_data(pathes[0])
    sindex2, value2 = prepare_data(pathes[1])
    print("sindex1, value1",sindex1, value1)
    print("sindex2, value2",sindex2, value2)

    plt.figure(figsize=(10, 10))
    plt.subplot(2, 1, 1)
    plt.plot(sindex1, value1)
    plt.title("before")
    plt.grid(True)
    #plt.axhline(0, color='black', linestyle='-', linewidth=1)
    plt.tight_layout()

    plt.subplot(2, 1, 2)
    plt.plot(sindex2, value2)
    plt.title("after")
    plt.grid(True)
    plt.axhline(0, color='black', linestyle='-', linewidth=1)
    plt.tight_layout()
    plt.show()
    print("time delay is",Time_analysis(value1, value2,100))


    test_1 = prepare_data_for_template(tests[0])
    test_2 = prepare_data_for_template(tests[1])

    template_match(test_1, class_1, class_2)

    template_match(test_2, class_1, class_2)


if __name__ == "__main__":
    main()