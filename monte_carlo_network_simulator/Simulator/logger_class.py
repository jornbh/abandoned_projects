# This is the logger class. It will generate a Log and save it.
import sys
import os
sys.path.append("..\\GUI\\")

import displayedTexts as TXT
import numpy as np
from packet_statuses import PACKET_STATUS 


#TODO: 1. Too much of this is hardcoded.
#      2. Allow for storing in different formats. (csv)

# The logger can save 2 files
# 1. Plot Results. That is the raw data generating the plots
# 2. RawSimulationResults. That is the raw data from the simulation

class Logger():

    def __init__(self, simulationType = ''):
        self.resultMatrices = []            # Variable for storing the data from the various simulations
        self.plotResult = None              # Variable for storing the plot data
        self.simulationType = simulationType
        self.savePath = '\Log\\'
        self.absPath= ('\\'.join((os.path.realpath(__file__).split('\\')[:-2])) + self.savePath)
    
    def set_plotResults(self, plotResults):
        self.plotResults = plotResults
    
    def add_resultMatrix(self, resultMatrix):
        self.resultMatrices.append(np.copy(resultMatrix))
    
    def set_simulationType(self, simulationType):
        self.simulationType = simulationType
    
    def savePlotData(self,args,kwargs, format = 'txt',saveName ='ParsedResults'):
        if format == 'txt':
            np.set_printoptions(threshold=np.inf)
            f = open('{}{}_{}.txt'.format(self.absPath, saveName,self.simulationType), 'w')
            f.write("Simulation parameters: \n")
            f.write("[nNodes, nPackets, TxP, jitterMax] = ")
            f.write(str(args) + '\n')
            f.write(str(kwargs) + '\n')
            f.write('Results below are the data used for making the plots. By comparing them to the plots it should be clear what the different arrays represent\n')

            if self.simulationType == 'bandwidthAtTransmittingNodes':
                f.write(TXT.logDescription_bandwidthAtTransmittingNodes_parsed)
                f.write(str(self.plotResults) + '\n')

            elif self.simulationType == 'checkInTime':
                f.write(TXT.logDescription_checkInTime_parsed)
                f.write(np.array_str(self.plotResults[0]))

            elif self.simulationType == 'bandwidthAtGatewayNode':
                f.write(TXT.logDescription_bandwidthAtGatewayNode_parsed)
                f.write(str(self.plotResults[1]) + '\n')
                f.write(np.array_str(self.plotResults[2][0]) + '\n')
                f.write(np.array_str(self.plotResults[2][1]) + '\n')
                f.write(np.array_str(self.plotResults[2][2]) + '\n')
                f.write(np.array_str(self.plotResults[2][3]) + '\n')

            f.close()

        else:
            print("Could not save log. \"{}\" is invalid file format".format(format))
    
    def saveRawSimulationData(self, args, kwargs, saveName = 'RawResults'):
        # Open log file
        f = open('{}{}_{}.txt'.format(self.absPath,saveName, self.simulationType), 'w')

        # Write simulation parameters to the first lines
        f.write("Simulation parameters: \n")
        f.write("[nNodes, nPackets, TxP, jitterMax] = ")
        f.write(str(args) + '\n')
        f.write(str(kwargs) + '\n')

        
        np.set_printoptions(threshold=np.inf) # Little hack to print the complete result matrix
        #Write explanation of result matrix
        f.write("Explanation of result matrix: \n")
        if self.simulationType == 'bandwidthAtTransmittingNodes':
            f.write(TXT.logDescription_bandwidthAtTransmittingNodes_raw)

        elif self.simulationType == 'checkInTime':
            f.write(TXT.logDescription_checkInTime_raw)

        elif self.simulationType == 'bandwidthAtGatewayNode':
            f.write(TXT.logDescription_bandwidthAtGatewayNode_raw)



        # Print all the result matrices
        for idx, resultMatrix in enumerate(self.resultMatrices):  
            f.write(np.array_str(resultMatrix))
            f.write('\n')



    def cleanUp(self):
        # Remove the references to the simulation results
        self.resultMatrices = []
        self.plotResult = None





