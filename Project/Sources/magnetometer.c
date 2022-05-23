#include "magnetometer.h"     
#include "math.h"
#include <hidef.h>
#include "derivative.h"
#include "beep.h"


//idk about *16/pow(2,16)
float returnMagnetometerUnits(int raw_mag){
   return ((float)raw_mag * 16)/pow(2,16);
}


void  scaleMagUnits(MagRaw * read_mag, MagScaled * scaled_mag){
   
   scaled_mag->x = returnMagnetometerUnits(read_mag->x);
   scaled_mag->y = returnMagnetometerUnits(read_mag->y);
   scaled_mag->z = returnMagnetometerUnits(read_mag->z);   

}

void getModulus(MagScaled * values){
  values->mod = sqrt(pow(values->x,2) + pow(values->y,2) + pow(values->z, 2)); 
}

void CalibrateMagnetometer(MagScaled * mag_noise){
  
  int i, error_code;
  MagRaw read_mag;
  MagScaled scaled_mag;
  
  mag_noise->x = 0;
  mag_noise->y = 0;
  mag_noise->z = 0;
  
  DisableInterrupts;
  for(i =0; i <100; i++){
    error_code = getRawDataMagnet(&read_mag);   
  //if (error_code != NO_ERROR) {
    //printErrorCode(error_code);   
         
    //error_code = iicSensorInit();
    //printErrorCode(error_code);
        
  //}
  
    scaleMagUnits(&read_mag, &scaled_mag);
    
    mag_noise->x += scaled_mag.x;
    mag_noise->y += scaled_mag.y;
    mag_noise->z += scaled_mag.z;
    
  }
  
  mag_noise->x /= 100;
  mag_noise->y /= 100;
  mag_noise->z /= 100;
  
  
  EnableInterrupts;
  
  
  
}

void objectBeep(MagScaled * values,MagScaled * mag_noise ){
  int i = 0;
  int length;
  length = sizeof(values)/sizeof(values[0]);
  while (i < length) {
    if (values[i]->mod > mag_noise[i]->mod){
      makeBeep();
      i = i + 150;
    }
    i++;
  }
  
 
  //if data is greater than magnoise + some more
  //beep
  //wait 200 iterations? 
 
  
}





//void detectObject(