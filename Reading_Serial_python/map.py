import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def convertAngles(servo_positions):
    maxVal = servo_positions['Azimuth'].max()
    minVal = servo_positions['Azimuth'].min()
    difference = maxVal - minVal
    servo_positions['Azimuth'] -= minVal
    servo_positions['Azimuth'] /= difference/100
    servo_positions['Azimuth'] *= 0.9
    servo_positions['Azimuth'] -= 45

    return servo_positions['Azimuth']

def polarToRectangular(ranges, azimuths):
    hits = pd.DataFrame(columns = ['X', 'Y'])
    cosVals = np.cos(azimuths*np.pi/180)
    sinVals = np.sin(azimuths*np.pi/180)
    hits['X'] = ranges["Ranges"] * cosVals
    hits['Y'] = ranges["Ranges"] * sinVals

    return hits

def map():
    C = 299792458

    lidar_readings = pd.read_csv ('lidar.csv', header = None)
    ranges = C*lidar_readings*10**(-13)
    ranges.set_axis(["Ranges"], axis = 1, inplace = True)


    servo_positions = pd.read_csv('angledata.csv',  header = None)
    servo_positions.set_axis(["Azimuth", "Elevation"], axis = 1, inplace = True)

    azimuths = convertAngles(servo_positions)
    hits = polarToRectangular(ranges, azimuths)

    plt.scatter(hits['X'], hits['Y'])
    plt.show()











