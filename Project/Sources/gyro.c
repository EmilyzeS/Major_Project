#include "gyro.h"
#include <hidef.h>      /* common defines and macros */
#include "derivative.h"
#include <math.h>
#include <stdlib.h>
#include "iic.h"


// y is left to right
// x is up down
// 


void ConvertGyro(GyroRaw *read_gyro, GyroScaled *scaled_gyro){
 scaled_gyro->x = (float)(read_gyro)->x*250/pow(2,15);
 scaled_gyro->y = (float)(read_gyro)->y*250/pow(2,15);
 scaled_gyro->z = (float)(read_gyro)->z*250/pow(2,15);
} 


void CalibrateGyro(float * xyz){
 
 
  
  int i, error_code;
   
 
  GyroRaw read_gyro;
  GyroScaled scaled_gyro;                
  

  for(i = 0; i<100; i++){
  
   error_code = getRawDataGyro(&read_gyro);   
   if (error_code != NO_ERROR) {
     printErrorCode(error_code);   
         
     error_code = iicSensorInit();
     printErrorCode(error_code);
        
   }
   
   
   
   ConvertGyro(&read_gyro, &scaled_gyro);
   
   xyz[0] += scaled_gyro.x;
   xyz[1] += scaled_gyro.y;
   xyz[2] += scaled_gyro.z;
   
  }
  
  for(i = 0; i <3; i++){ 
    xyz[i] /=100;
  }

  
  
}