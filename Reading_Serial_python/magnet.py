import numpy as np
import matplotlib.pyplot as plt
import csv

#moving the magnet in the x direction

x = []
y = []
z = []
t = 0

with open('mag2.csv', 'r') as csvfile:
    
    read = csv.reader(csvfile)
    
    
    for row in read:
        #These scale factors are the standard deviation of the background noise
        x.append(float(row[0]))#/605)#/605)
        y.append(float(row[1]))#/771)#/771)
        z.append(float(row[2]))#/479)#/479)
        t = t+1

mod = []

means = []
stdvs = []

time = np.arange(1,t+1)
for i in time-1:
    mod.append(np.sqrt((x[i])**2+(y[i])**2+(z[i])**2))

components = [x,y,z,mod]
components_names = ['x','y','z','Modulus']

#Change the values based on ploting
for i in components:
    k = 0
    while (k < t-100):
        if (i[k] - np.mean(i[k:k+100]) < 20):
            static_min = k
            break
        else:
            k = k+10

    
    means.append(np.mean(i[static_min:static_min + 100]))  
    stdvs.append(np.std(i[static_min:static_min+ 100]))

plt.figure()
plt.plot(time[400:500], x[400:500]- means[0])

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

in_peak = 0
i = 0
mytime = 0
while i < len(x):
    #we want peak need to edit this 
    if (abs(x[i]-means[0]) >40000) and in_peak == 0:
        mytime = time[i]
        object_detected = 1
        print(f"object found {time[i]} {x[i]-means[0]}")
        in_peak = 1
    if abs(x[i]-means[0]) < 10000 and time[i] >mytime +100:
        in_peak = 0
        
    i = i+1
        

