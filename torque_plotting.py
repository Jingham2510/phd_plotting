"""
A simple file that contains the associated data/plotting functions
"""
import matplotlib.pyplot as plt
import datetime
import os 
import tools


def plot_torques(filename):


    #Time data
    timestep = []

    #Torque Data
    m1_trq = []
    m2_trq = []
    m3_trq = []
    m4_trq = []
    m5_trq = []
    m6_trq = []


    #Open the file
    with open(filename) as f:

    
        #Save the first timestep as 0

        times = []

        m1_trq = []
        m2_trq = []
        m3_trq = []
        m4_trq = []
        m5_trq = []
        m6_trq = []

        

        for line in f:

            #Extract the line info
            curr_line = line.split(",", 2)

           #Format the timestep
            print(curr_line[1][11:26])
            curr_line_time = datetime.datetime.strptime(curr_line[1][11:26], "%H:%M:%S.%f")

            #Save the first time as the original time
            if len(times) == 0:
                times.append(0)
                first_time = curr_line_time

            else:
                #Calculate time passed since original time
                times.append((curr_line_time - first_time).total_seconds())

            #Split the torque array into seperate torques
            #Remove the square brackets
            tq = curr_line[2].replace("[","")
            tq = tq.replace("]","")
            torques = tq.split(",")

            m1_trq.append(float(torques[0]))
            m2_trq.append(float(torques[1]))
            m3_trq.append(float(torques[2]))
            m4_trq.append(float(torques[3]))
            m5_trq.append(float(torques[4]))
            m6_trq.append(float(torques[5]))


    #Create a plot contianing 6 seperate subplots
    fig, axs = plt.subplots(3, 2)

    axs[0,0].plot(times, m1_trq)
    axs[0,0].set_title("Motor 1 Torque")

    axs[0,1].plot(times, m2_trq)
    axs[0,1].set_title("Motor 2 Torque")

    axs[1,0].plot(times, m3_trq)
    axs[1,0].set_title("Motor 3 Torque")

    axs[1,1].plot(times, m4_trq)
    axs[1,1].set_title("Motor 4 Torque")

    axs[2,0].plot(times, m5_trq)
    axs[2,0].set_title("Motor 5 Torque")

    axs[2,1].plot(times, m6_trq)
    axs[2,1].set_title("Motor 6 Torque")

    #Set axs labels
    for ax in axs.flat:
        ax.set(xlabel="Time(s)", ylabel="Torque(Nm)")


    #Set layout type
    fig.tight_layout()


    plt.show()




    return




if __name__ == "__main__":
    print("PLOTTING")
    plot_torques("C:/Users/User/Documents/Results/torque_test/raw/11_03_real.txt")