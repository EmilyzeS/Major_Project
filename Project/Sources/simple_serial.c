       /* derivative information */
#include "derivative.h"
#include "simple_serial.h"
#include <hidef.h>
#include <stdio.h> 
#include <string.h>
#include "python_responses.h"
#include <stdlib.h>



#include "servo.h"


#define BUFFER 128

#define CARRAIGE_RETURN 0x0D
 

int j = 0;
char inputs[BUFFER];


// instantiate the serial port parameters
//   note: the complexity is hidden in the c file
SerialPort SCI1 = {&SCI1BDH, &SCI1BDL, &SCI1CR1, &SCI1CR2, &SCI1DRL, &SCI1SR1};
//SerialPort SCI0 = {&SCI0BDH, &SCI0BDL, &SCI0CR1, &SCI0CR2, &SCI0DRL, &SCI0SR1};



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
  
  //enable read and write
  *(serial_port->ControlRegister2) = 0x2C;
  *(serial_port->ControlRegister1) = 0x00;
}
    
//SCI1CR2_RE_MASK | SCI1CR2_TE_MASK | SCI1CR2_SCTIE_MASK
        
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



// void SendAccelMsg(int x, int y, int z) {
//   struct MSG_HEADER accel_header = {0xABCD, "accel", 0, 0, 0xDCBA};
//   struct MSG_ACCEL accel_message = {0x2468, 0, 0, 0, 0};
                             
//   accel_header.msg_size = sizeof(struct MSG_MAG);
  
  
//   accel_header.header_time = TCNT;
  
//   accel_message.time = TCNT;
//   accel_message.x = x;
//   accel_message.y = y;
//   accel_message.z = z;
  
//   SerialOutputBytes((char*)&accel_header, sizeof(struct MSG_HEADER), &SCI1);  
//   SerialOutputBytes((char*)&accel_message, sizeof(struct MSG_ACCEL), &SCI1); 
// }

void SendMagMsg(int x, int y, int z) {


  struct MSG_HEADER magnet_header = {0xABCD, "magnet", 0, 0, 0xDCBA};
  struct MSG_MAG magnet_message = {0x1357, 0, 0, 0, 0};
                             
                             
                             
  magnet_header.msg_size = sizeof(struct MSG_MAG);
  
  
  magnet_header.header_time = TCNT;
  
  magnet_message.time = TCNT;
  magnet_message.x = x;
  magnet_message.y = y;
  magnet_message.z = z;

  //disable interrupts because if scanning mode is suddenly exited data will be corrupted 
  DisableInterrupts;
  SerialOutputBytes((char*)&magnet_header, sizeof(struct MSG_HEADER), &SCI1);  
  SerialOutputBytes((char*)&magnet_message, sizeof(struct MSG_MAG), &SCI1);
  EnableInterrupts; 
}


void SendGyroMsg(int rot_x, int rot_y, int rot_z) {

  struct MSG_HEADER gyro_header = {0xABCD, "gyro", 0, 0, 0xDCBA};
  struct MSG_GYRO gyro_message = {0x1358, 0, 0, 0, 0};
                             
  gyro_header.msg_size = sizeof(struct MSG_GYRO);
  
  
  gyro_header.header_time = TCNT;
  
  gyro_message.last_sample_time = TCNT;
  gyro_message.rotation_x = rot_x;
  gyro_message.rotation_y = rot_y;
  gyro_message.rotation_z = rot_z;
  
  SerialOutputBytes((char*)&gyro_header, sizeof(struct MSG_HEADER), &SCI1);  
  SerialOutputBytes((char*)&gyro_message, sizeof(struct MSG_GYRO), &SCI1); 
}

void SendLidarMsg(unsigned long laser_reading){
  struct MSG_HEADER laser_header = {0xABCD, "lidar", 0, 0, 0xDCBA};
  struct MSG_LIDAR laser_message = {0x1234, 0,0};
  
  laser_header.msg_size = sizeof(struct MSG_LIDAR);
  laser_header.header_time = TCNT;
  
  
  laser_message.last_sample_time = TCNT;
  laser_message.laserSample = laser_reading;
  
  SerialOutputBytes((char*)&laser_header, sizeof(struct MSG_HEADER), &SCI1);
  SerialOutputBytes((char*)&laser_message, sizeof(struct MSG_LIDAR), &SCI1);
}



void SendTextMsg(char* text_message) {

  struct MSG_HEADER text_header = {0xABCD, "text", 0, 0, 0xDCBA};
  text_header.msg_size = strlen(text_message);
  text_header.header_time = TCNT;
  
  SerialOutputBytes((char*)&text_header, sizeof(struct MSG_HEADER), &SCI1);  
  SerialOutputBytes(text_message, text_header.msg_size, &SCI1);
}



void interpretSerial(char * buffer){
  
  struct READ_HEADER MsgHeader;
  char msg[3][8];
  int i = 0, numberElements = 0, start = 0, end;
  
  //loop through the entire array recieved 
  for(i = 0; i < BUFFER; i++){
  
    
    //the message is padded by zeros, look for these zeros and then decipher the message
     if(buffer[i] == 0){
        end = i;
        
        //copy the info into a matrix of strings
        strncpy(msg[numberElements], &buffer[start], end-start);
        
        //add the null terminator
        msg[numberElements][end-start] = '\0';
        
        
                
        start = i +1;
        
        numberElements++;
     }
     
     if(numberElements >= 3){
        break;
     }
    
     
  }
  
  //delegate the information into the appropriate struct
  MsgHeader.sentinel = atoi(msg[0]);
  //to prevent overflow only copy 8 digits
  strncpy(MsgHeader.msg_type, msg[1], 8);
  MsgHeader.end_sentinel = atoi(msg[2]);
  
  

  
  //detectMsgType(&buffer[11], &MsgHeader);



}


int SerialRead(SerialPort *serial_port, char* buffer, int j) {


  // Check if data is received by reading the RDRF flag
  if (*(serial_port->StatusRegister) && 0x20) {
  
  
  //looking for carriage return (end of data) or if the input buffer will overflow
    if (*(serial_port->DataRegister) == CARRAIGE_RETURN) {
        return 0;
    } 
    else if(j >= BUFFER){//making sure no overflow 
        return 0; 
    }
    else{
        buffer[j] = *(serial_port->DataRegister);
        j ++;
        return j;
    }
  }
  
    
}

//interrupt for message recieved
#pragma CODE_SEG __NEAR_SEG NON_BANKED /* Interrupt section for this module. Placement will be in NON_BANKED area. */
__interrupt void Serial1ISR(void) {
  j = SerialRead(&SCI1, inputs, j);
}

