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

  //checksum on header
  if(header->sentinel + header->end_sentinel != HEADER_SENT){
    return; 
  }
  
  
  //if an object was detected
  if(!strncmp(header->msg_type,"object",8)){
     objectDetected(msg);
     
  } 

}

void objectDetected(char * msg){

  int i;

//find the start of the message denoted by '('
  for(i = 0;i < BUFFER;i++){
   if(msg[i] == '('){
     break;
   }
  }

//display sent message
  displayLCD("Objects: ", &msg[i]);
 


}

