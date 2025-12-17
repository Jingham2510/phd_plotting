"""
This set of functions contains the ability to mass extract all the relevant data from every folder
"""


#Extracts all the data from a file
from tools import calc_time_passed, str_to_array, data_split
from os import listdir
from statistics import mean
from numpy import concatenate
import matplotlib.pyplot as plt


"""
Main is currently setup for comparing PHPID and PID erros for the geotechnical 3 phase testing
"""
def PHPID_PID_comp(folderpath):

    prefixes = ["PHPID", "PID1", "PID2"]

    avg_errs = {"PHPID":[],"PID1":[],"PID2":[]}

    #Go through every prefix and get the average error for each run
    for prefix in prefixes:
        print(f"----{prefix}----\n")
        avg_errs[prefix] = get_avg_force_err(folderpath, prefix)


    
    

    return



#Create boxplots of each force err dataset (i.e. show spread)



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
            data = get_data((folderpath+file+"/data_"+file+".txt"))
            #Get the force errors
            data_ferr = concatenate(data["force error"])
            

            phase_2_mark = data["phase 2 marker"]
            phase_3_mark = data["phase 3 marker"]

           

            #Group the file based on the force target (calc from a force and force error)
            target = round(data_ferr[0] - data["forces"][0][2])

            #Append the data in the force error to the relevant section of the dictionary
            if target in total_force_err.keys():
                total_force_err[target].append(mean(data_ferr))
            else:
                total_force_err[target] = [mean(data_ferr)]

            #Append the data in the force error to the relevant section of the dictionary
            if target in phase2_force_err.keys():
               phase2_force_err[target].append(mean(data_ferr[phase_2_mark:phase_3_mark]))
            else:
                phase2_force_err[target] = [mean(data_ferr[phase_2_mark:phase_3_mark])]

            #Append the data in the force error to the relevant section of the dictionary
            if target in phase3_force_err.keys():
                phase3_force_err[target].append(mean(data_ferr[phase_3_mark:]))
            else:
                phase3_force_err[target] = [mean(data_ferr[phase_3_mark:])]


    #print the average force errors
    for key in total_force_err.keys():
        print(f"{key} TOTAL AVG - {mean(total_force_err[key])}, P2 AVG - {mean(phase2_force_err[key])}, P3 - {mean(phase3_force_err[key])} \n")
       
    

    #Return average errors
    return [total_force_err, phase2_force_err, phase3_force_err]


#Get phase2 and phase3 force errors
def get_phase_errs(folderpath, prefix):
    phase2_force_err = {}
    phase3_force_err = {}
    
    #Go through every file
    for file in listdir(folderpath):
        #Check it has the right prefix
        if prefix in file:            
            #Get the data for that file
            data = get_data((folderpath+file+"/data_"+file+".txt"))
            #Get the force errors
            data_ferr = data["force error"]

            phase_2_mark = data["phase 2 marker"]
            phase_3_mark = data["phase 3 marker"]

            #Group the file based on the force target (calc from a force and force error)
            target = round(data_ferr[0] - data["force"][0])

            #Append the data in the force error to the relevant section of the dictionary
            if target in phase2_force_err.keys():
               phase2_force_err[target].append(data_ferr[phase_2_mark:phase_3_mark])
            else:
                phase2_force_err[target] = [data_ferr[phase_2_mark:phase_3_mark]]

            #Append the data in the force error to the relevant section of the dictionary
            if target in phase3_force_err.keys():
                phase3_force_err[target].append(data_ferr[:phase_3_mark])
            else:
                phase3_force_err[target] = data_ferr[:phase_3_mark]


    return [phase2_force_err, phase3_force_err]

"""
Creates box plots based on the phase2 and phase 3 error for each of the PHPID and PID tests 
Useful when combined with the average area to look at the spread of errors
allows for a more quantative analysis (that considers the whole signal)
"""
def PHPID_PID_box_comp(folderpath):

    prefixes = ["PHPID", "PID1", "PID2"]

    errs = {"PHPID":[],"PID1":[],"PID2":[]}

    #Go through every prefix and get the error for the phases of each run
    for prefix in prefixes:
        print(f"----{prefix}----\n")
        errs[prefix] = get_phase_errs(folderpath, prefix)


    #Set up the figure to store all the subfigures
    ROW_MAX = 3
    COL_MAX = 2
    fig,axs = plt.subplots(ROW_MAX, COL_MAX)
    row_cnt = 0
    col_cnt = 0

    

    #Go through each prefix and create the plot
    for prefix in prefixes:
        #Reset the pointer
        if col_cnt == COL_MAX-1:
            row_cnt = row_cnt + 1
            col_cnt = 0

        axs(row_cnt,col_cnt) = plt.boxplot(errs[prefix][col_cnt])
        col_cnt = col_cnt + 1
        axs(row_cnt,col_cnt) = plt.boxplot(errs[prefix][col_cnt])

        


  
    #Setup the figure
    fig.suptitle("Phase error Comparison")


    for ax, row in zip(axs[:, 0],prefixes):
        ax.set_title(row)

    for ax, col in zip(axs[:, 0], ["Phase 2", "Phase 3"]):
        ax.set_title(col)    


    plt.show()
    

    return
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



        #Calculate the time differences 
        time = calc_time_passed(datetimes, True)



        #Turn the positions into numbers
        pos = str_to_array(pos)

        #Turn the forces into numbers
        forces = str_to_array(forces)

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

    PHPID_PID_comp(folderpath)