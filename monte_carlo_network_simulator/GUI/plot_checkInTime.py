import tkinter as tk



# Own imports
import sys
sys.path.append("GUI")
sys.path.append("Simulator/Network_models")
sys.path.append("Simulator/")
sys.path.append("Simulator")
sys.path.append("Plot_functionality")




from base_simulatorPlotPage import base_simulatorPage
from packet_statuses import PACKET_STATUS

import bandwidth_with_drift as SIM


from compressor_class import FirstCheckinTimes
from logger_class     import Logger
import displayedTexts as TXT






import numpy as np



class checkInTime_page(base_simulatorPage): 


    def __init__(self,parent, controller): 
        self.title = "Check-in time"
        self.workFunction = workFunction
        self.plotFunction = plotFunction

        base_simulatorPage.__init__(self, parent, controller)
        self.addParameter(TXT.numberOfSimulations      , startValue= 50)
        self.addParameter(TXT.faultTolerance_percent   ,startValue= 1)
        self.setDescription(TXT.description_checkinTime)
        self.logger = Logger(simulationType = "checkInTime")
        
    def getInputs(self):
        args, kwargs = base_simulatorPage.getInputs(self)
        numberOfSimulations= int(self._getInput_raw(TXT.numberOfSimulations))
        faultTolerance_percent = float(self._getInput_raw(TXT.faultTolerance_percent))
        kwargs["faultTolerance_percent"] = faultTolerance_percent
        kwargs["numberOfSimulations"] = numberOfSimulations
        return args, kwargs






def workFunction(progressQueue,*args, numberOfSimulations =200, faultTolerance_percent = 99, logger = None, **kwargs): 

    nNodes = args[0]
    kwargs['dataStorage_type'] = FirstCheckinTimes
    totalActuallyCheckedIn = []
    totalNeverCheckedIn = []
    print(args)

    checkinMatrix = []
    for i in range(numberOfSimulations):
        progressQueue.put(i, numberOfSimulations)
        resultMatrix = SIM.bandwidthWithDrift( *args, **kwargs)
        logger.add_resultMatrix(resultMatrix)   # Dump to logger
        checkinMatrix.append( resultMatrix )

    checkinMatrix = np.array(checkinMatrix)
    delete_mask = np.ones(checkinMatrix.shape, dtype = bool)

    if np.any(checkinMatrix ==None):
        # Count the ones that didnt check in and remove the samples
        numberOfUnchecked = 0
        for i, sim in enumerate(checkinMatrix):
            for j, node in enumerate(sim):
                if node == None:
                    numberOfUnchecked += 1
                    delete_mask[i,j] = False
        
        checkinMatrix = checkinMatrix[delete_mask]

        percentageCheckedIn = (1 - (numberOfUnchecked/(nNodes*numberOfSimulations)))*100
        percentageCheckedIn_tuple = ("How many checked in: ",'{} %'.format(percentageCheckedIn))
        
    else:
        percentageCheckedIn = 100
        percentageCheckedIn_tuple = ("How many checked in: ", '{} %'.format(percentageCheckedIn))

    return [percentageCheckedIn_tuple], (checkinMatrix, faultTolerance_percent, percentageCheckedIn)
    

def plotFunction(parameters, **y):
    checkinMatrix, faultTolerance_percent, percentageCheckedIn = parameters
    fig, ax = y['target']

    # Check if some nodes didnt check-in.
    if percentageCheckedIn < 100:
        fig.suptitle('NB! Only {} % of nodes checked in'.format(int(percentageCheckedIn)), color = 'r')
    else:
        fig.suptitle('')
    ARR = np.array (list((np.ndarray.flatten(checkinMatrix))))
    boxValues = ax.boxplot([ARR], whis= [0, 100- faultTolerance_percent], labels=[''])
    ax.set_ylabel("Periods\nbefore\nCheck-in", rotation='horizontal', labelpad = 25, size = 'x-large')
    ax.set_title("Box plot of Check-In time")
    ax.legend( (str(100 - faultTolerance_percent)+ "-Percentile",))
    # Now we want to display the box-plot variables.
    median = boxValues['medians'][0].get_xydata()[0,1]
    lowerBox = boxValues['boxes'][0].get_xydata()[0,1]
    upperBox = boxValues['boxes'][0].get_xydata()[2,1]
    lowerWhisker = boxValues['whiskers'][0].get_xydata()[1,1]        
    upperWhisker = boxValues['whiskers'][1].get_xydata()[1,1]

    outliers = []

    ARR.sort()
    outliers = np.unique(ARR[ARR>upperWhisker])
    

    return[ (TXT.Outliers, outliers),
            (TXT.UpperWhisker, upperWhisker) ,
            (TXT.UpperBox, upperBox),
            (TXT.Median, median) ,
            (TXT.LowerBox, lowerBox), 
            (TXT.LowerWhisker, lowerWhisker), ]


