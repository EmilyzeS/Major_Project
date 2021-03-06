#include <hidef.h>      /* common defines and macros */
#include <assert.h>
#include "derivative.h"      /* derivative-specific definitions */

// need this for string functions
#include <stdio.h>

#include "pll.h"
#include "simple_serial.h"

#include "l3g4200d.h"

#include "servo.h"
#include "laser.h"

#include "gyro.h"
#include <string.h>
#include "magnetometer.h"
#include "buttons.h"
#include "LCD.h"


#define BUFFER 128
#define SPINCOUNT 4

//Operation Modes
int scan_mode = 0;
int magnet_mode = -1;



void printErrorCode(IIC_ERRORS error_code) {
  char buffer[128];  
  switch (error_code) {
    case NO_ERROR: 
      sprintf(buffer, "IIC: No error\r\n");
      break;
    
    case NO_RESPONSE: 
      sprintf(buffer, "IIC: No response\r\n");
      break;
    
    case NAK_RESPONSE:
      sprintf(buffer, "IIC: No acknowledge\r\n");
      break;
    
    case IIB_CLEAR_TIMEOUT:
      sprintf(buffer, "IIC: Timeout waiting for reply\r\n");
      break;
    
    case IIB_SET_TIMEOUT: 
      sprintf(buffer, "IIC: Timeout not set\r\n");
      break;
    
    case RECEIVE_TIMEOUT:
      sprintf(buffer, "IIC: Received timeout\r\n");
      break;
    
    case IIC_DATA_SIZE_TOO_SMALL:
      sprintf(buffer, "IIC: Data size incorrect\r\n");
      break;

    default:
      sprintf(buffer, "IIC: Unknown error\r\n");
      break;
  }
    
  SerialOutputString(buffer, &SCI1);
}

void main(void) {

  AccelRaw read_accel;
  AccelScaled scaled_accel;
  
  
  //char input[100];

  GyroRaw read_gyro;
  GyroScaled scaled_gyro, gyro_noise;
  MagRaw read_magnet;
  MagScaled scaled_mag, mag_noise;
  
  IIC_ERRORS error_code = NO_ERROR;
  
  char buffer[BUFFER]; 
  float mag_mods[BUFFER];
  int i =0;
    
  int turnCount[1] = {0};
  
  extern char inputs[BUFFER]; 

  
  unsigned long singleSample;
  


  #ifndef SIMULATION_TESTING

  // make sure the board is set to 24MHz
  //  this is needed only when not using the debugger
  PLL_Init();

  // initialise PWM
  PWMinitialise();
  initialiseButtons();

  #endif
  
  // initialise the simple serial
  SerialInitialise(BAUD_9600, &SCI1);

  
    
  

  #ifndef SIMULATION_TESTING
  
  // initialise the sensor suite
  error_code = iicSensorInit();
  
  // write the result of the sensor initialisation to the serial
  if (error_code == NO_ERROR) {
    sprintf(buffer, "NO_ERROR\r\n");
    SerialOutputString(buffer, &SCI1);
  } else {
    sprintf(buffer, "ERROR %d\r\n");
    SerialOutputString(buffer, &SCI1);
  }

  laserInit();
  
  #else
  
  #endif

  Init_TC6();
  //initialise LCD
  displayLCD(" "," ");
  
  //updae LCD and begin calibration
  displayLCD("Calibrating", " ");
  CalibrateGyro(&gyro_noise);
  CalibrateMagnetometer(&mag_noise);
  getModulus(&mag_noise);
  
  //let python know the calibration has been completed
  SendTextMsg("calibrate");
  setServoPose(100, 100);
  displayLCD("Standby"," ");


	EnableInterrupts;
  //COPCTL = 7;
  _DISABLE_COP();
  
  
  
  //calibrateGyro() ;
    
  for(;;) {
  
    // read the raw values
    error_code = getRawDataGyro(&read_gyro);   
    if (error_code != NO_ERROR) {
      printErrorCode(error_code);   
       
      error_code = iicSensorInit();
      printErrorCode(error_code);   
    }
    
    
    error_code = getRawDataMagnet(&read_magnet);
    if (error_code != NO_ERROR) {
      printErrorCode(error_code);   
    
      error_code = iicSensorInit();
      printErrorCode(error_code); 
    }    

    GetLatestLaserSample(&singleSample);
    
    //if searching for objects
    if(scan_mode == 1){
    
      
      ConvertGyro(&read_gyro, &scaled_gyro);
      
      //count the number of times the gyro has been spun
      servoSpinCount(turnCount, scaled_gyro.x, gyro_noise.x);
      
      
      //send info for python mapping
      SendGyroMsg(read_gyro.x, read_gyro.y, read_gyro.z);
      SendLidarMsg(singleSample);
    
    
    //if it has finished mapping
      if(*turnCount > SPINCOUNT){
        scan_mode = 0;

        
        (*turnCount) = 0;
        SendTextMsg("clear");
      }
      
    } 
    
    //stocktake mode
    else if( magnet_mode == 1){
    
     // if(i >= BUFFER){
     //  i =0; 
     // }
      
     // scaleMagUnits(&read_magnet, &scaled_mag);
      
     // mag_mods[i] = scaled_mag.mod;
      
      
      //send magnet message to python
      SendMagMsg(read_magnet.x, read_magnet.y, read_magnet.z);
          
      
     // i++; 
      
       
    }
    
    //poll when  a message has been recieved
    if(!strcmp(inputs, "12")){
     interpretSerial(inputs); 
     inputs[0] = '\0';
     //memset(inputs, 0, BUFFER);
    }
    
    

    
   // sprintf(buffer, "%f\r\n", scaled_gyro.x);
   // SerialOutputString(buffer, &SCI1);
      
      
    //_FEED_COP(); /* feeds the dog */
  } /* loop forever */
  
  /* please make sure that you never leave main */
}

