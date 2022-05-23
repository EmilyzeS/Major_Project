#include <string.h>
#include "derivative.h"
#include "simple_serial.h"
#include <hidef.h>
#include "python_responses.h"

#define HEADER_SENT 26



void detectMsgType(char * msg, struct READ_HEADER * header){

  ObjectLocations locations;

  if(header->sentinel + header->end_sentinel != HEADER_SENT){
    return; 
  }
  
  

  if(!strncmp(header->msg_type,"object",8)){
     
     locations.sentinel = msg[2];
     locations.x = msg[4];
     locations.y = msg[5];
      
     objectDetected(&locations);
  }
}

void objectDetected(ObjectLocations * locations){

  int tog;
  if(56 == 56 ){
    DDRB = 0xFF;
    DDRJ = 0xFF;
    DDRP = 0xFF;
    DDRH = 0xFF;
    PTJ = 0x00;
    
    tog = 0x0F;
    PORTB = PORTB^tog;
  }
}
