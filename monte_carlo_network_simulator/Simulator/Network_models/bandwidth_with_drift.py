import random as R
import operator
import numpy as np
import sys
sys.path.append("./../Collision_models/")
sys.path.append("./../Signal_strength_models")
sys.path.append("./../")
from simple_collision                       import simpleTransmisionModel
import randomized_field_based_collision_model 
import uniform_randomized_field_collision_model

from uniform_signal_strength                import uniformSignalStrength
from packet_statuses                        import PACKET_STATUS
from compressor_class                       import StatusMatrixCompressor
import physical_parameters as PAR
# All time is in milliseconds


## API-Function
def bandwidthWithDrift(nNodes, nPeriods, txPeriod_ms, jitterMax_ms, 
                            # parameters for spechial cases
                            driftMax_ppm= PAR.oscilator_drift_ppm,            
                            initial_startTimeOfset =0, 
                            packetDuration = PAR.packetDuration_ms, 
                            bitsPerMilisecond = PAR.bits_per_ms, 

                            receivedPacketProcessingTime= PAR.packetProcessingTime_ms,
                            failedPacketProcessingTime= PAR.packetProcessingTime_ms,
                            clockFrequency_kHz = PAR.crystalClockFrequency, 

                            # Topology of the network
                            signalStrengthModel = uniformSignalStrength, 

                            # Can be changed to reduce run-time
                            transmissionModel =  uniform_randomized_field_collision_model.randomizedFieldTransmisionModel, 
                            # transmissionModel =  randomized_field_based_collision_model.randomizedFieldTransmisionModel,
                            # Class to store results in
                            dataStorage_type = StatusMatrixCompressor  
                                                            ) :
                            

    PAR.init_physicalParameters( new_bits_per_ms= bitsPerMilisecond, new_packetDuration= packetDuration)
    driftMax_ms = (txPeriod_ms/1000) *   driftMax_ppm/(10**6)  # Drift from PPM is not suposed to be affected by clock frequency

    periodStartTimes = np.random.rand( nNodes)*initial_startTimeOfset
    start_times = ((np.random.rand(nNodes)*jitterMax_ms) + periodStartTimes)%txPeriod_ms
    result = dataStorage_type(nPeriods, nNodes)
    
    for i in range(nPeriods):
        periodStatuses = simulateTransmitionPeriod(  start_times, 
                                                     nNodes, 
                                                     txPeriod_ms, 
                                                     packetDuration,
                                                     bitsPerMilisecond,
                                                     receivedPacketProcessingTime, 
                                                     failedPacketProcessingTime, 
                                                     transmissionModel, 
                                                     signalStrengthModel)
        result.addToData(periodStatuses, start_times)
        start_times = ((np.random.uniform(low =0, high = jitterMax_ms, size= nNodes)) + periodStartTimes) % txPeriod_ms
        periodStartTimes += np.random.uniform( low = -(driftMax_ms), high = driftMax_ms, size =nNodes) 

        if result.is_done():
            break

    return result.getData()




#  IMPLEMENTATION
###########################################################################

def simulateTransmitionPeriod( start_times, nNodes, txPeriod_ms, packetDuration, bitsPerMilisecond,receivedPacketProcessingTime,  failedPacketProcessingTime, transmissionModel, signalStrengthModel): 
    indexes = np.argsort(start_times)
    start_times = start_times[indexes]
    nodeIDs = np.arange(nNodes)[indexes]
    to_node = nNodes # We say that the center node has the last ID 
    np.append(nodeIDs, to_node)
    receivedIDs = []
    ind =0
    packetStatuses= np.full( nNodes,PACKET_STATUS.NEVER_ARRIVED)
    while ind< nNodes: 
        transmisionStatus, receivingUntill = transmissionModel(ind, nNodes,  start_times, nodeIDs, packetDuration, bitsPerMilisecond, signalStrengthModel)
        if transmisionStatus == PACKET_STATUS.RECEIVED : 
            receivedIDs.append(nodeIDs[ind])
            busyUntil = receivingUntill + receivedPacketProcessingTime
        else: 
            busyUntil = receivingUntill + failedPacketProcessingTime
        packetStatuses[nodeIDs[ind]] = transmisionStatus
        while start_times[ind] <= busyUntil:
            ind +=1 
            if ind >= nNodes:
                break
    return packetStatuses
        














# For debugging purposes
# Runs several tests and writes the time used for each of them to results.txt
def main():
    fil = open("result.txt", 'a')
    fil.write("")
    fil.close()

    maxNodes = 1000
    # nNodes_list = [ i for i in range(1, maxNodes, max(1,maxNodes// 20) )]+ [maxNodes]
    nNodes_list = [10, 100, 500, 1000, 10000, 100000]
    print(nNodes_list)
    for nNodes in nNodes_list: 
        start = time.process_time()
        Mat = bandwidthWithDrift(nNodes, 800, nNodes*2, 10, initial_startTimeOfset=nNodes*2)
        diff = (time.process_time() -start)
        fil = open("result.txt", 'a')
        fil.write(str(nNodes)+" "+str(diff)+"\n")
        fil.close()
        print("nNodes =", nNodes)
        print("Received ", np.sum( Mat ==0))
        print("Time =",diff )
    

if __name__ == '__main__':

    import time 
    start = time.process_time()
    main()


    print("Total =", time.process_time() -start)
