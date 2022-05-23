#include "LCD.h"
#include <hidef.h>      /* common defines and macros */
#include "derivative.h"      /* derivative-specific definitions */
#include <stdlib.h>
#include <string.h>

void easy_delay(unsigned int delayTime) 
{
  int i;
  int j;
  for (i = 0; i < delayTime; i++) 
  {
    for (j = 0; j < 4000; j++) 
    {
      // do nothing
    }
  }
}

char scanKey(int row)
{
    unsigned char lookUpRows[4] = {0x10, 0x20, 0x40, 0x80};
    unsigned char keypad[4][4] = {{49, 50, 51, 65}, 
                                 {52, 53, 54, 66}, 
                                 {55, 56, 57, 67}, 
                                 {42, 48, 35, 68}};

    PORTA = lookUpRows[row];

    if (PORTA & 0x01)
    {
        return keypad[row][0];
    }
    
    else if (PORTA & 0x02)
    {
        return keypad[row][1];
    }
    else if (PORTA & 0x04)
    {
        return keypad[row][2];
    }
    else if (PORTA & 0x08)
    {
        return keypad[row][3];
    }

    return '\0';
}


char getKey(void)
{
    char key;
    int row;

    // set lower 4 bits to input
    DDRA = 0xF0;

    // always check for input
    while(1)
    {
        // go through each row of keypaf
        for (row = 0; row < 4; row++)
        {
            // get the character representation
            key = scanKey(row);
            if (key)
            {
                easy_delay(400);
                if (key == scanKey(row))
                {
                    return key;
                }
            }
        }
    }
}


void cmd2LCD(char cmd)
{
    // variable to send four bits of data at a time
    char fourBits;
    
    // PK0 and PK1 = 0. E and RS = 0. Select instruction register
    PORTK = 0x00;

    // get the upper four bits
    fourBits = cmd & 0xF0; 
    
    // shift to match LCD data pins
    fourBits >>=2; 
    
    // output the upper 4 bits by pulling E to high
    PORTK = fourBits | 0x02;

    // select to write to instruction register and disable LCD
    PORTK = 0x00;

    // set the remaining four bits
    fourBits = cmd & 0x0F;
    PORTK = 0x02;
    fourBits <<=2;
    PORTK = fourBits | 0x02;

    // select to write to instruction register and disable LCD
    PORTK = 0x00;

    easy_delay(10);
}

// initializes the LCD
void openLCD(void)
{
    // Set LCD to output
    DDRK = 0xFF;
    easy_delay(100);
    
    // sets 4-bit data, 2-line display, 5x7 font
    cmd2LCD(0x28);
    
    // turns on display and places a blinking cursor 
    cmd2LCD(0x0F);
    
    // moves cursor to the right
    cmd2LCD(0x06);
    
    cmd2LCD(0x80);
    
    // clears screen and moves cursor to home
    cmd2LCD(0x01);
    easy_delay(2);
}

// outputs a character to LCD
void putcLCD(char cx)
{
    char fourBits;
    
    // select data register
    PORTK = 0x01;    
    
    // get the upper four first
    fourBits = cx&0xF0;
    
    // shift bits to match LCD pins
    fourBits >>= 2;
    
    // output the upper four bits
    PORTK = fourBits|0x03;

    // pull E to low
    PORTK = 0x01;
    
    // send the remaining four bits
    fourBits = cx & 0x0F;
    PORTK = 0x03;
    fourBits <<=2;
    PORTK = fourBits|0x03;
    
    PORTK = 0x01;
    easy_delay(1);
    
}

// outputs a string to LCD
void putsLCD(char *ptr)
{
    while (*ptr)
    {
        putcLCD(*ptr);
        ptr++;
    }
}

void displayLCD(char string1[], char string2[]){
  openLCD();
  cmd2LCD(0x0C);
  putsLCD(string1);
  cmd2LCD(0xC0);
  putsLCD(string2);
  cmd2LCD(0x02);
}

void reverseString(char str[], int len){
    int i, j, start, end;
    char temp;
      
      for(start=0, end=len-1; start < end; start++, end--) {
        temp = *(str+start);
        *(str+start) = *(str+end);
        *(str+end) = temp;
      }

}

char* itoa(int num, char *str, int base){
    int i = 0;
    int rem;
  
    if (num == 0) {
        str[i] = '0';
        str[i + 1] = '\0';
        return str;
    }  
    
    while (num != 0) {
          rem = num % base;
          str[i++] = (rem > 9)? (rem-10) + 'A' : rem + '0';
          num = num/base;
    }
    
    while (i <= 2){
      str[i] = '0';
      i++;
    }
  
    str[i] = '\0';   
 
    reverseString(str, i);
  
    return str;
}





