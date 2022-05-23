#ifndef GYRO_HEADER
#define GYRO_HEADER

typedef struct GyroRaw {
  int x;
  int y;
  int z;
} GyroRaw;

typedef struct GyroScaled {
  float x;
  float y;
  float z;
} GyroScaled;

void ConvertGyro(GyroRaw * read_gyro, GyroScaled * scaled_gyro);

void CalibrateGyro(GyroScaled * gyro_noise);
float returnGyroUnits(int reading);



int gyroDirection(float azimuthSpeed, float gyro_noise);


#endif