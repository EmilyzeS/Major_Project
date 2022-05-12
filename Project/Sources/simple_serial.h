#ifndef SIMPLE_SERIAL_HEADER
#define SIMPLE_SERIAL_HEADER


// NOTE: these are stored as pointers because they 
//       are const values so we can't store them directly
//       in the struct
typedef struct SerialPort {
  byte *BaudHigh;
  byte *BaudLow;
  byte *ControlRegister1;
  byte *ControlRegister2;
  byte *DataRegister;
  byte *StatusRegister;
} SerialPort;


//
struct MSG_HEADER{
  int sentinel;
  char msg_type[8];
  unsigned int msg_size;
  unsigned int header_time;
  int end_sentinel;
};

//
struct MSG_GYRO{
  int sentinel;
  int rotation_x;
  int rotation_y;
  int rotation_z;
  unsigned int last_sample_time;
};

//
struct MSG_BUTTONS{
  int sentinel;
  unsigned char button_states;
  unsigned int last_press_time;
};

struct MSG_LIDAR{
  int sentinel;
  int laserSample;
  unsigned int last_sample_time;
  
};

struct MSG_ANGLE{
  int sentinel;
  int azimuth;
  int elevation;
  unsigned int time; 
};
 
//used for magnetic reading AND accelerometer
//struct MSG_IMU{
  //int sentinel;
  //int x;
  //int y;
  //int z;
  //int last_sample_time;  
//}



// make two instances of the serial port (they are extern because
//   they are fixed values)
extern SerialPort SCI0, SCI1;


enum {
  BAUD_9600,
  BAUD_19200,
  BAUD_38400,
  BAUD_57600,
  BAUD_115200
};

 
// SerialInitialise - initialise the serial port
// Input: baud rate as defined in the enum
void SerialInitialise(int baudRate, SerialPort *serial_port);
 

// SerialOutputChar - output a char to the serial port
//  note: this version waits until the port is ready (not using interrupts)
// Input: char to be transferred
void SerialOutputChar(char, SerialPort *serial_port);  
 

// SerialOutputString - output a NULL TERMINATED string to the serial port
// Input: pointer to a NULL-TERMINATED string (if not null terminated, there will be problems)
void SerialOutputString(char *pt, SerialPort *serial_port);


// SerialOutputString - output a set of bytes to the serial port
// Input: pointer to a char sized buffer, the size must be correct
void SerialOutputBytes(char *pt, int size, SerialPort *serial_port); 


void SendGyroMsg(int rot_x, int rot_y, int rot_z);
void SendButtonsMsg();
void SendTextMsg(char* text_message); 

void SendLidarMsg(int laser_reading); 
void SendAngleMsg(int azimuth, int elevation);
 
 
#endif