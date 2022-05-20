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
    
 
point_message = struct.pack('< h h h', 56, 1, 2)

header_message = struct.pack('<h6sh',12,b"object",14)


while True:
    serialOutputChar('COM4', header_message, point_message)
    
    #time.sleep(0.05)
