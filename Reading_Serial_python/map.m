clc
clear

%q2
%Millimeter wave (mmWave) is a special class of radar technology that uses short- wavelength electromagnetic waves.
%millimeter wave technology allows transmission on frequencies between 30 GHz and 300 GHz

%the return time of a short infarred light pulse to be emitted and returned
%to teh sensor

%time of flight  =speedlight x time to return/2
%=3*10^8*t/2 

%load and store the data 'radar_202.csv' in raw_data
%be in form distance, angle
angles=csvread('angledata.csv');
time_intervals = csvread('lidar.csv');

[num_angle_readings, ~] = size(angles);
[number_lidar_readings, ~] = size(time_intervals);

while(num_angle_readings ~= number_lidar_readings)
    
    [num_angle_readings, ~] = size(angles);
    [number_lidar_readings, ~] = size(time_intervals);
    
    if(num_angle_readings > number_lidar_readings)
       angles = angles(1:end-1, :); 
    elseif (num_angle_readings < number_lidar_readings)
        time_intervals = time_intervals(1:end-1, :);      
    end
    
    
    
    
end

%create the  zero matrix of the same size of raw_data
azimuth = angles(:,1);

maxvalue=max(azimuth);
minvalue=min(azimuth);
difference=maxvalue-minvalue;



azimuth = azimuth - minvalue;
azimuth = azimuth ./ (difference/100);
azimuth = azimuth .* 0.9;
azimuth = azimuth - 45;





%value for the speed of light
c=299792458;

%calculate the ranges by using the prior equation, multiplying time x
%speed, dividing by two and 10^9 to convert to metres
ranges=time_intervals .* c / (10^13);


%convert the range and angle to the x coordinate via r*cos(t)
x= ranges .* cosd(azimuth);

%convert the range and angle to the y coordinate via r*sin(t)
y=ranges .* sind(azimuth);


scatter(x,y,"*")
