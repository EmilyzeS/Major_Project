from re import S
import serial
import struct
import sys
import time
import initialise_serial



def serialOutputChar(com_port, header, message):
    #serialPort = serial.Serial(port=com_port, baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)


    initialise_serial.serialPort.write(header)
    initialise_serial.serialPort.write(message)
    initialise_serial.serialPort.write(b'\r')

    print('sent!')

    #serialPort.close()
    

def sendData(data, format, module):
    point_message = struct.pack(format, data)
    header_message = struct.pack('<3s7s3s',b"12", bytes(module, "utf-8"),b"14")
    serialOutputChar("COM4", header_message, point_message)




#initialise_serial.serialinit()

#serialOutputChar("COM4",  struct.pack('<3s7s3s',b"12", b"object",b"14"), struct.pack("<3s", b"123"),)
#time.sleep(0.05)
