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


//char inputs[128];


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
  GyroScaled scaled_gyro;
  MagRaw read_magnet;
  
  IIC_ERRORS error_code = NO_ERROR;
  
  char buffer[128]; 
    
  int checkClear =0;

  
  unsigned long singleSample;
  
  //calibrate servos
  
 // float xyz[3];

  
  //assert(error_code != NO_ERROR);

  #ifndef SIMULATION_TESTING

  // make sure the board is set to 24MHz
  //  this is needed only when not using the debugger
  PLL_Init();

  // initialise PWM
  PWMinitialise();
  setServoPose(100, 100);

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

	EnableInterrupts;
  //COPCTL = 7;
  _DISABLE_COP();
  
  //CalibrateGyro() ;
    
  for(;;) {
  
    // read the raw values
    error_code = getRawDataGyro(&read_gyro);   
    if (error_code != NO_ERROR) {
      printErrorCode(error_code);   
       
      error_code = iicSensorInit();
      printErrorCode(error_code);   
    }
    
    error_code = getRawDataAccel(&read_accel);
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
    
    
    //IMPLEMENT ERROR CODE for lidar?  

    //ConvertGyro(&read_gyro, &scaled_gyro);

    SendGyroMsg(read_gyro.x, read_gyro.y, read_gyro.z);
    SendLidarMsg(singleSample);
   // SendAngleMsg(PWMDTY67, PWMDTY45);
    //SendMagMsg(read_magnet.x, read_magnet.y, read_magnet.z);
    
    if((checkClear %2 == 0) && CheckGyroClear(&read_gyro)){
      checkClear += 1;
    }
    if((checkClear %2 == 1) && !CheckGyroClear(&read_gyro)){
      checkClear += 1; 
    }
    
    if(checkClear >= 3*2-1){
      
      checkClear = 0;
      setServoPose(100,100);
      
      SendTextMsg("clear");
       
    }

    
    
    //_FEED_COP(); /* feeds the dog */
  } /* loop forever */
  
  /* please make sure that you never leave main */
}

