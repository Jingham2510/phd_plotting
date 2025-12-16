"""
This set of functions contains the ability to mass extract all the relevant data from every folder
"""


#Extracts all the data from a file
from tools import calc_time_passed, str_to_array, data_split
from os import listdir
from statistics import mean


def main(folderpath):

    prefixes = ["PHPID", "PID1", "PID2"]

    #Go through every prefix
    for prefix in prefixes:
        print(get_avg_force_err(folderpath, prefix))

    return

#Returns the total/phase2/phase3 force error over the whole run of each test
def get_avg_force_err(folderpath, prefix):
     
    #Create a dictionary to store the force error data
    total_force_err={}
    phase2_force_err = {}
    phase3_force_err = {}



    #Go through every file
    for file in listdir(folderpath):

        #Check it has the right prefix
        if prefix in file:
            #Get the data for that file
            data = get_data((folderpath + "/" +file))
            #Get the force errors
            data_ferr = data["force error"]

            phase_2_mark = data["phase 2 marker"]
            phase_3_mark = data["phase 3 marker"]

            #Group the file based on the force target (calc from a force and force error)
            target = round(data_ferr[0] - data["force"][0])

            #Append the data in the force error to the relevant section of the dictionary
            if target in total_force_err.keys():
                total_force_err[target].insert(mean(data_ferr))
            else:
                total_force_err[target] = mean(data_ferr)

            #Append the data in the force error to the relevant section of the dictionary
            if target in phase2_force_err.keys():
               phase2_force_err[target].insert(mean(data_ferr[phase_2_mark:phase_3_mark]))
            else:
                phase2_force_err[target] = mean(data_ferr[phase_2_mark:phase_3_mark])

            #Append the data in the force error to the relevant section of the dictionary
            if target in phase3_force_err.keys():
                phase3_force_err[target].insert(mean(data_ferr[:phase_3_mark]))
            else:
                phase3_force_err[target] = mean(data_ferr[:phase_3_mark])


    #print the average force errors
    for key in total_force_err.keys:
        print(f"{key} - {mean(total_force_err[key])}\n")
    

    #Return average errors
    return [total_force_err, phase2_force_err, phase3_force_err]






#Get all the data from each test
def get_data(filepath):
        

        phase2_marker = -1
        phase3_marker = -1

        datetimes = []
        pos = []
        ori = []
        forces = []
        force_error = []

        line_cnt = 0
        #Open the file
        with open(filepath) as file:
            #Go through every line
            for line in file:
                #Ensure line isnt empty
                if line and not(line.startswith("!")):
                    #Split the line up
                    tokens = data_split(line, True)               
                    
                    #Append the time data
                    datetimes.append(tokens[0])

                    #Append the position data
                    pos.append(tokens[1])
                    
                    #Append the force data
                    ori.append(tokens[2])

                    forces.append(tokens[3])

                    force_error.append(tokens[4])
                elif line.startswith(("!")) and "PHASE 2 STARTED" in line:
                    phase2_marker = line_cnt
                elif line.startswith(("!")) and "PHASE 3 STARTED" in line:
                    phase3_marker = line_cnt

                line_cnt = line_cnt + 1


        print(f"2:{phase2_marker}")
        print(f"3:{phase3_marker}")

        #Calculate the time differences 
        time = calc_time_passed(datetimes, True)



        #Turn the positions into numbers
        pos = str_to_array(pos)

        #Turn the forces into numbers
        force = str_to_array(forces)

        force_error = str_to_array(force_error)


        #Check that the data arrays are the same lengths
        if(not len(time) == len(pos) == len(forces)):
            print("DATA ARRAYS ARE INCONSISTENT LENGTH")

            print(f"time: {len(time)}, pos: {len(pos)}, forces: {len(forces)}")

            raise Exception()
        

        return {"datetimes":datetimes,
                "pos":pos,
                "ori":ori,
                "forces":forces,
                "force error":force_error, 
                "phase 2 marker":phase2_marker,
                "phase 3 marker":phase3_marker
                }





if __name__ == "__main__":

    print("FULL FOLDER COMP\n")

    folderpath = "C:\\Users\\User\\Documents\\Results\\DEPTH_TESTS\\"