#include "derivative.h"
#include "servo.h"
#include <hidef.h>
#include "buttons.h"
#include "simple_serial.h"
#include "LCD.h"

extern int iterator_counter;
extern long tilt_iterator;


void initialiseButtons(){
  DDRH = 0x00;
  PIEH = 0xFF;
  //PIFH = 0xFF;
  
}

#pragma CODE_SEG __NEAR_SEG NON_BANKED
__interrupt void detectMode(void){
   
   extern int scan_mode;
   extern int magnet_mode;
   
   if(PTH == PTH_PTH0_MASK ){
      scan_mode = 1;
      displayLCD("Detecting", " ");
   } 
   else if(PTH == PTH_PTH1_MASK){
      magnet_mode *= -1;
   
      if(magnet_mode == -1){
       displayLCD("Standby", " ");
       SendTextMsg("MagClr"); 
      } 
      else {
         displayLCD("Classifying", " ");
      }
   }

   
   PIFH = 0xFF;

}