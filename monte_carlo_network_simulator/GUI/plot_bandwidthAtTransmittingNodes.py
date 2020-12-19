#DEFAULT IMPORTS 
########################################################################
import tkinter as tk



# Own imports
import sys
sys.path.append("GUI")
sys.path.append("Simulator/Network_models")
sys.path.append("Simulator")
sys.path.append("Plot_functionality")




from base_simulatorPlotPage import base_simulatorPage
from packet_statuses import PACKET_STATUS
from logger_class import Logger
import displayedTexts as TXT

import bandwidth_with_drift as SIM
########################################################################









# UNIQUE IMPLEMENTATION
########################################################################

import numpy as np

class bandwidthAtTransmttingNodes_page(base_simulatorPage):




    def __init__(self,parent, controller): 
        self.title = "Bandwidth at Transmitting Nodes"
        self.workFunction = workFunction
        self.plotFunction = plotFunction_averageBandwidth

        base_simulatorPage.__init__(self, parent, controller)
        self.addParameter(TXT.numberOfSimulations, startValue= 2)
        self.addParameter(TXT.faultTolerance_percent, startValue= 1)
        self.setDescription(TXT.description_bandwidthAtTransmittingNode)
        self.logger = Logger(simulationType = 'bandwidthAtTransmittingNodes')
        
    def getInputs(self):
        args, kwargs = base_simulatorPage.getInputs(self)
        numberOfSimulations= int(self._getInput_raw(TXT.numberOfSimulations))
        faultTolerance_percent = float(self._getInput_raw(TXT.faultTolerance_percent))
        kwargs["faultTolerance_percent"] = faultTolerance_percent
        kwargs["numberOfSimulations"] = numberOfSimulations
        return args, kwargs








# Must be outside the class        
def workFunction(progressQueue, *args, logger = None, numberOfSimulations = 10, faultTolerance_percent = 1, **kwargs):

    simulatorFun = SIM.bandwidthWithDrift

    nNodes = args[0]
    nPeriods = args[1]

    packetSize =kwargs['packetDuration']*kwargs['bitsPerMilisecond']
    transmitionTime = nPeriods*args[2] # args[2] = txPeriod (ms)
    newArgs = list(args)
    testCases = [i for i in  range( 1, nNodes, max(1, nNodes//20)) ] +[nNodes]
    totalMaxes = []
    totalMins = []
    totalMeans = []

    for i in testCases: 
        lowPosition  = int(i*( (faultTolerance_percent)/ 100)) #         
        highPosition = min( i-1,int(i*( (100 -faultTolerance_percent)/ 100)))                
        newArgs[0] = i
        maxes = []
        mins = []
        means = []
        for j in range(numberOfSimulations):
            progressQueue.put(i*numberOfSimulations + j, testCases[-1]*numberOfSimulations + numberOfSimulations)
            resultMatrix = simulatorFun( *newArgs, **kwargs)
            # Give data to the logger
            logger.add_resultMatrix(resultMatrix)

            
            throughput_per_node = np.sum( resultMatrix == PACKET_STATUS.RECEIVED, axis =0)

            tempMax = np.partition(throughput_per_node, highPosition)[highPosition] # Get the 2nd largest element 
            tempMin = np.partition(throughput_per_node, lowPosition)[lowPosition] # Get the 2nd largest element 


            maxes.append(     tempMax  *packetSize/transmitionTime )
            mins.append(      tempMin  *packetSize/transmitionTime )
            means.append( np.mean(throughput_per_node)  *packetSize/transmitionTime )

            

        totalMaxes.append(      max(maxes)        )
        totalMins.append(       min(mins)       )
        totalMeans.append(  np.mean(means)        )
        

        

    return  [], (faultTolerance_percent, testCases, totalMaxes,totalMins,totalMeans)




def plotFunction_averageBandwidth( *args, target = None, **kwargs ):
    tol = 3

    faultTolerance_percent, nNodes_list, maxBandwidths, minBandwidths, averageBandwidths = args[0]

    fig, ax = target
    ax.set_xlabel(TXT.transmitter_nNodes_axis)
    ax.set_ylabel(TXT.transmitter_bandwidth_axis, rotation = 'horizontal', labelpad = 25)
    ax.set_title(TXT.transmitter_plotTitle)
    ax.plot( nNodes_list, maxBandwidths,     "o-" , label = TXT.transmitter_upperLine_fun(faultTolerance_percent), color = "blue", picker = tol)
    ax.plot( nNodes_list, averageBandwidths, "o-" , label = TXT.transmitter_averageLine,color = "black", picker = tol)
    ax.plot( nNodes_list, minBandwidths,     "o-" , label = TXT.transmitter_lowerLine_fun(faultTolerance_percent), color = "red", picker = tol)
    ax.legend()



