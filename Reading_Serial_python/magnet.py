import numpy as np
import matplotlib.pyplot as plt
import csv

x = []
y = []
z = []
t = 0

with open('mag.csv', 'r') as csvfile:
    
    read = csv.reader(csvfile)
    
    
    for row in read:
        #These scale factors are the standard deviation of the background noise
        x.append(float(row[0]))#/605)
        y.append(float(row[1]))#/771)
        z.append(float(row[2]))#/479)
        t = t+1

mod = []

means = []
stdvs = []

#Use this line if unsure where data is static
#means = [0, 0, 0, 0]

time = np.arange(1,t+1)
for i in time-1:
    mod.append(np.sqrt((x[i])**2+(y[i])**2+(z[i])**2))

components = [x,y,z,mod]
components_names = ['x','y','z','Modulus']

#Change the values based on ploting
for i in components:
    
    means.append(np.mean(i[500:600]))  
    stdvs.append(np.std(i[400:500]))

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

