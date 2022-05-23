import serial
import struct
import sys
import time

def serialOutputChar(com_port, header, message):
    serialPort = serial.Serial(port=com_port, baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

    serialPort.write(header)
    serialPort.write(message)
    serialPort.write(b'\r')

    print('sent!')

    serialPort.close()
    

def sendData(data, format):
    point_message = struct.pack(format, "123", data)
    header_message = struct.pack('<3s7s3s',b"12", b"object",b"14")

#time.sleep(0.05)
