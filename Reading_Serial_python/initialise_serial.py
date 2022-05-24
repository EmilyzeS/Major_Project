
import serial

def serialinit():
    global serialPort
    serialPort = serial.Serial(port="COM5", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        