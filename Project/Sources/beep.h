#ifndef BEEP_HEADER
#define BEEP_HEADER



#define E6 1138
#define ZZ 20       // delay count to create an inaudible sound
#define toggle 0x04 // value to toggle OC5 pin
#define enable_timer 0x90
#define prescaler_8 0x03
#define output_compare 0x20

int period;
void initialiseTimers();
void makeBeep();

interrupt 13 void speakerISR();



#endif