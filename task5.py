import math
import numpy as np
import matplotlib.pyplot as plt
import comparesignal2

def read_fie(file_path):
        x = []
        c= []
        with open(file_path, 'r') as file:
            lines = file.readlines()[3:]
            #N = file.readlines()[3:]
            for line in lines:
                print("line", line)
                a, b = line.strip().split(" ")
                a = float(a)
                b = float(b)
                c.append(a)
                x.append(b)
            N = len (x)
            print(N)
        return c,x,N

def DC():
    filepath = "C:/Users/SCH/Downloads/drive-download-20231117T211844Z-001/Lab 5/Task files/DCT/DCT_input.txt"
    c, x , N = read_fie(filepath)
    y = []
    for k in range(N):
        res = 0
        for n in range(N):
            s = ((np.pi/(4*N))*((2*n)-1)*((2*k)-1))
            res = res + (math.sqrt(2/N)*x[n]*math.cos(s))
        y.append(res)
    print(y)
    with open("y.txt", "w") as file:
        file.write(f"0\n")
        file.write(f"0\n")
        file.write(f"{len(y)}\n")
        for i in ((y)):
            file.write(f"{i}\n")
    return y

def remove_dc_component():
    filepath = "C:/Users/SCH/Downloads/drive-download-20231117T211844Z-001/Lab 5/Task files/Remove DC component/DC_component_input.txt"
    c, x , N = read_fie(filepath)

    mean = np.mean(x)
    print("mean" , mean)

    dc_removed=[]
    #component removal
    for i in range(N):
        dc_removed.append(x[i]-mean)
    # Create the figure and subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

    # Top subplot
    ax1.plot(c, x)
    ax1.set_xlim([1, 50])
    ax1.grid(True)
    ax1.set_title('dct')
    ax1.set_xlabel('time(s)')
    ax1.set_ylabel('Acceleration')

    # Bottom subplot
    ax2.plot(c,dc_removed,  'red')
    ax2.grid(True)
    ax2.set_title('dct removal')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Amplitude (m)')

    # Adjust spacing between subplots
    plt.tight_layout()

    # Show the plot
    plt.show()

    #write the file
    with open("dc_removed.txt", "w") as file:
        file.write(f"0\n")
        file.write(f"0\n")
        file.write(f"{len(dc_removed)}\n")
        for i in ((dc_removed)):
            file.write(f"{i}\n")
    return dc_removed

y = DC()
dc_removed = remove_dc_component()

comparesignal2.SignalSamplesAreEqual("DC_component_output.txt",dc_removed)
comparesignal2.SignalSamplesAreEqual("DCT_output.txt",y)


