from re import S
import pandas as pd
import numpy as np
import data_output as do

def CalibrateGyro():
    gyro_calibration_velocities = pd.read_csv('gyro.csv',  header = None)
    gyro_calibration_velocities.set_axis(["xvel", "yvel","zvel","time"], axis = 1, inplace = True)
    x_offset=np.average(gyro_calibration_velocities['xvel'])
    y_offset=np.average(gyro_calibration_velocities['yvel'])
    
    return x_offset, y_offset


