# This is a Python script to parse the example messages from a file.
import data_output as do
import serial_functions as sf

# main program entry point
if __name__ == '__main__':

    #clear files
    #do.clear_file('angledata.csv')
    #do.clear_file('lidar.csv')
    #do.clear_file('mag.csv')
    #do.clear_file('calibration.csv')
    #do.clear_file('gyro.csv')
    do.clear_all_files()
    
    while(1):

        sf.read_serial("COM4")
        #sf.sendPoint(2,2)

    #sendPoint(2,2)


