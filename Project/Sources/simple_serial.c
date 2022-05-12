#include <mc9s12dp256.h>        /* derivative information */

#include "simple_serial.h"
#include <hidef.h>
#include <stdio.h> 
#include <string.h>

// instantiate the serial port parameters
//   note: the complexity is hidden in the c file
SerialPort SCI1 = {&SCI1BDH, &SCI1BDL, &SCI1CR1, &SCI1CR2, &SCI1DRL, &SCI1SR1};
SerialPort SCI0 = {&SCI0BDH, &SCI0BDL, &SCI0CR1, &SCI0CR2, &SCI0DRL, &SCI0SR1};



// InitialiseSerial - Initialise the serial port SCI1
// Input: baudRate is tha baud rate in bits/sec
void SerialInitialise(int baudRate, SerialPort *serial_port) {
  
  // Baud rate calculation from datasheet
  switch(baudRate){
	case BAUD_9600:
      *(serial_port->BaudHigh)=0;
      *(serial_port->BaudLow)=156;
	  break;
	case BAUD_19200:
      *(serial_port->BaudHigh)=0;
      *(serial_port->BaudLow)=78;
	  break;
	case BAUD_38400:
      *(serial_port->BaudHigh)=0;
      *(serial_port->BaudLow)=39;
	  break;
	case BAUD_57600:
      *(serial_port->BaudHigh)=0;
      *(serial_port->BaudLow)=26;
	  break;
	case BAUD_115200:
      *(serial_port->BaudHigh)=0;
      *(serial_port->BaudLow)=13;
	  break;
  }
  
  *(serial_port->ControlRegister2) = SCI1CR2_RE_MASK | SCI1CR2_TE_MASK;
  *(serial_port->ControlRegister1) = 0x00;
}
    
        
void SerialOutputChar(char data, SerialPort *serial_port) {  
  while((*(serial_port->StatusRegister) & SCI1SR1_TDRE_MASK) == 0){
  }
  
  *(serial_port->DataRegister) = data;
}



void SerialOutputString(char *pt, SerialPort *serial_port) {
  while(*pt) {
    SerialOutputChar(*pt, serial_port);
    pt++;
  }            
}

void SerialOutputBytes(char *pt, int size, SerialPort *serial_port) {
  while(size > 0) {
    SerialOutputChar(*pt, serial_port);
    pt++;
    size--;
  }            
}

void SendAngleMsg(int azimuth, int elevation){
  struct MSG_HEADER angle_header = {0xABCD, "angle", 0, 0, 0xDCBA};
  struct MSG_ANGLE angle_message = {0x5678, 0, 0, 0};
  
  angle_header.msg_size = sizeof(struct MSG_ANGLE);
  angle_header.header_time = TCNT;
  
  angle_message.azimuth = azimuth;
  angle_message.elevation = elevation;
  angle_message.time = TCNT;
  
  SerialOutputBytes((char*)&angle_header, sizeof(struct MSG_HEADER), &SCI1);
  SerialOutputBytes((char*)&angle_message, sizeof(struct MSG_ANGLE), &SCI1);  
}



void SendGyroMsg(int rot_x, int rot_y, int rot_z) {
  struct MSG_HEADER gyro_header = {0xABCD, "gyro", 0, 0, 0xDCBA};
  struct MSG_GYRO gyro_message = {0x9876, 0, 0, 0, 0};
                             
  gyro_header.msg_size = sizeof(struct MSG_GYRO);
  
  
  gyro_header.header_time = TCNT;
  
  gyro_message.last_sample_time = TCNT;
  gyro_message.rotation_x = rot_x;
  gyro_message.rotation_y = rot_y;
  gyro_message.rotation_z = rot_z;
  
  SerialOutputBytes((char*)&gyro_header, sizeof(struct MSG_HEADER), &SCI1);  
  SerialOutputBytes((char*)&gyro_message, sizeof(struct MSG_GYRO), &SCI1); 
}

void SendLidarMSG(int laser_reading){
  struct MSG_HEADER laser_header = {0xABCD, "lidar", 0, 0, 0xDCBA};
  struct MSG_LIDAR laser_message = {0x1234, 0,0};
  
  laser_header.msg_size = sizeof(struct MSG_LIDAR);
  laser_header.header_time = TCNT;
  
  
  laser_message.last_sample_time = TCNT;
  laser_message.laserSample = laser_reading;
  
  SerialOutputBytes((char*)&laser_header, sizeof(struct MSG_HEADER), &SCI1);
  SerialOutputBytes((char*)&laser_message, sizeof(struct MSG_LIDAR), &SCI1);
}

void SendButtonsMsg() {
  struct MSG_HEADER button_header = {0xABCD, "buttons", 0, 0, 0xDCBA};
  struct MSG_BUTTONS button_message = {0x4321, 0x0A, 0};
                             
  button_header.msg_size = sizeof(struct MSG_BUTTONS);
  button_header.header_time = TCNT;
  
  button_message.last_press_time = TCNT;
  
  SerialOutputBytes((char*)&button_header, sizeof(struct MSG_HEADER), &SCI1);  
  SerialOutputBytes((char*)&button_message, sizeof(struct MSG_BUTTONS), &SCI1);   
}


void SendTextMsg(char* text_message) {
  struct MSG_HEADER text_header = {0xABCD, "text", 0, 0, 0xDCBA};
  text_header.msg_size = strlen(text_message);
  text_header.header_time = TCNT;
  
  SerialOutputBytes((char*)&text_header, sizeof(struct MSG_HEADER), &SCI1);  
  SerialOutputBytes(text_message, text_header.msg_size, &SCI1);
}


