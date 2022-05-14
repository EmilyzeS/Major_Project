import map
import data_output as do

def read_string(text):
    if(text == "b\'clear\'"):
        #map.map()
        do.clear_file('lidar.csv')
        do.clear_file('angledata.csv')
        return

    print("Error reading string ")

            
    
