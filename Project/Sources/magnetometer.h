#ifndef MAGNETOMETER_HEADER
#define MAGNETOMETER_HEADER

typedef struct MagRaw {
  int x;
  int y;
  int z;
} MagRaw;

typedef struct MagScaled {
 float x;
 float y;
 float z;
 float mod; 
} MagScaled;







void getModulus(MagScaled * values);



float returnMagnetometerUnits(int raw_mag);

void  scaleMagUnits(MagRaw * read_mag, MagScaled * scaled_mag);

void CalibrateMagnetometer(MagScaled * mag_noise);



#endif