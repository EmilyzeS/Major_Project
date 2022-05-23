import time
import serial
import struct
import traceback
import data_output as do
import map
import read_text
import convertUnits as cu
import calibration as ca


MSG_HEADER_SIZE = 16
MSG_HEADER_SUM = 100487
GYRO_SENT = 4952
ANGLE_SENT = 22136
LIDAR_SENT = 4660
MAG_SENT = 4951
ACCEL_SENT = 9320



def read_packet(f):
    header_bytes = f.read(MSG_HEADER_SIZE)

    if len(header_bytes) < MSG_HEADER_SIZE:
        # must be out of messages
        return False

    header_data = struct.unpack(">H8sHHH", header_bytes)

    #checksum on the header sentinels
    if(header_data[0] + header_data[4] != MSG_HEADER_SUM):
        print("Header Sentinels Do not add up.")
        print(header_data)
        return False

    message_type = header_data[1].split(b'\0', 1)[0]  # remove the null characters from the string
    print(message_type)

    #find what type of message was recieved
    if message_type == b"text":
        text_bytes = f.read(header_data[2])

        read_text.read_string(str(text_bytes))

        print("text message: " + str(text_bytes))

    elif message_type == b"gyro":

        gyro_bytes = f.read(header_data[2])
        gyro_data = struct.unpack(">hhhhH", gyro_bytes)
        
        #check if sentiniel is correct
        if (gyro_data[0] != GYRO_SENT):
            print("Gyro data corrupted")
            return False

        #convert units and write to a csv file
        info = [cu.ConvertGyro(gyro_data[1]), cu.ConvertGyro(gyro_data[2]), cu.ConvertGyro(gyro_data[3]), gyro_data[4]]

        do.write_to_csv('gyro.csv', info)

    elif message_type == b"buttons":
        buttons_bytes = f.read(header_data[2])
        print("buttons message: " + str(hex(buttons_bytes[1])) + ", time=" + str(buttons_bytes[2]))
    
    elif message_type == b"lidar":
        lidar_bytes = f.read(header_data[2])
        lidar_data = struct.unpack(">hIH", lidar_bytes)

        if(lidar_data[0] != LIDAR_SENT):
            print("Lidar data corrupted")
            return False

        #write to a csv file
        info = [lidar_data[1]]

        do.write_to_csv('lidar.csv', info)

    elif message_type == b"magnet":
        magnet_bytes = f.read(header_data[2])
        magnet_data = struct.unpack(">hhhhH", magnet_bytes)

        if(magnet_data[0] != MAG_SENT):
            print("Magnet Data corrupted")
            return False


        info = [magnet_data[1], magnet_data[2], magnet_data[3]]

        do.write_to_csv('mag.csv', info)

    return True


def serialOutputChar(com_port, char):
    serialPort = serial.Serial(port=com_port, baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

    serialPort.write(1)

    print('sent!')

    serialPort.close()

def sendPoint(x, y):
    point_header = struct.pack('< h 6s h', 1234, b"object", 4321)
    point_message = struct.pack('< h h h', 5678, x, y)

    serialOutputChar('COM4', 2)

# main program entry point