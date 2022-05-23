# This is a Python script to parse the example messages from a file.
import serial_functions as sf
import time
import serial
import traceback
import data_output as do
import initialise_serial


# main program entry point
if __name__ == '__main__':

    #clear files
    #do.clear_file('angledata.csv')
    #do.clear_file('lidar.csv')
    #do.clear_file('mag.csv')
    #do.clear_file('calibration.csv')
    #do.clear_file('gyro.csv')
    do.clear_all_files()
    
    initialise_serial.serialinit()
    
    while True:
        # constantly checking if there is data in the serial port
        while True:

            # Wait until there is data waiting in the serial buffer
            if initialise_serial.serialPort.in_waiting > 0:

                try:
                    if not sf.read_packet(initialise_serial.serialPort):
                        break
                except Exception as e:
                    # Logs the error appropriately. 
                    print(traceback.format_exc())
                    break
            
            else:
                time.sleep(0.05)
            # sf.read_serial("COM4")
            #sf.sendPoint(2,2)

        #sendPoint(2,2)


