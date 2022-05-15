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
        x.append(row[0])
        y.append(row[1])
        z.append(row[2])
        t = t+1

time = np.arange(1,t)
figure()
plt.plot(t,x,'r')
plt.plot(t,y,'b')
plt.plot(t,z,'g')
plt.legend()
plt.show()


    


