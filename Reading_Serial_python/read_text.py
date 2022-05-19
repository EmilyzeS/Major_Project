import map
import data_output as do

def read_string(text):
    if(text == "b\'clear\'"):
        map.map()
        do.clear_all_files()
        return

    print("Error reading string ")

            
    
