import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# def convertAnglesGyro(gyro_velocities,servo_positions):
#     servo_positions[0;:] = 0
#     for i in servo_positions:
#         servo_positions[i+1][0] = servo_positions[i][0]+ gyro_velocities[i][0]*((gyro_velocities[i+1][3]-gyro_velocities[i][3])*(1/(24*10**6)))
#         servo_positions[i+1][1] = servo_positions[i][1]+ gyro_velocities[i][2]*((gyro_velocities[i+1][3]-gyro_velocities[i][3])*(1/(24*10**6)))


#     return servo_positions


def convertAngles(servo_positions):
    maxVal = servo_positions['Azimuth'].max()
    minVal = servo_positions['Azimuth'].min()
    difference = maxVal - minVal
    servo_positions['Azimuth'] -= minVal
    servo_positions['Azimuth'] /= difference/100
    servo_positions['Azimuth'] *= 0.7
    servo_positions['Azimuth'] -= 35
  


    maxVal = servo_positions['Elevation'].max()
    minVal = servo_positions['Elevation'].min()
    difference = maxVal - minVal
    servo_positions['Elevation'] -= minVal
    servo_positions['Elevation'] /= difference/100
    servo_positions['Elevation'] *= 0.30

    return servo_positions

def polarToRectangular(ranges, servo_angles):
    hits = pd.DataFrame(columns = ['X', 'Y','Z','D'])
    cosVals = np.cos(servo_angles['Elevation']*np.pi/180)
    sinVals = np.sin(servo_angles['Elevation']*np.pi/180)
    hits['Z'] = ranges["Ranges"] * sinVals
    hits['D'] = ranges["Ranges"] * cosVals
  
    

    cosVals = np.cos(servo_angles['Azimuth']*np.pi/180)
    sinVals = np.sin(servo_angles['Azimuth']*np.pi/180)
    hits['X'] = hits['D'] * cosVals

    hits['Y'] = hits['D'] * sinVals

    return hits




lidar_readings = pd.read_csv ('lidar.csv', header = None)
ranges = lidar_readings/(24*10**(3))
ranges.set_axis(["Ranges"], axis = 1, inplace = True)


# gyro_velocities = pd.read_csv('angledata.csv',  header = None)
# gyro_velocities.set_axis(["xvel", "yvel","zvel","time"], axis = 1, inplace = True)

servo_positions = pd.read_csv('angledata.csv',  header = None)
servo_positions.set_axis(["Azimuth", "Elevation"], axis = 1, inplace = True)

# servo_angles = convertAngles(gyro_velocities, servo_positions) 
servo_angles = convertAngles(servo_positions)

hits = polarToRectangular(ranges, servo_angles)
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection='3d')
ax.scatter(hits['X'], hits['Y'],hits['Z'])
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()











