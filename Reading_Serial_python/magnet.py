import numpy as np
import matplotlib.pyplot as plt
import csv

#moving the magnet in the x direction
#25cm away from imu
#slowish
#scan round flat face perpendicular to ground
#scan large with longest edge facing IMU and face where they're stuck together perpendicular to ground


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
    static_min = 0
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

def plot_summary(components,components_names, time):
    plt.figure()
    plt.xlabel('Time')
    plt.ylabel('Magnetic Field Strength')
    plt.plot(time,components[0],'r', label = 'x')
    plt.plot(time,components[1],'b', label = 'y')
    plt.plot(time,components[2],'g',label = 'z')
    plt.legend()
   
    colors = ['b','g','r','purple']
    i = 0
    while i < 4:
   
        plt.figure()
        plt.xlabel('Time')
        plt.ylabel("Magnetic Strength")
        plt.title(f'{components_names[i]}')
        plt.plot(time,(components[i]), c = colors[i])
        plt.savefig(f'magnet_data_{components_names[i]}')
        i = i+1
       
   
    #plt.show()

def detect_objects(mod, time, min_magnet_value, max_noise_value, minimum_scan_time):

    buffer = 20
    in_peak = 0
    i = 0
    time_in_peak = 0
    object_detected = 0
   
    objects = []
    times = []    
    while i <len(mod) - buffer:
        if abs(mod[i]) > min_magnet_value and in_peak == 0:
            time_in_peak = time[i]
            object_detected = object_detected + 1
           
            plt.plot(time[i:i+minimum_scan_time], mod[i:i+minimum_scan_time])
            plt.title(f'Object Detected Time {time[i]}')
            plt.xlabel('Time')
            plt.ylabel('Magnetic Strength')
            plt.savefig(f'magnet_data_peak_{time[i]}')
            #plt.show()
           
            max_peak = max(mod[i:i+minimum_scan_time])
           
            in_peak = 1
            objects.append(max_peak)
            times.append(time_in_peak)
           
            print(f"Object found at time {time[i]} with value {round(max_peak)}")
       
        if abs(mod[i]) < max_noise_value and abs(mod[i+2]) < max_noise_value and time[i] > time_in_peak + 200:
            in_peak = 0
           
        i = i+1
   
    return objects, times

def print_means_stdvs(means, stdvs, components_names):
    i = 0
    while i < 4:
        print(f'Mean {components_names[i]}: {means[i]}')
        print(f'Standard Deviations {components_names[i]}: {stdvs[i]}\n')
        i = i+1

def print_object_summary(object_peaks):
    print(f'\nFound {len(object_peaks)} objects with max values:')
    for i in object_peaks:
        if i == object_peaks[-1]:
            print(round(i))
        else:
            print(f'{round(i)}, ', end = '')  
   

def write_object_summary_file(objects,num_objects, names, peak_times, costs):
    f = open("summary.txt", 'w')
    f.write("Summary of Objects Scanned\n\n")
    f.write(f'Found {len(objects)} Items:\n\n')
    i = 0
    while i < len(num_objects):
        if num_objects[i] == 1:
           
            f.write(f'Object {names[i]} : {num_objects[i]} item, ')
        else:
            f.write(f'Object {names[i]} : {num_objects[i]} items, ')
        f.write(f'Cost: ${costs[i]}\n')
        i = i+1
    i= 0
    f.write(f'\nTotal cost: ${costs[3]}\n')
    f.write('\nScanning Data:\n')
    while i < len(objects):
        f.write(f'Object {names[objects[i]]} found at time stamp {peak_times[i]}\n')
        i = i+1
    f.close()
       
       

def classify_objects(object_peaks):
    objects = []
    num_objects = [0, 0, 0]
    for i in object_peaks:
        #small = 1 small round = 1500 - 8000 Allbran  0
        #medium = 2 small round = 8000 - 1700 ish weetBix  1
        #large = 1800+ Cheerios  2
       
        if i < 8000:
            objects.append(0)
        elif i < 17000:
            objects.append(1)
        elif i > 17000:
            objects.append(2)
   
    for i in objects:
        num_objects[i] = num_objects[i] + 1
           
    return objects, num_objects
           
           
def find_cost(prices, num_objects):
   total_cost = 0
   costs = []
   i = 0
   while i < len(num_objects):
       total_cost = total_cost + num_objects[i] * prices[i]
       costs.append(num_objects[i] * prices[i])
       i = i+1
   
   costs.append(total_cost)
   return costs      


   
def analyse_magnets():
    x,y,z,time = read_data('mag.csv')
    mod = find_modulus(x,y,z,time)
   
    components = [x,y,z,mod]
    components_names = ['x','y','z','Modulus']
   
    #Update components by subtracting mean
    means, stdvs = find_means_stdvs(components)
    components = shift_data(components, means)
    x, y, z, mod = components[0], components[1], components[2], components[3]
   
    #Plotting
    plot_summary(components,components_names, time)
   
    print_means_stdvs(means, stdvs, components_names)
   
    min_magnet_value = 5000
    max_noise_value = 5000
    minimum_scan_time = 200
    #Detect objects
    object_peaks, peak_times = detect_objects(mod, time, min_magnet_value, max_noise_value, minimum_scan_time)
   
    objects, num_objects = classify_objects(object_peaks)
   
    names = ['Allbran', 'weetBix', 'Cheerios']
   
    print_object_summary( object_peaks)
   
    prices = [9,7,15]
   
    costs = find_cost(prices, num_objects)
    write_object_summary_file(objects, num_objects, names, peak_times, costs)
#Total count and total cost on lcd
#point_message = struct.pack('<hhhh', 88, num_objects[0], num_objects[1], num_objects[2])

analyse_magnets()
