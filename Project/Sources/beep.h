#ifndef BEEP_HEADER
#define BEEP_HEADER




#define E6 10000
#define ZZ 0       // delay count to create an inaudible sound
#define toggle 0x04 // value to toggle OC5 pin
#define enable_timer 0x90
#define disable_timer 0x00
#define prescaler_8 0x03
#define output_compare 0x20




void delay(unsigned int time);
void initialiseTimers();
void makeBeep();

__interrupt void speakerISR();



#endif
