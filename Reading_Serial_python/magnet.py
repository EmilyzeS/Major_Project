import numpy as np
import matplotlib.pyplot as plt
import csv

#moving the magnet in the x direction

def read_data(filename):
    
    x = []
    y = []
    z = []
    t = 0
    
    with open(filename, 'r') as csvfile:
        read = csv.reader(csvfile)
        for row in read:
            #These scale factors are the standard deviation of the background noise
            x.append(float(row[0]))#/605)#/605)
            y.append(float(row[1]))#/771)#/771)
            z.append(float(row[2]))#/479)#/479)
            t = t+1
            
        time = np.arange(1,t+1)
    return x, y, z, time

x,y,z,time = read_data('mag2.csv')

def find_modulus(x,y,z,time):
    
    mod = []
    for i in time-1:
        mod.append(np.sqrt((x[i])**2+(y[i])**2+(z[i])**2))
    return mod

mod = find_modulus(x,y,z,time)
components = [x,y,z,mod]
components_names = ['x','y','z','Modulus']

def find_means_stdvs(components):
    
    means = []
    stdvs = []
    for i in components:
        k = 0
        while (k < len(components[0])-100):
            if (i[k] - np.mean(i[k:k+100]) < 20):
                static_min = k
                break
            else:
                k = k+10
    
        
        means.append(np.mean(i[static_min:static_min + 100]))  
        stdvs.append(np.std(i[static_min:static_min+ 100]))
    return means, stdvs

means, stdvs = find_means_stdvs(components)

#************************************************************
#******************Testing stuff*****************************
plt.figure()
plt.plot(time[1086:1300], x[1086:1300]- means[0])
#*******************************************************
#*******************************************************


#Plotting
plt.figure()
plt.xlabel('Time')
plt.ylabel('Magnetic Field Strength')
plt.plot(time,x - means[0],'r', label = 'x')
plt.plot(time,y - means[1],'b', label = 'y')
plt.plot(time,z - means[2],'g',label = 'z')
plt.legend()

colors = ['b','g','r','purple']
i = 0
while i < 4:

    plt.figure()
    plt.xlabel('Time')
    plt.ylabel("Magnetic Strength")
    plt.title(f'{components_names[i]}')
    plt.plot(time,(components[i]- means[i]), c = colors[i])

    #plt.plot(time,(components[i]- means[i])/stdvs[i], c = colors[i])
    print(f'Mean {components_names[i]}: {means[i]}')
    print(f'Standard Deviations {components_names[i]}: {stdvs[i]}')
    i = i+1
    

plt.show()
print('\n')

#*******************************************************
#*******************************************************
#****************WORK IN PROGRESS***********************
in_peak = 0
i = 0
mytime = 0
object_detected = 0
peaks = []

while i < len(x)-20:
    if (abs(x[i]-means[0]) >30000) and in_peak == 0:
        mytime = time[i]
        object_detected = object_detected + 1
        #I will edit this so it is the peak value
        print(f"Object found at time {time[i]} with value {round(abs(x[i]-means[0]))}")
        in_peak = 1
    if (abs(x[i]-means[0]) >30000) and in_peak == 1:
        object_detected = object_detected + 1
        peaks.append(abs(x[i]-means[0]))
        
    if abs(x[i]-means[0]) < 10000 and abs(x[i+1]-means[0]) < 10000 and time[i] > mytime + 50:
        in_peak = 0
        if object_detected != 0:
            #print(time[i])
            peak_duration = time[i] - mytime
            print(f'Duration object is detected for is {peak_duration} time units\n')
            object_detected = 0
            mytime = time[i]
        
    i = i+1
        

