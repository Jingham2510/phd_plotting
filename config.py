"""
Stores the test config information
Currently only accesses and stores the robot minimum embedment height
"""


#Store the tool data
#i.e. diameter of the sphere is 100mm
TOOL_DATA = {"SPHERE": 100}




class ConfigHandler:

    #The height the robot reports when the tool is on the edge of embedding
    min_embed_height = 0.0

    def __init__(self, filepath):

        print("CREATING CONFIG OBJECT----")

        self.filepath = filepath

        with open(filepath) as file:

            line_count = 0

            for line in file:

                #Robot line count
                if line_count == 1:                    
                    try:
                        split = line.split("EMB:[")
                        self.min_embed_height = float(split[2].replace("]", "").strip())
                    #If embed height cant be found (backwrds compatability)
                    except:
                        print("NO EMBED HEIGHT - DEFAULT SET")
                        #Assume default embed height for sphere
                        self.min_embed_height = 176.0

                
                line_count = line_count + 1



 

   