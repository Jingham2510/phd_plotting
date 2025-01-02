
from datetime import datetime


#From https://stackoverflow.com/questions/38066836/python-best-way-to-remove-char-from-string-by-index
#Removes a character from a given index
def remove(s, indx):
    return "".join(x for x in s if s.index(x) != indx)





#Turn an array of strings into an array of numbers
#As long as format of strings is [data1,data2,data3]
def str_to_array(arr):

    real_arr = []

    #Go through every point in the array
    for x in arr:
        
        curr_ind_str = []
        curr_ind = []

        #Strip the first and final square bracket
        x = remove(x, x.find("["))
        x = remove(x, x.find("]"))

        #split the string up
        curr_ind_str.append(x.split(","))
    
       
        #Convert to integers
        for y in curr_ind_str:
            for z in y:
                print(z)
                curr_ind.append(float(z))

    

        #Append the data point to the real array
        real_arr.append(curr_ind)

    return real_arr



#Calculates the differences between an array of datetimes and calculates the total time passed
def calc_time_passed(times):
    time_passed = [0]

    #For every time calculate the time between it and the previous 
    i = 1
    while i < len(times):

        #Convert strings to datetimes
        #Remove the 7th character of the string so it can be parsed correctly
        #We can't really work to that accuracy anyways

        curr_time = datetime.strptime(times[i][:-1], "%H:%M:%S.%f")
        prev_time = datetime.strptime(times[i-1][:-1], "%H:%M:%S.%f")

        #Append the time difference
        time_passed.append(time_passed[len(time_passed) - 1] + (curr_time - prev_time).total_seconds())

        i = i + 1 

    return time_passed



#Calculate the approximate integral as a trapezoid
#For 3d data (xyz)
def xyz_integ_avg(time, data):

  

    data_x = [0]
    data_y = [0]
    data_z = [0]

    prev_pos = data[0]

    #Calculate the velocity at every point
    #By calculating the pos change / time diff
    i = 1
    while(i < len(data)):
        time_diff = time[i] - time[i-1]
        

        data_x.append(abs(data[i][0] - data[i-1][0]) / time_diff)
        data_y.append(abs(data[i][1] - data[i-1][1]) / time_diff)
        data_z.append(abs(data[i][2] - data[i-1][2]) / time_diff)


        i = i + 1   
      

    return [data_x, data_y, data_z]


