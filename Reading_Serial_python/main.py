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

    g = open('Desktop\Major_Project\Reading_Serial_python\gyrodata.txt', 'a')


    header_data = struct.unpack(">H8sHHH", header_bytes)

    #g.writelines("header sentinels: " + str(hex(header_data[0])) + ", " + str(hex(header_data[4])))
    #g.write("\n")

    message_type = header_data[1].split(b'\0', 1)[0]  # remove the null characters from the string
    print(message_type)
    #g.writelines("message size: " + str(header_data[2]))
    #g.write("\n")

    if message_type == b"text":
        text_bytes = f.read(header_data[2])
        print("text message: " + str(text_bytes))
    elif message_type == b"gyro":
        gyro_bytes = f.read(header_data[2])
        gyro_data = struct.unpack(">hhhhH", gyro_bytes)
        g.writelines("gyro message: " + str(gyro_data[1]) + ", " + str(gyro_data[2]) + ", " + str(gyro_data[3]) + ", time=" + str(gyro_data[4]) + "\n")
    elif message_type == b"buttons":
        buttons_bytes = f.read(header_data[2])
        print("buttons message: " + str(hex(buttons_bytes[1])) + ", time=" + str(buttons_bytes[2]))

    #g.write("\n")

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
    serialPort = serial.Serial(port=com_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
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
