import tkinter as tk 
from abc import ABC

import sys
sys.path.append("GUI")





from base_graphPage import base_graphPage







class base_simulatorPage(base_graphPage, ABC):




    def __init__(self,parent, controller): 
        
        
        base_graphPage.__init__(self, parent, controller)
        self.__init_buttons()
        self.__init_entries()

    
    def __init_buttons(self):
        self.buttons = [
                tk.Button(self.buttonFrame, text = "Start", command = self.startPageTask) 
                ]

        for ind, el in enumerate(self.buttons):
            el.grid(row = ind, column = 0, stick = "ew") 

    def __init_entries(self): 

        # Text-boxes
        functionParameters = [  "Number of nodes", 
                                "Number of simulations", 
                                "Period between retransmits", 
                                "Max jitter-value",
                                "Max clock drift (ppm)",
                                "packet length", 
                                "bits per millisecond",
                                "Initial spread of transmit times"
                                ]
        self.labels = [ tk.Label(self.inputFrame, text = i) for i in functionParameters]
        self.entries = [tk.Entry(self.inputFrame) for i in functionParameters]

        for ind, elem in enumerate(self.labels):
            elem.grid(row = ind, column = 0, stick = "w")
        for ind, elem in enumerate(self.entries):
            elem.grid(row = ind, column = 1, stick="we", columnspan = 2)


        defaultValues = [50, 200, 40, 10, 40, 369, 1000, 0]
        [i.insert(0, str(j)) for i,j in zip( self.entries, defaultValues)]



        # Dropdown menues 
        # TODO ADD handlers that read form these fields
        versionLabel = tk.Label(self.inputFrame, text = "Board version") 
        var = tk.StringVar(self.inputFrame)
        var.set("select an option... ")
        options = " nRF252", "nRF251", "This does not do anything"

        boardVersion = tk.OptionMenu(self.inputFrame, var, *options)

        boardVersion.config(width = len( max(options, key = len)))
        versionLabel.grid(row = 5000, column =0, stick = "w")
        boardVersion.grid(row = 5000, column =1, stick = "we")


    def getInputs(self):
        raw_input = [i.get() for i in self.entries]
        return translateInput(raw_input)





def translateInput(raw_input_list):
    try:
        nNodes    = int(  raw_input_list[0] ) 
        nPeriods  = int(  raw_input_list[1] )   
        txPeriod  = float(raw_input_list[2] )   
        jitterMax = float(raw_input_list[3] )    
        print(raw_input_list)
        args = [ 
                nNodes, 
                nPeriods, 
                txPeriod, 
                jitterMax]
        kwargs = { }
        kwargs['driftMax_ppm'] = float(raw_input_list[4])
        kwargs['packetDuration'] = float(raw_input_list[5])/ float(raw_input_list[6])
        kwargs['bitsPerMilisecond'] = float(raw_input_list[6])

        kwargs["initial_startTimeOfset"] = float( raw_input_list[7])
        return args, kwargs
    except:
        print("Invalid input", raw_input_list)
    return None, None