#include <string.h>
#include "derivative.h"
#include "simple_serial.h"
#include <hidef.h>

void objectDetected(char * objectLocation){

  int tog;
  if(objectLocation[0] == '8' ){
    DDRB = 0xFF;
    DDRJ = 0xFF;
    DDRP = 0xFF;
    DDRH = 0xFF;
    PTJ = 0x00;
    
    tog = 0x0F;
    PORTB = PORTB^tog;
  }
}
