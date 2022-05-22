
#include "derivative.h"
#include <math.h> 
#include "servo.h"
#include "gyro.h"


#define ZERO_ELEVATION_DUTY 4600
#define ZERO_AZIMUTH_DUTY 2000

// variables to make the servo move back and forth
volatile long pan_iterator = 0;
volatile int pan_toggle = 0;
volatile int tilt_toggle = 0;
volatile long tilt_iterator = 0;

extern int scan_mode;



void servoSpinCount(int * turnCount, float azimuthSpeed, float azimuth_noise){

  //negative values mean its turning right
  //Starts by turning right, so every even turnCount value checks if it is coming
  //back
  if((*turnCount) % 2 == 0  && !gyroDirection(azimuthSpeed, azimuth_noise)){
    (*turnCount)++; 
  } 
  else if((*turnCount) %2 == 1 && gyroDirection(azimuthSpeed, azimuth_noise)){
    (*turnCount)++;
  }
  
}


void PWMinitialise(void){
    // set PP5 and PP7 for pwm output 
    PWMCLK = 0; // select clock A
    PWMPOL = 0xA0; // PWM5 and PWM7 output start high
    PWMCTL = 0xC0; // 16-bit PWM: use PWM4 and PWM5 for PWM5, PWM6 and PWM7 for PWM7
    PWMCAE = 0; // Center aligned
    PWMPRCLK = 0x33; // PWM Clock prescaler to 8 

    // set the PWM period appropriate for servos
    PWMPER45 = 0xEA6A;
    PWMPER67 = 0xEA6A;

    // set the initial duty cycle for both servos
    PWMDTY45 = ZERO_ELEVATION_DUTY;
    PWMDTY67 = ZERO_AZIMUTH_DUTY;
    
    PWME  |= 0xFF;      // enable PWM0
}

void setServoPose(int azimuth, int elevation){  
    PWMDTY45 = (int)(ZERO_ELEVATION_DUTY + elevation);  // Sets elevation to duty cycle using PWM 45
    PWMDTY67 = (int)(ZERO_AZIMUTH_DUTY + azimuth);   // Sets azimuth to duty cycle using PWM 67
}


void Init_TC6 (void) {
  TSCR1_TEN = 1;
  
  TSCR2 = 0x00;   // prescaler 1, before 32 = 0x04
  TIOS_IOS6 = 1;   // set channel 6 to output compare
    
  TCTL1_OL6 = 1;    // Output mode for ch6
  TIE_C6I = 1;   // enable interrupt for channel 6

  TFLG1 |= TFLG1_C6F_MASK;
}







// the interrupt for timer 6 which is used for cycling the servo
#pragma CODE_SEG __NEAR_SEG NON_BANKED /* Interrupt section for this module. Placement will be in NON_BANKED area. */
__interrupt void TC6_ISR(void) { 

   
  TC6 = TCNT + 64000;   // interrupt delay depends on the prescaler
  TFLG1 |= TFLG1_C6F_MASK;
  
  if(scan_mode == 0){
    pan_iterator = 0;
    pan_toggle = 0;
    tilt_toggle = 0;
    tilt_iterator = 0; 
    return;   
  }
  

  if (pan_toggle == 0)
    pan_iterator++;
  else
    pan_iterator--;
                                                                
  if (pan_iterator > 2100) {
    pan_toggle = 1;
  } else if (pan_iterator < -100) {
    pan_toggle = 0;
  }
  
  if(tilt_toggle == 0)
   tilt_iterator += 3; 
  else
   tilt_iterator -= 3;
  
  if(tilt_iterator > 315){
   tilt_toggle = 1; 
  } else if(tilt_iterator < -200){
   tilt_toggle = 0; 
  }
  
  

  setServoPose(50 + pan_iterator, 50 + tilt_iterator);

        
}

