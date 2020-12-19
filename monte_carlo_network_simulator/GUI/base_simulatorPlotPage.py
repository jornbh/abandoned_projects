import tkinter as tk 
from abc import ABC

import sys
sys.path.append("GUI")





from base_graphPage import base_graphPage
from base_graphPage import TEXT_WIDTH

import displayedTexts as TXT




class base_simulatorPage(base_graphPage, ABC):




    def __init__(self,parent, controller): 
        
        
        base_graphPage.__init__(self, parent, controller)
        self.__init_buttons()
        self.__init_entries()
        self.__init_text()

        

    


    def __init_buttons(self):
        self.buttons = [
                tk.Button(self.buttonFrame, text = "Start", command = self.startPageTask) 
                ]

        for ind, el in enumerate(self.buttons):
            el.grid(row = ind, column = 0, stick = "ew") 

    def __init_entries(self): 

        # Text-boxes and dropdownMenues
        t = lambda x :self.addParameter(x[0], startValue = x[1] )  # Entry will be text
        d = lambda x :self.addDropdownMenu(x[0], x[1])             # Parameter will be a dropdown-menu

        parameters = [          (t, TXT.nNodes,                                                             7        ),
                                (t, TXT.nRetransmits,                                                       800      ), 
                                (t, "", None),                  
                                (t, TXT.txPeriod,                                                           40       ),                
                                (t, TXT.jitterMax_ms,                                                       10       ),     
                                (t, "", None),                  
                                                
                                (t, TXT.driftMax_ppm,                                                       40       ),
                                (t, "", None),                  
                                                
                                (t, TXT.packetLength_bits,                                                  369      ),      
                                (t, TXT.bitsPerMilisecond,                                                  1000     ),    
                                (t, "", None),
                                
                                (d, TXT.is_nodesSyncronized,                                  [  "False", "True"]    ),                              
                                (t, "", None),
                                
                                (t, TXT.receivedPacketProcessingTime,                                       0.009   ),                                   
                                (t, TXT.failedPacketProcessingTime,                                         0.009   ),
                                (t, "", None),
                                
                                ]

        self.parameterTexts = []
        self.parameterEntries = {}


        for i in parameters:
            
            i[0](i[1:]) # Apply its function on the variables

    def addParameter(self,  LabelText, startValue = ""):

        self.parameterTexts.append(tk.Text(self.inputFrame, height=1, width = TEXT_WIDTH , borderwidth=0))
        self.parameterTexts[-1].insert(1.0, LabelText)
        self.parameterTexts[-1].configure(state="disabled")
        self.parameterTexts[-1].configure(bg=self.inputFrame.cget('bg'), relief=tk.FLAT)
        self.parameterTexts[-1].grid(row = len(self.parameterTexts)-1, column = 0, stick = "w")
        


        if LabelText != "":
            self.parameterEntries[LabelText] = tk.Entry(self.inputFrame)

            self.parameterEntries[LabelText].grid(row = len(self.parameterTexts)-1, column = 1, stick="we", columnspan = 2)
            if startValue != None:
                self.parameterEntries[LabelText].insert(0, str(startValue))
        

    def addDropdownMenu(self, MenuDescription, Options):
        # Dropdown menues 
        # TODO ADD handlers that read form these fields
        self.parameterTexts.append( tk.Label(self.inputFrame, text = "Are boards synced at start") )
        var = tk.StringVar(self.inputFrame)
        var.set( Options[0])
        options = " Synced", "Unsynced"

        self.parameterEntries[MenuDescription] =  tk.OptionMenu(self.inputFrame,  var, *Options)

        self.parameterEntries[MenuDescription].config(width = len( max(options, key = len)))
        self.parameterTexts[-1].grid(row = len(self.parameterTexts)-1, column = 0, stick = "w")
        self.parameterEntries[MenuDescription].grid(row = len(self.parameterTexts)-1, column = 1, stick="we", columnspan = 2)
        

        # Hack soluton to acheive polymorphism between all parameters
        self.parameterEntries[MenuDescription].var = var
        self.parameterEntries[MenuDescription].get = lambda :self.parameterEntries[MenuDescription].var.get()


    def __init_text(self): 
        self.prefixes = []
        self.textEntries = {}



    def _getInput_raw(self, keyValue): # The key-value is the name of the parameter
        return self.parameterEntries[keyValue].get()

    def getInputs(self):
        raw_input = dict([(i , j.get()) for i,j in self.parameterEntries.items()])
        return translateInput(raw_input)

    


def translateInput(raw_input_list):
    try:

                                
        nNodes    = int(  raw_input_list[TXT.nNodes] ) 
        nPeriods  = int(  raw_input_list[TXT.nRetransmits] )   
        txPeriod  = float(raw_input_list[TXT.txPeriod] )   
        jitterMax = float(raw_input_list[TXT.jitterMax_ms ])    
        args = [ 
                nNodes, 
                nPeriods, 
                txPeriod, 
                jitterMax]
        kwargs = { }
        kwargs['driftMax_ppm'] =      float(raw_input_list[TXT.driftMax_ppm])

        kwargs['packetDuration'] = (  float(raw_input_list[TXT.packetLength_bits])
                                     /float(raw_input_list[TXT.bitsPerMilisecond]))

        kwargs['bitsPerMilisecond'] = float(raw_input_list[TXT. bitsPerMilisecond])
        


        if raw_input_list[TXT.is_nodesSyncronized].lower() == "true": 
            kwargs["initial_startTimeOfset"] = 0
        else:
            kwargs["initial_startTimeOfset"] = txPeriod
        
        
        kwargs['receivedPacketProcessingTime'] = float(raw_input_list[TXT.receivedPacketProcessingTime])
        kwargs['failedPacketProcessingTime'] =   float(raw_input_list[TXT.failedPacketProcessingTime]      )


        return args, kwargs
    except ValueError:
        print("Error: Invalid input arguments detected in function -translateInput(raw_input_list)")
        quit()
        return None, None

