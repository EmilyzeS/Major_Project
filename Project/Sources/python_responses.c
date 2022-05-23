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


  //checksum on header sentinels
  if(header->sentinel + header->end_sentinel != HEADER_SENT){
    return; 
  }
  
  
  //if an object message has been recieved
  if(!strncmp(header->msg_type,"object",8)){
     objectDetected(msg);
     
  } 

}

void objectDetected(char * msg){

  int i;

  //look for the start of the message denoted by the char '('
  for(i = 0;i < BUFFER;i++){
   if(msg[i] == '('){
     break;
   }
  }

  //display the location of the found objects
  displayLCD("Objects: ", &msg[i]);

    
    //initialiseTimers();
    //makeBeep();
    //TIOS = disable_timer;
    //TSCR1 = disable_timer;
    //PORTB = 0x00;
    
    //TSCR1_TEN = 1;
}

