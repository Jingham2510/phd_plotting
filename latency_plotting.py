import matplotlib.pyplot as plt



def main(filepath):


    latency = []
    timesteps = []

    step = 1

    #Open the file
    with open(filepath) as file:

        #extract the line
        for line in file:

            #Save the data in the line
            latency.append(float(line.strip("\n")))

            timesteps.append(step)

            step = step + 1 


    plt.plot(latency)

    plt.show()




    return





if __name__ == "__main__":

    main("C:/Users/User/Documents/Results/robot_latency_tests/raw/latency_python.txt")