# This is a Python script to parse the example messages from a file.

import time
import serial
import struct
import traceback
import csv
import pandas as pd
import os

MSG_HEADER_SIZE = 16
MSG_HEADER_SUM = 100487

def clear_file(path : str):
    clear = open(path, 'w')
    clear.close()

def read_packet(f):
    header_bytes = f.read(MSG_HEADER_SIZE)

    if len(header_bytes) < MSG_HEADER_SIZE:
        # must be out of messages
        return False



    header_data = struct.unpack(">H8sHHH", header_bytes)
    

    #checksum on the header sentinels
    if(header_data[0] + header_data[4] != MSG_HEADER_SUM):
        print("Header Sentinels Do not add up.")
        return False






    message_type = header_data[1].split(b'\0', 1)[0]  # remove the null characters from the string
    print(message_type)


    if message_type == b"text":
        text_bytes = f.read(header_data[2])
        print("text message: " + str(text_bytes))
    elif message_type == b"gyro":

        gyro_bytes = f.read(header_data[2])
        gyro_data = struct.unpack(">hhhhH", gyro_bytes)
        
        #check if sentiniel is correct
        if (gyro_data[0] != 39030):
            print("Gyro data corrupted")
            return False

        #write to a csv file
        g = open('gyrodata.txt', 'a', newline='')
        g.writelines("gyro message: " + str(gyro_data[1]) + ", " + str(gyro_data[2]) + ", " + str(gyro_data[3]) + ", time=" + str(gyro_data[4]))
        g.close()
    elif message_type == b"buttons":
        buttons_bytes = f.read(header_data[2])
        print("buttons message: " + str(hex(buttons_bytes[1])) + ", time=" + str(buttons_bytes[2]))
    elif message_type == b"angle":


        #unpack
        angle_bytes = f.read(header_data[2])
        angle_data = struct.unpack(">hhhH", angle_bytes)

        #check sentinel
        if(angle_data[0] != 22136):
            print("Angle data corrupted")
            return False

        #write to a csv file
        g = open('angledata.csv', 'a', newline='')
        
        writer = csv.writer(g)
        
        info = [int(angle_data[1]), angle_data[2]]
        
        writer.writerow(info)
        
        g.close()

    elif message_type == b"lidar":
        lidar_bytes = f.read(header_data[2])
        lidar_data = struct.unpack(">hIH", lidar_bytes)

        if(lidar_data[0] != 4660):
            print("Lidar data corrupted")
            return False

        #write to a csv file
        g = open('lidar.csv', 'a', newline='')
        
        writer = csv.writer(g)

        info = [lidar_data[1]]

        writer.writerow(info)

        g.close()





    return True


def read_file(file_name):
    # open the file
    with open(file_name, "rb") as f:
        while True:
            try:
                if not read_packet(f):
                    break
            except Exception as e:
                print(traceback.format_exc())
                break
                # Logs the error appropriately. 
    

def read_serial(com_port):
    serialPort = serial.Serial(port=com_port, baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialString = ""  # Used to hold data coming over UART

    while True:

        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            try:
                if not read_packet(serialPort):
                    break
            except Exception as e:
                # Logs the error appropriately. 
                print(traceback.format_exc())
                break
       
        else:
            time.sleep(0.05)


        check_if_clear_ready('angledata.csv')

#checks if the lidar has done one complete revolution and clears the written data if it has
def check_if_clear_ready(path : str):
    if(os.path.getsize(path) > 1):



        f = open(path, 'r')
        f_csv = csv.reader(f)

        line_count = 0

        #get the last line and line count
        for row in f_csv:
            if(line_count == 0):
                first_line = row
            line_count += 1
            last_line = row


    
        #if the last read angle is smaller than the first read angle by 1% 
        #if line count > 1000 then there was an for sure and error reading so it never cleared
        # (might not need)
        if(line_count > 100 and (float(first_line[0])*1.02 > float(last_line[0]) ) or line_count > 1000):
            clear_file(path)
            clear_file('lidar.csv')

        f.close()

        


# main program entry point
if __name__ == '__main__':

    #clear files
    clear_file('angledata.csv')
    clear_file('lidar.csv')
    while(1):
    #read_file('C:/Users/Stewart Worrall/Documents/data/test.hex')
        read_serial("COM4")
