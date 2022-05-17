# This is a Python script to parse the example messages from a file.
import time
import serial
import struct
import traceback
import data_output as do
import map
import read_text

MSG_HEADER_SIZE = 16
MSG_HEADER_SUM = 100487
GYRO_SENT = 39030
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

        #write to a csv file
        info = [gyro_data[1], gyro_data[2], gyro_data[3]]

        do.write_to_csv('gyro.csv', info)

    elif message_type == b"buttons":
        buttons_bytes = f.read(header_data[2])
        print("buttons message: " + str(hex(buttons_bytes[1])) + ", time=" + str(buttons_bytes[2]))
    elif message_type == b"angle":


        #unpack
        angle_bytes = f.read(header_data[2])
        angle_data = struct.unpack(">hhhH", angle_bytes)

        #check sentinel
        if(angle_data[0] != ANGLE_SENT):
            print("Angle data corrupted")
            return False

        #write to a csv file
        info = [int(angle_data[1]), angle_data[2]]

        do.write_to_csv('angledata.csv', info)


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

    elif message_type == b"accel":
        accel_bytes = f.read(header_data[2])
        accel_data = struct.unpack(">hefH", accel_bytes)

        if(accel_data[0] != ACCEL_SENT):
            print("Acceleration Data corrupted")
            return False


        info = [accel_data[1], accel_data[2], accel_data[3]]

        do.write_to_csv('accel.csv', info)       



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

        #checks if one revolution has been made
        do.check_if_clear_ready('angledata.csv')



# main program entry point
if __name__ == '__main__':

    #clear files
    do.clear_file('angledata.csv')
    do.clear_file('lidar.csv')
    
    while(1):
        read_serial("COM4")
