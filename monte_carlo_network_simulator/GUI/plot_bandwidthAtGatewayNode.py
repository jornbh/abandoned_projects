#DEFAULT IMPORTS 
########################################################################
import tkinter as tk
import numpy as np


# Own imports
import sys
import os
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




from functools import reduce
from operator import add
import compressor_class




# UNIQUE IMPLEMENTATION
########################################################################

import numpy as np

class bandwidthAtGatewayNode_page(base_simulatorPage):




    def __init__(self,parent, controller): 
        self.title = "Bandwidth at Gateway Node"
        self.workFunction = workFunction
        self.plotFunction = plotFunction_averageBandwidth
        base_simulatorPage.__init__(self, parent, controller)
        
        
        self.f.delaxes(self.a)
        vals =  [411, 412, 413, 414] # each element descrives one subplot in a grid (nrows, ncols, position in grid)
        List = [ self.f.add_subplot(i) for i in vals]
        self.a_list = List
        self.addParameter(TXT.numberOfSimulations, startValue= 2)
        self.addParameter(TXT.faultTolerance_percent, startValue= 1)
        self.setDescription(TXT.desxription_bandwidthAtGatewayNode)

        self.logger = Logger(simulationType = 'bandwidthAtGatewayNode')


 
    def getInputs(self):
        args, kwargs = base_simulatorPage.getInputs(self)
        numberOfSimulations= int(self._getInput_raw(TXT.numberOfSimulations))
        faultTolerance_percent = float(self._getInput_raw(TXT.faultTolerance_percent))
        kwargs["faultTolerance_percent"] = faultTolerance_percent
        kwargs["numberOfSimulations"] = numberOfSimulations
        return args, kwargs



    def animate(self, i):
        if not self.q.empty():
            printResult, plotResult  = self.q.get()
            self.printFunction(printResult)
            if plotResult != None:
                self.a.clear()
                self.plotFunction( plotResult, target=( self.f, self.a_list))









# Must be outside the class        
def workFunction(progressQueue,*args, numberOfSimulations=10, faultTolerance_percent = 1, logger=None, **kwargs):
    print(args)
    nNodes = args[0]
    nPeriods = args[1]
    txPeriod = args[2]


    packetSize = kwargs['packetDuration']* kwargs['bitsPerMilisecond']
    kwargs['dataStorage_type']=  compressor_class.CountPacketOfAllTypesForEachNode
    newArgs = list(args)
    testCases = [num_nodes for num_nodes in  range( 1, nNodes, max(1, nNodes//20)) ] + [nNodes]

    totalBandwidths       = np.full( (3,len(testCases)), 0.0 )
    CRCErrors_percent     = np.full( (3,len(testCases)), 0.0 )
    AddressErrors_percent = np.full( (3,len(testCases)), 0.0 )
    neverDetecetd_percent = np.full( (3,len(testCases)), 0.0 )

    
    for ind, num_nodes in enumerate(testCases): 


        progressQueue.put(num_nodes, testCases[-1]) # Show how far the simulation has come
    
        newArgs[0] = num_nodes
        #resultMatrixes =np.array( [ SIM.bandwidthWithDrift(*newArgs, **kwargs) for j in range(numberOfSimulations)]) # 3D matrix
        resultMatrixes = []
        for j in range(numberOfSimulations):
            resultMatrix =  SIM.bandwidthWithDrift(*newArgs, **kwargs)
            logger.add_resultMatrix(resultMatrix)
            resultMatrixes.append(resultMatrix)


        #Simpler notation
        f = lambda *Types: getCounts(np.array(resultMatrixes),faultTolerance_percent, *Types)

        totalBandwidths[:, ind]       = f( PACKET_STATUS.RECEIVED                                   )*packetSize/(nPeriods*txPeriod)
        CRCErrors_percent[:, ind]     = f( PACKET_STATUS.PAYLOAD_ERROR, PACKET_STATUS.LENGTH_ERROR  )*100.0/(nPeriods)
        AddressErrors_percent[:, ind] = f( PACKET_STATUS.ADDRESS_ERROR                              )*100.0/(nPeriods)
        neverDetecetd_percent[:, ind] = f( PACKET_STATUS.NEVER_ARRIVED                              )*100.0/(nPeriods)
    
    
    
    plotValues = faultTolerance_percent ,testCases,  (totalBandwidths, CRCErrors_percent, AddressErrors_percent, neverDetecetd_percent)

    return [], plotValues


def getCounts( resultMatrixes, tolerance_percent, *Types):
    # countPerNode= lambda x:np.sum(resultMatrixes==x, axis =2)
    

    perNode_list = sum( [ resultMatrixes[:,:, i] for i in Types])



    flattenedList = np.ndarray.flatten(perNode_list)
    highIndex = min(  len(flattenedList) -1, int((100-tolerance_percent)*len(flattenedList)/100) )
    lowIndex =  int(     tolerance_percent *len(flattenedList)/100)
    


    highEstimate =   np.partition(flattenedList, highIndex)[highIndex]
    mediumEstimate = np.mean( perNode_list)
    lowEstimate =    np.partition(flattenedList, lowIndex)[lowIndex]



    return np.array([highEstimate, mediumEstimate,lowEstimate ], dtype = 'f')
    





def plotFunction_averageBandwidth( args, target = None, **kwargs ):
    # Define tolerance for clicking on data points. Clicks in vincinity of a datapoint will show as clicks on that datapoint
    tol = 3

    faultTolerance_percent, testCases, Results_list = args
    # Target is multiple values in this class
    fig, ax_list = target
    fig.suptitle("Bandwidth and interference at the Gateway Node")
    ylabel_list = [ "Bandwidth\n[kbps]", 
                    "CRC\nerrors\n[%]", 
                    "Access\nAddress\nerrors\n[%]", 
                    "Arrived\nwhile busy\n[%]"]
    xlabel_list = ["Number of nodes" ] *4
    colors = ["red", "blue", "black", "brown"]

    fig.subplots_adjust(hspace = 0.3)
    for i, ax in enumerate(ax_list):
        
        ax.clear()
        ax.set_xlabel(xlabel_list[i])
        ax.set_ylabel(ylabel_list[i], rotation = 'horizontal', labelpad = 30)
        for j,el in enumerate(Results_list[i]):
            if j ==1:
                ax.plot(testCases, el, "o-", color = colors[i], picker=tol)
            elif j ==0:
                ax.plot(testCases, el, "o--", color = colors[i], picker=tol)
            else:
                ax.plot(testCases, el, "x--", color = colors[i], picker=tol)

        ax.legend([

                    TXT.gateway_upperLine_fun(faultTolerance_percent),
                    TXT.gateway_averageLine ,
                    TXT.gateway_lowerLine_fun(faultTolerance_percent)
        ])

