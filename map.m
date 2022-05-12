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
raw_data=csvread('dataeg.csv');

%establish the number of angles and ranges in the data
[number_of_data_sets, number_of_measurements]=size(raw_data);


%create the  zero matrix of the same size of raw_data
time_intervals = raw_data(:,1);

ranges = zeros(size(number_of_data_sets));

angles = raw_data(:,2);

maxvalue=max(angles);
minvalue=min(angles);
difference=maxvalue-minvalue;



angles = angles - minvalue;
angles = angles ./ (difference/100);
angles = angles .* 0.9;
angles = angles - 45;





%value for the speed of light
c=299792458;

%calculate the ranges by using the prior equation, multiplying time x
%speed, dividing by two and 10^9 to convert to metres
ranges=time_intervals .* c / (10^13);


%convert the range and angle to the x coordinate via r*cos(t)
x= ranges .* cosd(angles);

%convert the range and angle to the y coordinate via r*sin(t)
y=ranges .* sind(angles);


scatter(x,y,"*")
