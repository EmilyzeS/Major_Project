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
// 


void ConvertGyro(GyroRaw *read_gyro, GyroScaled *scaled_gyro){
 scaled_gyro->x = (float)(read_gyro)->x*250/pow(2,15);
 scaled_gyro->y = (float)(read_gyro)->y*250/pow(2,15);
 scaled_gyro->z = (float)(read_gyro)->z*250/pow(2,15);
} 


int CheckGyroClear(GyroRaw * read_gyro){

  GyroScaled scaled_gyro;
  
  
  ConvertGyro(read_gyro, &scaled_gyro);
  
  if(scaled_gyro.x < 0){ 
    return 0;
  }
  else{
    return 1; 
  }

  
}

void CalibrateGyro(){
  
  

  
  int i = 0, error_code;
   
 
  GyroRaw read_gyro;
  //GyroScaled scaled_gyro;                
  
  DisableInterrupts;

  for(i = 0; i<100; i++){
  
   error_code = getRawDataGyro(&read_gyro);   
  // if (error_code != NO_ERROR) {
    // printErrorCode(error_code);   
         
     //error_code = iicSensorInit();
     //printErrorCode(error_code);
        
   //}
   
   
   
   SendGyroMsg(read_gyro.x, read_gyro.y, read_gyro.z);

   
  }
  
  EnableInterrupts;
  
  

  
  
}