import csv
import os

def clear_file(path : str):
    clear = open(path, 'w')
    clear.close()


def write_to_csv(path :str , info):
        g = open(path, 'a', newline='')
        
        writer = csv.writer(g)
                
        writer.writerow(info)
        
        g.close()

#checks if the lidar has done one complete revolution and clears the written data if it has
def check_if_clear_ready(path : str):
    if(os.path.getsize(path) > 1):



        f = open(path, 'r')
        f_csv = csv.reader(f)

        line_count = 0

        #get the last line and line count
        for row in f_csv:
            if(line_count == 0):
                first_line = row
            line_count += 1
            last_line = row


    
        #if the last read angle is smaller than the first read angle by 1% 
        #if line count > 1000 then there was an for sure and error reading so it never cleared
        # (might not need)
        if(line_count > 100 and (float(first_line[0])*1.02 > float(last_line[0]) ) or line_count > 1000):
            clear_file(path)
            clear_file('lidar.csv')

        f.close()