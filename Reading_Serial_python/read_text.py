import map
import data_output as do
import calibration as cal
import magnet

x_offset = 0
y_offset = 0


def read_string(text):
    

    if(text == "b\'clear\'"):
        global x_offset
        global y_offset
        map.map(x_offset, y_offset)
        do.clear_all_files()
        return
    elif(text == "b\'calibrate\'"):
        [x_offset,y_offset] = cal.CalibrateGyro()
        do.clear_all_files() 
    elif(text == "b\'MagClr\'"):
        magnet.analyse_magnets()
        
        do.clear_all_files()