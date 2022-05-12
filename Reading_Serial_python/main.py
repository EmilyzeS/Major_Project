# This is a Python script to parse the example messages from a file.

import time
import serial
import struct
import traceback

MSG_HEADER_SIZE = 16

def read_packet(f):
    header_bytes = f.read(MSG_HEADER_SIZE)

    if len(header_bytes) < MSG_HEADER_SIZE:
        # must be out of messages
        return False



    header_data = struct.unpack(">H8sHHH", header_bytes)
    

    #checksum on the header sentinels
    if(header_data[0] + header_data[4] != 100487):
        #print(str(header_data[0]) + "," + str(header_data[4])) 
        #print("Header Sentinels Do not add up.")
        return True





    #print("header sentinels: " + str(hex(header_data[0])) + ", " + str(hex(header_data[4])))

    message_type = header_data[1].split(b'\0', 1)[0]  # remove the null characters from the string
    print(message_type)
    #print("message size: " + str(header_data[2]))

    if message_type == b"text":
        text_bytes = f.read(header_data[2])
        print("text message: " + str(text_bytes))
    elif message_type == b"gyro":

        gyro_bytes = f.read(header_data[2])
        gyro_data = struct.unpack(">hhhhH", gyro_bytes)
        
        # if(header_data[2] > 10) or (gyro_data[0] != 39030):
        #     # print(str(gyro_data[4]) +","+ str(header_data[4]))
        #     print("Gyro data corrupted")
        #     return True

        g = open('Desktop\Major_Project\Reading_Serial_python\gyrodata.txt', 'a')
        g.writelines("gyro message: " + str(gyro_data[1]) + ", " + str(gyro_data[2]) + ", " + str(gyro_data[3]) + ", time=" + str(gyro_data[4]) + "\n")
        g.close()
    elif message_type == b"buttons":
        buttons_bytes = f.read(header_data[2])
        print("buttons message: " + str(hex(buttons_bytes[1])) + ", time=" + str(buttons_bytes[2]))
    elif message_type == b"angle":
        angle_bytes = f.read(header_data[2])
        angle_data = struct.unpack(">hhhH", angle_bytes)

        g = open('Desktop\Major_Project\Reading_Serial_python\gledata.txt', 'a')
        g.writelines("azimuth: "+ str(angle_data[1])+ " elevation: " + str(angle_data[2]) + "\n")
        g.close()
    elif message_type == b"lidar":
        lidar_bytes = f.read(header_data[2])
        lidar_data = struct.unpack(">hhH", lidar_bytes)

        g = open('Desktop\Major_Project\Reading_Serial_python\lidar.txt.txt', 'a')
        g.writelines("lidar: " + str(lidar_data[1]) + "\n")
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



# main program entry point
if __name__ == '__main__':
    #read_file('C:/Users/Stewart Worrall/Documents/data/test.hex')
    read_serial("COM4")
