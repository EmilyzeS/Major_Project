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

def find_modulus(x,y,z,time):
    
    mod = []
    for i in time-1:
        mod.append(np.sqrt((x[i])**2+(y[i])**2+(z[i])**2))
    return mod

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

def shift_data(components, means):
    i = 0
    new_components = []
    while i < len(components):
        new_components_list = []
        new_components.append(new_components_list)
        j = 0
        while j < len(components[i]):
            new_components_list.append(components[i][j] - means[i])
            j = j+1

        i = i+1
        
    return new_components

def plot_summary(components, time):
    plt.figure()
    plt.xlabel('Time')
    plt.ylabel('Magnetic Field Strength')
    plt.plot(time,x,'r', label = 'x')
    plt.plot(time,y,'b', label = 'y')
    plt.plot(time,z,'g',label = 'z')
    plt.legend()
    
    colors = ['b','g','r','purple']
    i = 0
    while i < 4:
    
        plt.figure()
        plt.xlabel('Time')
        plt.ylabel("Magnetic Strength")
        plt.title(f'{components_names[i]}')
        plt.plot(time,(components[i]), c = colors[i])
        print(f'Mean {components_names[i]}: {means[i]}')
        print(f'Standard Deviations {components_names[i]}: {stdvs[i]}\n')
        i = i+1
        
    
    plt.show()

def detect_objects(mod, time, min_magnet_value, max_noise_value, minimum_scan_time):

    buffer = 20
    in_peak = 0
    i = 0
    time_in_peak = 0
    object_detected = 0
    
    objects = []
    
    while i <len(mod) - buffer:
        if abs(mod[i]) > min_magnet_value and in_peak == 0:
            time_in_peak = time[i]
            object_detected = object_detected + 1
            
            plt.plot(time[i:i+minimum_scan_time], mod[i:i+minimum_scan_time])
            plt.title(f'Object Detected Time {time[i]}')
            plt.xlabel('Time')
            plt.ylabel('Magnetic Strength')
            plt.show()
            
            max_peak = max(mod[i:i+minimum_scan_time])
            
            in_peak = 1
            objects.append(max_peak)
            
            print(f"Object found at time {time[i]} with value {round(max_peak)}")
        
        if abs(mod[i]) < max_noise_value and abs(mod[i+2]) < max_noise_value and time[i] > time_in_peak + 200:
            in_peak = 0
            
        i = i+1
    
    return objects

def print_object_summary(objects):
    print(f'\nFound {len(objects)} objects with max values:')
    for i in objects:
        if i == objects[-1]:
            print(round(i))
        else:
            print(f'{round(i)}, ', end = '')        

x,y,z,time = read_data('mag.csv')
mod = find_modulus(x,y,z,time)

components = [x,y,z,mod]
components_names = ['x','y','z','Modulus']

#Update components by subtracting mean
means, stdvs = find_means_stdvs(components)
components = shift_data(components, means)
x, y, z, mod = components[0], components[1], components[2], components[3]

#Plotting
plot_summary(components, time)

min_magnet_value = 5000
max_noise_value = 5000
minimum_scan_time = 200
#Detect objects
objects = detect_objects(mod, time, min_magnet_value, max_noise_value, minimum_scan_time)


print_object_summary(objects)
    
