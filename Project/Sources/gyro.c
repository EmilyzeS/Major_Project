#include "gyro.h"
#include <hidef.h>      /* common defines and macros */
#include "derivative.h"
#include <math.h>
#include <stdlib.h>
#include "iic.h"
#include "simple_serial.h"
#include "l3g4200d.h"



// y is left to right
// x is up down


float returnGyroUnits(int reading){
  return ((float)reading*250/pow(2,15)); 
}


void ConvertGyro(GyroRaw *read_gyro, GyroScaled *scaled_gyro){
 scaled_gyro->x = returnGyroUnits(read_gyro->x);
 scaled_gyro->y = returnGyroUnits(read_gyro->y);
 scaled_gyro->z = returnGyroUnits(read_gyro->z);
} 


int gyroDirection(float azimuthSpeed, float azimuth_noise){

  //returns 0 if the servo is spinning right and 1 if it is spinning left
  if(azimuthSpeed < -fabs(azimuth_noise)){  //if turning right
    return 0;
  }
  else if (azimuthSpeed > fabs(azimuth_noise)){
    return 1; //if turning left 
  }

  
}


void CalibrateGyro(GyroScaled * gyro_noise){
  
  

  
  int i = 0, error_code;
   
 
  GyroRaw read_gyro;
  GyroScaled scaled_gyro;
  
  gyro_noise->x = 0;
  gyro_noise->y = 0;
  gyro_noise->z = 0;
  
  DisableInterrupts;
  
  SendTextMsg("CalibrateGyros");


  //take average of 100 stationary noise readings
  for(i = 0; i<100; i++){
  
  error_code = getRawDataGyro(&read_gyro);   
  //if (error_code != NO_ERROR) {
    //printErrorCode(error_code);   
         
    //error_code = iicSensorInit();
    //printErrorCode(error_code);
        
  //}
   
  ConvertGyro(&read_gyro, &scaled_gyro );
  
  gyro_noise->x += scaled_gyro.x;
  gyro_noise->y += scaled_gyro.y;
  gyro_noise->z += scaled_gyro.z;
  
  
   
  
  
  //for python to initialise 
  SendGyroMsg(read_gyro.x, read_gyro.y, read_gyro.z);

   
  }
  
  gyro_noise->x /= 100;
  gyro_noise->y /= 100;
  gyro_noise->z /= 100;
  
  
  EnableInterrupts;
  
  

  
  
}