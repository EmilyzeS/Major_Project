#include "math.h"
#include <hidef.h>
#include "derivative.h"
#include "beep.h"



void initialiseTimers() {
    // Enable timer and fast flag clear
  	TSCR1 = enable_timer; 
    // Set prescaler to 8
    TSCR2 = prescaler_8;
    // Choose output compare for channel 5
    TIOS = output_compare;
    // Toggle upon successful output compare 
    TIE = output_compare; 
}



#pragma CODE_SEG __NEAR_SEG NON_BANKED
__interrupt void speakerISR(){
  
	TC5 = TC5 + period;
	
}


void makeBeep(){
  int x = 0;
  int length = 2;

	
  unsigned int beep[] = {E6,ZZ};
  unsigned int beep_dur[] = {1000,100};
                                

  //initialise timer for sound playing
  TCTL1 = toggle;
  TC5 = TCNT;
 

  while(x < length) {
      		period = beep[x];
      	  delay(beep[x]);
      		x++;
  }

}

