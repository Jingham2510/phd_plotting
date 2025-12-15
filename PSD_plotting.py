import matplotlib.pyplot as plt
from os import listdir
from math import sqrt
from statistics import mean
"""
This program opens up a folder of TSV (tab-seperated value) files contianing particle size distribution data
Goes through the number-suffixed ones and plots the PSD data, whilst also tracking the range of different values provided for each

"""

def main(folderpath, manual = False):

    #Count the number of files in the folder
    num_of_files = len([file for file in listdir(folderpath)])
    print(f"TOTAL DATA_FILES: {num_of_files}")
    num_of_files = 0


    #Create a dictionary that stores the distribution density value lists
    dide_dic = {}

    #Create a dictionary that stores the cumulative distribution value lists
    cum_dic = {}

    first_val = 0
    first_val_acq = False

    #For each file
    for file in listdir(folderpath):
               
        #Check if the file name contains man (indicates manual)
        if not manual:
            if "man" not in file:    
                num_of_files =  num_of_files + 1
                #Return a paired list of grain size/associated value
                val_pairs = extract_values(folderpath, file)
                #Check the prefix (cum = cumulative, dide = distribution density)
                if str(file).startswith("cum"):
                    active_dict = cum_dic
                else:
                    active_dict = dide_dic
                
                #Place this in the relevant dictionary
                for val in val_pairs:
                    
                    #Get the first entry in the dict
                    if not first_val_acq:
                        first_val = val[0]
                        first_val_acq = True

                    if val[0] in active_dict.keys():
                        #If it does add it to the list
                        active_dict[val[0]].append(val[1])
                    else:
                        active_dict[val[0]] = [val[1]]             

        else:
            if "man" in file:    
                num_of_files =  num_of_files + 1
                #Return a paired list of grain size/associated value
                val_pairs = extract_values(folderpath, file)
                #Check the prefix (cum = cumulative, dide = distribution density)
                if str(file).startswith("cum"):
                    active_dict = cum_dic
                else:
                    active_dict = dide_dic
                
                #Place this in the relevant dictionary
                for val in val_pairs:
                    
                    #Get the first entry in the dict
                    if not first_val_acq:
                        first_val = val[0]
                        first_val_acq = True

                    if val[0] in active_dict.keys():
                        #If it does add it to the list
                        active_dict[val[0]].append(val[1])
                    else:
                        active_dict[val[0]] = [val[1]]      

    

    #Check the length of the first entry in the dictionary
    assumed_length = len(cum_dic[first_val])


    #Go through the dictionary and delete any entry that doesnt match the first length
    for key in dide_dic.copy().keys():
        if len(dide_dic[key]) != assumed_length:
            dide_dic.pop(key)
            print(f"KEY {key} REMOVED")
    for key in cum_dic.copy().keys():
        if len(cum_dic[key]) != assumed_length:
            cum_dic.pop(key)
            print(f"KEY {key} REMOVED")

    

    #print(cum_dic)
    #print(dide_dic)

    #Dipslay figure with all the PSDS on
    create_all_plots(cum_dic, assumed_length, "Cumulative Distribution of particles", "Particle size (umm)", "Cumulative Distribution (%)")

    #Display other figure with cumulative on
    create_all_plots(dide_dic, assumed_length, "Distribution Density of Particles", "Particle size (umm)", "Log(Distribution Density)")

    #-------Statistical analysis of results----------

    #Create boxplot of individual values
    #create_box_plot(cum_dic, "Cumulative Distribution Particle Size Statistical Distribution", "Particle size (umm)", "Cumulative Distribution (%)")
    
    #create_box_plot(dide_dic, "Distribution Density Statistical Distribution", "Particle size (umm)", "Cumulative Distribution (%)")



    plot_both_means(cum_dic, dide_dic)

    return


#Extract the value pairs from the tsv
def extract_values(folderpath, filename):

    vals = []

    first_line_skip = True

    with open(folderpath + "/" + filename) as f:        
        
        for line in f.readlines():
            #Skip the first line
            if first_line_skip:
                first_line_skip = False
                continue

            #Split the line into the seperate pairs
            pair = line.split()
            #convert the values to floats
            pair = [float(val) for val in pair]
            vals.append(pair)

    return vals


"""
Given a dictionary containing 
"""
def create_all_plots(val_dict, num_of_subplots, title, x_lab, y_lab):

    num_of_rows = 0
    num_of_columns = 0

    n_sqrt = sqrt(num_of_subplots)

    #Calculate how to split the number of rows/columns
    if  n_sqrt.is_integer:
        num_of_rows =  int(n_sqrt)
        num_of_columns =  int(n_sqrt)

    else:
        for i in range(2, 10):
            if num_of_subplots % i == 0:
                num_of_rows = int(i)
                num_of_columns = int(num_of_subplots/i)
                break
        #If their is no divisor lower than 10 - too many plots for a reasonable display
        print("Plot will be too messy!")
        exit()


    #Make a figure with the appropriate number of subplots
    fig, axs = plt.subplots(num_of_rows, num_of_columns) 

    row_cnt = 0 
    col_cnt = 0


    #Range of 0 -> number of plots to make
    for i in range(0, num_of_subplots):
        x = []
        y = []

        #Extract the appropriate value from each key
        for key in val_dict.keys():
            x.append(key)
            y.append(val_dict[key][i])       
        
        
        #Create the subfigure add the the main figure
        if col_cnt == num_of_columns:
            row_cnt = row_cnt + 1
            col_cnt = 0
        
        print(f"{i} - Row{row_cnt}, Col{col_cnt}")

        if num_of_subplots > 1:
            axs[row_cnt, col_cnt].plot(x, y)
            axs[row_cnt, col_cnt].set_xscale("log")
            axs[row_cnt, col_cnt].grid(True)
        else:
            axs.plot(x, y)
            axs.set_xscale("log")
            axs.grid(True)
        


        col_cnt = col_cnt + 1

    fig.suptitle(title)
    fig.supxlabel(x_lab)
    fig.supylabel(y_lab)


    plt.show()

    return


def create_box_plot(val_dict, title, x_lab, y_lab):

    data_pnts = [val_dict[vals] for vals in val_dict.keys()]

    fig = plt.boxplot(data_pnts)

    plt.grid(True)

    plt.title(title)

    plt.show()

    return



#Calculates the means of each set of dictionaries and plots the results on seperate graphs
def plot_both_means(cum_dict, dide_dict):

    #Plot font
    plt_font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}


    #Tick font
    title_font ={'family' : 'normal',
        'size'   : 16}

    #Generate the axis values
    x_cum = cum_dict.keys()
    y_cum = [mean(val) for val in cum_dict.values()]


    fig = plt.plot(x_cum, y_cum,  color="#7570b3")

    
    plt.tick_params("both", which="major", labelsize=14)
    plt.ylim([0, 100])
    plt.text(100, 60, "D60", fontdict=plt_font)
    plt.axhline(60, color = "r", linestyle="--")
    plt.text(100, 30, "D30",fontdict=plt_font)
    plt.axhline(30, color = "r", linestyle="--")
    plt.text(100, 10, "D10",fontdict=plt_font)
    plt.axhline(10, color = "r", linestyle="--")
    

    plt.title("Cumulative distribution of DKS grains", fontdict=title_font)
    plt.xscale("log")
    plt.xlabel("Particle Size (umm)", size=16)    
    plt.ylabel("Cumulative Distribution (%)", size=16)

    plt.grid(True)
    plt.show()


    x_dide = dide_dict.keys()
    y_dide = [mean(val) for val in dide_dict.values()]
    fig = plt.plot(x_dide, y_dide, color="#7570b3")

    plt.tick_params("both", which="major", labelsize=14)
    plt.title("Density distribution of DKS grains", fontdict=title_font)
    plt.xscale("log")
    plt.xlabel("Particle Size (umm)", size=16)    
    plt.ylabel("Density distribution (log(%))", size=16)

    plt.grid(True)
    plt.show()



    return


if __name__ == "__main__":
    print("---Particle Soil Distribution Plotting---")

    #This current folderpath only contains PSD measurements for the same sand
    folderpath = "C:/Users/User/Documents/Results/SOil Characterisation/PSD_csvs"


    main(folderpath, False)
    main(folderpath, True)