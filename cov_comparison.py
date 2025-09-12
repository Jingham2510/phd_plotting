import matplotlib.pyplot as plt
import os

#Function that takes two test folders and compares the coverage data
def comp_coverage(test_1_name, test_2_name):

    DEFAULT_TEST_LOC = "C:/Users/User/Documents/Results/DEPTH_TESTS"

    #Check the tests exist
    if not (os.path.isdir((DEFAULT_TEST_LOC + "/" + test_1_name))): 
        print("TEST 1 DOESNT EXIST")
        return
    if not (os.path.isdir((DEFAULT_TEST_LOC + "/" + test_2_name))):
        print("TEST 2 DOES NOT EXIST")
        return


    #Get the test data
    cov_1 = []
    cov_2 = []

    with open(DEFAULT_TEST_LOC + "/" + test_1_name + "/cov_" + test_1_name + ".txt") as f:
        for line in f:
            cov_1.append(float(line.strip()))

    with open(DEFAULT_TEST_LOC + "/" + test_2_name + "/cov_" + test_2_name + ".txt") as f:
        for line in f:
            cov_2.append(float(line.strip()))

    #Remove the first values - as these will be outliars generated
    #cov_1.pop(0)
    #cov_2.pop(0)



    #Create a dictionary that holds the data
    data_dict = {test_1_name : cov_1, test_2_name : cov_2}

    #Plot the boxplots
    fig, ax = plt.subplots()
    ax.boxplot(data_dict.values())
    ax.set_xticklabels(data_dict.keys())

    plt.show()
    
    




if __name__ == "__main__":

    print("BOXPLOT COMP")

    comp_coverage("30_deg_cov", "45_deg_cov")