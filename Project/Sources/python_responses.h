#ifndef PYTHON_RESPONSES_HEADER
#define PYTHON_RESPONSES_HEADER


#include "simple_serial.h"
#include "LCD.h"

typedef struct ObjectLocations{
  int sentinel;
  int x;
  int y;
  int z;
}ObjectLocations;;

void detectMsgType(char * msg, struct READ_HEADER * header);

void objectDetected(char * msg);


#endif