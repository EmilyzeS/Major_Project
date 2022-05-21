import map
import data_output as do
import calibration as cal

def read_string(text):
    if(text == "b\'clear\'"):
        map.map(x_offset, y_offset)
        do.clear_all_files()
        return
    else if(text == "b\'calibrate\'"):
        [x,y] = cal.CalibrateGyro()
        do.clear_all_files()
        return [x,y]  


            
    
