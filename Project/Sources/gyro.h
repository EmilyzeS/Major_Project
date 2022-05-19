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

void CalibrateGyro();


// NOTE: some function is required to convert between raw and 
//       scaled values. Also, calibration and removing the bias is
//       needed


int CheckGyroClear(GyroRaw * read_gyro);


#endif