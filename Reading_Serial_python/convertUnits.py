import numpy as np

def ConvertGyro(value: int):
    return (float(value)*250/ 2**15) * np.pi/180

def ConvertMagnet(value : int):
    return (float(value)*16/2**12) #maybe power 16???