#include <hidef.h>      /* common defines and macros */
#include "derivative.h"      /* derivative-specific definitions */
#include <stdlib.h>
#include <string.h>


void easy_delay(unsigned int delayTime);
char getKey(void);
char scanKey(int row);
void cmd2LCD(char cmd);
void openLCD(void);
void putcLCD(char cx);
void putsLCD(char *ptr);
void displayLCD(char string1[], char string2[]);