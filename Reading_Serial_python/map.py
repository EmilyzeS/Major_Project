from re import S
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans

def convertAnglesGyro(gyro_velocities):
    servo_positions = pd.DataFrame(columns = ['Azimuth', 'Elevation'])
    servo_positions['Azimuth'] = np.zeros(len(gyro_velocities))
    servo_positions['Elevation'] = np.zeros(len(gyro_velocities))

    times = list(gyro_velocities['time'].values)

    delta_time = []
    delta_time.append(0)
    
    i = 1
    while i < len(times):
        if times[i] > times[i-1]:
            delta_time.append(times[i] - times[i-1])
        else:
            delta_time.append(times[i] + 2**16 - 1 - times[i-1])
        
        i += 1

    delta_time.pop(0)
    delta_time.append(0)

    gyro_velocities['Delta Time'] = np.array(delta_time)
    gyro_velocities['Delta Time'] = gyro_velocities['Delta Time'] / (24 * 10**6)


    azimuths = [0]
    elevations = [0]
    
    i = 1
    while i  < len(delta_time):
        azimuths.append(azimuths[i-1] + gyro_velocities['Delta Time'][i-1] * gyro_velocities['xvel'][i-1])
        elevations.append(elevations[i-1] + gyro_velocities['Delta Time'][i-1] * gyro_velocities['yvel'][i-1])
        i += 1
    
    servo_positions['Azimuth'] = np.array(azimuths)
    servo_positions['Elevation'] = np.array(elevations)

    servo_positions['Azimuth'] *= 180/np.pi
    servo_positions['Elevation'] *= 180/np.pi


    return servo_positions

def polarToRectangularGyro(ranges, servo_angles):
    hits = pd.DataFrame(columns = ['X', 'Y','Z','D'])
    cosVals = np.cos(servo_angles['Elevation'])
    sinVals = np.sin(servo_angles['Elevation'])
    hits['Z'] = ranges["Ranges"] * sinVals
    hits['D'] = ranges["Ranges"] * cosVals
  
    

    cosVals = np.cos(servo_angles['Azimuth'])
    sinVals = np.sin(servo_angles['Azimuth'])
    hits['X'] = hits['D'] * cosVals
    hits['Y'] = hits['D'] * sinVals

    return hits




def map():
    lidar_readings = pd.read_csv ('lidar.csv', header = None)
    ranges = lidar_readings/(24*10**(3))
    ranges.set_axis(["Ranges"], axis = 1, inplace = True)

    gyro_velocities = pd.read_csv('gyro.csv',  header = None)
    gyro_velocities.set_axis(["xvel", "yvel","zvel","time"], axis = 1, inplace = True)

    servo_angles = convertAnglesGyro(gyro_velocities) 

    hits = polarToRectangularGyro(ranges, servo_angles)
    hits.dropna()

    model = DBSCAN(eps = 0.1, min_samples = 20).fit(hits[['X','Y']])
    colors = model.labels_

    numClusters = len(np.unique(colors))
    if -1 in colors:
        numClusters -= 1

    clusters = []

    for cluster in range(numClusters):
        cluster_hits = pd.DataFrame(hits)[model.labels_ == cluster]
        kmeans = KMeans(n_clusters= 1, random_state=0).fit(cluster_hits)
        clusters.append((cluster_hits, kmeans.cluster_centers_))
        print(kmeans.cluster_centers_)


    plt.figure("Data")
    plt.scatter(hits['X'], hits['Y'], c=colors, marker='o')

    hits_xy = []

    for cluster in range(numClusters):
        plt.figure("Filtered data")
        print(clusters[cluster])
        point = (clusters[cluster][1][0][0], clusters[cluster][1][0][1])
        hits_xy.append(point)
        plt.scatter(clusters[cluster][0]['X'], clusters[cluster][0]['Y'], marker='o')
        plt.scatter(point[0], point[1] ,marker = 'o')


    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(projection='3d')
    ax.scatter(hits['X'], hits['Y'],hits['Z'])
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()

    return hits_xy

def prepareData(data):
    messages = []
    for hit in data:
        x = data[0]*100
        x = x.zfill(3)

        y = data[1]*100
        y  y.zfill(3)
        message =  x + y
        messages.append(message)






    



