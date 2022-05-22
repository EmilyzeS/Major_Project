#ifndef SERVO_H
#define SERVO_H

#include "gyro.h"


void PWMinitialise(void);

// sets servo in elevation and azimuth
// note: this requires verification and calibration 
void setServoPose(int azimuth, int elevation);


// interrupt used for cycling through the servo positions
__interrupt void TC6_ISR(void);

void Init_TC6 (void);


void servoSpinCount(int * turnCount, float azimuthSpeed, float azimuthNoise);

#endif