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
Results pre-taken from the results excel sheet
Compares the force error averages for the different speeds tested
"""
def speed_mod_comparison(folderpath):

    #Target for all of the speed 
    FORCE_TARGET = -200    

    #Speeds (in mm/s)
    speeds =[0.25, 0.5, 1, 2, 5, 10, 25] 

    vert_force_errs = {}
    lateral_forces = {}

    #Go through every file
    for file in listdir(folderpath):
        data = get_data((folderpath+file+"/data_"+file+".txt"))

        #We only care about phase 3 data
        phase3_marker = data["phase 3 marker"]
      
        #Extract the forces
        phase3_x_forces = list(x[0] for x in data["forces"][phase3_marker:])
        phase3_y_forces = list(x[1] for x in data["forces"][phase3_marker:])
        phase3_z_errs = concatenate(list(x for x in data["force error"][phase3_marker:]))
        

        #Get the speed from the title
        splt_title = file.split("_")[0]
        splt_title=int(splt_title.split("-")[1]) / 100
            
        
        #Sort the forces into the dictionary
        if splt_title in vert_force_errs.keys():
            vert_force_errs[splt_title].append(phase3_z_errs)            
            lateral_forces[splt_title].append([phase3_x_forces, phase3_y_forces])
        else:
            vert_force_errs[splt_title] = [phase3_z_errs]
            lateral_forces[splt_title] = [phase3_x_forces, phase3_y_forces]


            
    #Force Averages
    avg_vert_errs = []
    avg_lat_force = []

    #Go through each key and calculate the force averages
    for key in speeds:

        #WRONG
        #Flatten all the error signals from each run into one
        #errs_flattened =list((x for xs in vert_force_errs[key] for x in xs))
        
        #Calculate the average error for each run
        errs = list(mean(x) for x in vert_force_errs[key])
    
        #Calculate the average of the average errors and append
        avg_vert_errs.append(mean(errs)) 

        #Calculate the absolute lateral force being applied 
        x_forces = list(abs(x) for x in lateral_forces[key][0])
        y_forces = list(abs(y) for y in lateral_forces[key][1])

        #Calculate the average of the average lateral forces and append
        avg_lat_force.append((mean(x_forces) + mean(y_forces))/2)


    fig, ax = plt.subplots()
    ax.plot(speeds, avg_vert_errs, color="#1b9e77", label = "Fz", marker = "o")
    ax.set_xlabel("End-effector speed (mm/s)", size = 18)
    ax.set_ylabel("Mean force error (N)", size = 18)
    

    #ax2 = ax.twinx()
    #ax2.set_ylabel("Mean lateral force (N)")
    #ax2.plot(speeds, avg_lat_force, color="#d95f02", label = "FLat", marker = "o")    
    ax.set_xscale("log")

    plt.grid(True)
    fig.legend(fontsize = 18)
    plt.show()


    #BOXPLOT ------------------
    errs_flattened = list(list((x for xs in vert_force_errs[key] for x in xs)) for key in speeds)

    fig, ax = plt.subplots()
    plt.boxplot(errs_flattened, showfliers=False)
    ax.set_xlabel("Speed (mm/s)", size = 16)
    ax.set_ylabel("Force error (N)", size = 16)
    ax.set_xticklabels(speeds)
    #plt.ylim([-17, 17])
    plt.show()


    return




"""
Main is currently setup for comparing PHPID and PID erros for the geotechnical 3 phase testing
"""
def PHPID_PID_comp(folderpath):

    prefixes = ["PHPID", "PID1", "PID2"]
    targets = [5, 10, 25, 50, 100, 200, 300, 400]


    avg_errs = {"PHPID":[],"PID1":[],"PID2":[]}

    phase2_errs = []
    phase2_percentage_errs = []

    phase3_errs = []
    phase3_percentage_errs = []


    #Go through every prefix and get the average error for each run
    for prefix in prefixes:
        print(f"----{prefix}----\n")
        avg_errs[prefix] = get_avg_force_err(folderpath, prefix)


        #PHASE 2 ----------
        phase_2_avgs = list(mean(avg_errs[prefix][1][x]) for x in targets)
        phase_2_percentage_err = []

        for i in range(len(phase_2_avgs)):
            phase_2_percentage_err.append(abs((phase_2_avgs[i]/targets[i]) * 100))

        phase2_errs.append(phase_2_avgs)
        phase2_percentage_errs.append(phase_2_percentage_err)
        

        #PHASE 3 ---------
        phase_3_avgs = list(mean(avg_errs[prefix][2][x]) for x in targets)
        phase_3_percentage_err = []
        for i in range(len(phase_3_avgs)):
            phase_3_percentage_err.append(abs((phase_3_avgs[i]/targets[i]) * 100))


        phase3_errs.append(phase_3_avgs)
        phase3_percentage_errs.append(phase_3_percentage_err)
    

    #PHASE 2 PLOTS ----

    #------MAGNITUDE-----
    print("PHASE 2 MAGNITUDE")
    plt.plot(targets, phase2_errs[0], color="#1b9e77", label = "PHPID", marker = "o")
    plt.plot(targets, phase2_errs[1], color="#d95f02", label = "PID", marker = "o")

    plt.xticks(targets)
    plt.xlabel("Force Target (N)", size = 18)
    plt.ylabel("Average Error (N)", size = 18)
    plt.grid(True)
    
    plt.legend(fontsize = 18)
    plt.show()

    #PERCENTAGE ERROR
    print("PHASE 2 PERCENTAGE ERROR")
    plt.plot(targets, phase2_percentage_errs[0], color="#1b9e77", label = "PHPID", marker = "o")
    plt.plot(targets, phase2_percentage_errs[1], color="#d95f02", label = "PID", marker = "o")

    plt.xticks(targets)
    plt.xlabel("Force Target (N)", size = 18)
    plt.ylabel("Average Error (%)", size = 18)
    plt.grid(True)
    
    plt.legend(fontsize = 18)
    plt.show()
    

    #PHASE 3 PLOTS -----
 #------MAGNITUDE-----
    print("PHASE 3 MAGNITUDE")
    plt.plot(targets, phase3_errs[0], color="#1b9e77", label = "PHPID", marker = "o")
    plt.plot(targets, phase3_errs[1], color="#d95f02", label = "PID(Hi)", marker = "o")    
    plt.plot(targets, phase3_errs[2], color="#7570b3", label = "PID(Lo)", marker = "o")

    plt.xticks(targets)
    plt.xlabel("Force Target (N)", size = 18)
    plt.ylabel("Average Error (N)", size = 18)
    plt.grid(True)
    
    plt.legend(fontsize = 18)
    plt.show()

    #PERCENTAGE ERROR
    print("PHASE 3 PERCENTAGE ERROR")
    plt.plot(targets, phase3_percentage_errs[0], color="#1b9e77", label = "PHPID", marker = "o")
    plt.plot(targets, phase3_percentage_errs[1], color="#d95f02", label = "PID(Hi)", marker = "o")
    plt.plot(targets, phase3_percentage_errs[2], color="#7570b3", label = "PID(Lo)", marker = "o")

    plt.xticks(targets)
    plt.xlabel("Force Target (N)", size = 18)
    plt.ylabel("Average Error (%)", size = 18)
    plt.grid(True)
    
    plt.legend(fontsize = 18)
    plt.show()


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
        #for key in total_force_err.keys():
        #   print(f"{key} TOTAL AVG - {mean(total_force_err[key])}, P2 AVG - {mean(phase2_force_err[key])}, P3 - {mean(phase3_force_err[key])} \n")
       
    

    #Return average errors
    return [total_force_err, phase2_force_err, phase3_force_err]


#Get phase2 and phase3 force errors
#DATA STRUCTURE 
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
            data_ferr = concatenate(data["force error"])

            phase_2_mark = data["phase 2 marker"]
            phase_3_mark = data["phase 3 marker"]

            #Group the file based on the force target (calc from a force and force error)
            target = round(data_ferr[0] - data["forces"][0][2])

            #Append the data in the force error to the relevant section of the dictionary
            if target in phase2_force_err.keys():
               phase2_force_err[target].append(data_ferr[phase_2_mark:phase_3_mark])
            else:
                phase2_force_err[target] = [data_ferr[phase_2_mark:phase_3_mark]]

            #Append the data in the force error to the relevant section of the dictionary
            if target in phase3_force_err.keys():
                phase3_force_err[target].append(data_ferr[phase_3_mark:])
            else:
                phase3_force_err[target] = [data_ferr[phase_3_mark:]]


    return [phase2_force_err, phase3_force_err]

"""
Creates box plots based on the phase2 and phase 3 error for each of the PHPID and PID tests 
Useful when combined with the average area to look at the spread of errors
allows for a more quantative analysis (that considers the whole signal)
"""
def PHPID_PID_box_comp_all(folderpath):

    prefixes = ["PHPID", "PID1", "PID2"]

    errs = {"PHPID":[],"PID1":[],"PID2":[]}

    targets = [5, 10, 25, 50, 100, 200, 300, 400]

    #Go through every prefix and get the error for the phases of each run
    for prefix in prefixes:      
        errs[prefix] = get_phase_errs(folderpath, prefix)



    
    for targ in targets:
            #Set up the figure to store all the subfigures
        ROW_MAX = 3
        COL_MAX = 2
        fig,axs = plt.subplots(ROW_MAX, COL_MAX)
        
        row_cnt = 0
        col_cnt = 0

        #Go through each prefix and create the plot
        for prefix in prefixes:
            print(f"----{prefix}----\n")
            #Reset the pointer
            if col_cnt == COL_MAX-1:
                row_cnt = row_cnt + 1
                col_cnt = 0
            print(f"{row_cnt}, {col_cnt}")
            axs[row_cnt,col_cnt].boxplot(errs[prefix][col_cnt][targ], showfliers=False)
            col_cnt = col_cnt + 1
            axs[row_cnt,col_cnt].boxplot(errs[prefix][col_cnt][targ], showfliers=False)



        #Setup the figure
        fig.suptitle(f"Phase error comparison - target = -{targ}")


        #for ax, row in zip(axs[:, 0],prefixes):
        #   ax.set_title(row)

        #for ax, col in zip(axs[:, 0], ["Phase 2", "Phase 3"]):
        #   ax.set_title(col)    


        fig.show()
        plt.show()
        fig.clear()
    

    return


#Plot the boxplots of the combined force errors (i.e. zip all target 5N together then plot as a box next to 10/25 etc...)
def PHPID_PID_box_comp_targets(folderpath):

    prefixes = ["PHPID", "PID1", "PID2"]

    errs = {"PHPID":[],"PID1":[],"PID2":[]}

    targets = [5, 10, 25, 50, 100, 200, 300, 400]

    #Go through every prefix and get the error for the phases of each run
    for prefix in prefixes:      
        errs[prefix] = get_phase_errs(folderpath, prefix)


        #Phase 2 - index 0
        
        #Flatten each of the error signals into one giant list to asses the whole thing
        phase2_errs_flattened = list(list((x for xs in errs[prefix][0][key] for x in xs)) for key in targets)

        fig, ax = plt.subplots()
        plt.boxplot(phase2_errs_flattened, showfliers=False)
        ax.set_xlabel("Force Target (N)", size = 16)
        ax.set_ylabel("Force (N)", size = 16)
        ax.set_xticklabels(targets)
        plt.ylim([-17, 17])
        plt.show()

        #Phase 3 - index 1 

        phase3_errs_flattened = list(list((x for xs in errs[prefix][1][key] for x in xs)) for key in targets)

        fig, ax = plt.subplots()
        plt.boxplot(phase3_errs_flattened, showfliers=False)
        ax.set_xlabel("Force Target (N)", size = 16)
        ax.set_ylabel("Force (N)", size = 16)
        ax.set_xticklabels(targets)
        plt.ylim([-55, 55])
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

    #PHPID_PID_comp(folderpath)

    #PHPID_PID_box_comp_targets(folderpath)
    speed_mod_comparison(folderpath)