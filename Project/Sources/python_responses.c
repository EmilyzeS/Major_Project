#include <string.h>
#include "derivative.h"
#include "simple_serial.h"
#include <hidef.h>
#include "python_responses.h"
#include "beep.h"

#define HEADER_SENT 26
#define BUFFER 128

#include "LCD.h"

void detectMsgType(char * msg, struct READ_HEADER * header){

  //ObjectLocations locations;

  if(header->sentinel + header->end_sentinel != HEADER_SENT){
    return; 
  }
  
  

  if(!strncmp(header->msg_type,"object",8)){
     
     //locations.sentinel = msg[2];
     //locations.x = msg[4];
     //locations.y = msg[5];
      
     objectDetected(msg);
  }
}

void objectDetected(char * msg){

  int i;

  for(i = 0;i < BUFFER;i++){
   if(msg[i] == '('){
     break;
   }
  }

  displayLCD("Objects: ", &msg[i]);
  delay(100);
    
    //initialiseTimers();
    //makeBeep();
    //TIOS = disable_timer;
    //TSCR1 = disable_timer;
    //PORTB = 0x00;
    
    //TSCR1_TEN = 1;
}
