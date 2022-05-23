# Major_Project
# Problem statement
In a supermarket, a large proportion of manual labor is spent on organising goods to be sent to shelves. Whether being unloaded off a truck or returned by customers, these goods need to be organised into categories based on the aisle they belong to. This normally requires staff to manually unpack and sought the delivery, and is therefore a financial burden on the supermarket. Our goal is to eliminate the staffing requirements of this stage.

Furthermore, stocktaking and keeping track of stock arrival is a common problem within supermarkets. Receiving an incorrect amount of goods is costly to a supermarket and will impact the stock recordings of the supermarket. Therefore we will attempt to ensure that we count each good that arrives and check if there is any disparity with the order, whilst updating the stock on hand accordingly.

# Project description
The system designed will be placed in a 2x2 bay where objects are placed upon arrival into the warehouse. The object can be thrown haphazardly into the bay to assist in unloading the truck as quickly as possible. Once there, the machine will routinely map the bay and detect objects that have been added. After calculating their location relative to the bay, the machine would theoretically position a robotic arm to reach for the object and move it to a conveyor belt.

Once on the conveyor belt, the objects are passed over a magnetometer at a constant pace and distance. The magnetometer reads the magnetic strength of a unique magnet which is pre-placed on the object (like a barcode). In doing so, the object is classified and the contents are recorded in a database. 

This system should allow for significant time saved when unloading goods and organising them based on their in-store location. Furthermore, it allows the supermarket to audit every single delivery it receives, ensuring they are being sent all the goods they ordered.

The system can be split into 2 key functions, the mapping/object detection module utilising the lidar and gyroscope, and the object classification/stock audit module using the magnetometer.

# Modules


## Lidar and gyroscope data collection
The purpose of this module is to use the Lidar and IMU to take a snapshot of the 2x2 bay where parcels are placed when the object detection module is being operated. This data can then be sent via serial to python, which does mapping and object detection from this data. The Lidar scans a 70 degree azimuth by 20 degree elevation to provide a 3D snapshot of the environment. Our program calculates the time length between a rising edge and falling edge, and that data is later converted in our mapping module to a distance. For each corresponding time period, the program records the gyroscope data to provide the angular velocity in the x,y and z axis in degrees/second, and the time of the recording. This data is then sent to python using the serial interface. The data is constantly collected as the system operates, and every 2 cycles, it signals to the python program to do mapping and object detection on that data. This module inputs raw Lidar and gyroscope data, and outputs the angular velocity and lidar data recorded at small discrete time periods to the serial transfer module.

## Magnetic data collection
This component uses the magnetometer in the IMU to collect data on the change in magnetic field when the stock counting module is being run. It records and scales the x,y and z components of the magnetic field at small discrete time intervals to present an almost continuous recording. This data is then sent at the conclusion of the stocktake via serial to python where objects of different magnetic strengths are detected and counted. This data inputs raw magnetic data and outputs the x,y,z magnetic data to the serial transfer module.



## Mapping and object detection
This module takes in the lidar and angular velocity data in csv form and produces a 3d map of the scanned area. It first converts the lidar readings to distance values, removes the offset error for gyroscope values found in the calibration and performs manual integration on the angular velocity data to calculate the azimuth and elevation at each Lidar data point. It then uses trigonometry to convert the azimuth, elevation and distance recordings into an x,y,z coordinate for each data point. The program will then plot this in a 3D map to provide a visual verification of the setting to the user.
The program will then run a density-based spatial clustering algorithm using the x,y coordinates to find the number of objects in the scanned area and filter out the noise, and then performs a Kmeans search to find the centroid of each object. The module will then output the x,y coordinates of each object for the robotic arm to then collect them, and to the dragonboard to display on the LCD’s.


## Gyro calibration
This module reads the input stationary gyroscope values of the IMU and averages them over a certain period. It then outputs the error from zero for the x and y axis values, which the mapping and object detection module then use to debias the future readings.



## Serial transfer from codewarrior to python
This module is responsible for transferring the raw data from the LIDAR, and the gyroscope and magnetometer data from the IMU from the dragonboard to a csv file on a computer via the serial port. Here, the data can be manipulated using python. It utilises header guards and other sanity checks to ensure the data that is being transferred is correct and not being corrupted, before outputting the data to each respective CSV file to be later used in other modules. 

## Object Classification 
This module receives raw data from the magnetometer from a variety of samples and classifies them into different categories based on the magnetic field strength. It filters the bias and then finds the absolute magnitude across the 3 axes of the magnetometer data. It then searches for the peaks of the data and saves each peak to the magnetic strength associated with each object. It then saves the relevant category tally to a text file which is used for stocktake purposes, and outputs the count to then be transferred to the dragonboard to display on the LCD’s.

## Serial transfer from python to codewarrior
This module is responsible for transferring the data from the object detection and object classification modules from python to thedragonboard via the serial port. Here, the data can be manipulated using python. It utilises header guards and other sanity checks to ensure the data that is being transferred is correct and not being corrupted, before outputting the data to each respective CSV file to be later used in other modules. 

## Dragonboard display modules
The board will display a message for both the object detection/mapping and object classification modules. It takes inputs from the serial port and outputs to the LCD display. For the object detection modules, the board will receive from serial the x,y coordinates of any detected objects, and will display this on the LCD display. If the object classification module is being operated, it will display the objects found and total cost on the LCD display.


