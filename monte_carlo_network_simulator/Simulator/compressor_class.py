import numpy as np
from packet_statuses import PACKET_STATUS

from abc import ABC # Makes abstract base classes

# A compressor can be taken into the network model in order to reduce the amount of stored data 
# It needs to implement all the functions of the Base compressor




class BaseCompressor(ABC):
    
    def __init__(self, nNodes, nPeriods):
        ...

    # Takes in numpy-arrays
    def addToData(self, statuses_ofPeriod, startTimes_ofPeriod): # Sorted by nodeID
        ...


    def getData(self):
        ...
    
    def is_done(self): 
        return False





# Default compressor; Returns a matrix of the statuses for each packet, but no start-times
class StatusMatrixCompressor(BaseCompressor): 
    data = np.array(0)
    index =0

    def __init__(self, nPeriods, nNodes):
        self.data = np.full(( nPeriods, nNodes ), PACKET_STATUS.NEVER_ARRIVED)
        self.index =0

    def addToData(self, numpyArrayofStatuses, numpyArrayOfStartTimes): 
        self.data[self.index, :] = numpyArrayofStatuses
        self.index +=1

    def getData(self):
        return self.data


    

class RawStatusesAndStartTimes(BaseCompressor):

    statuses = np.array(0)
    start_times =np.array(0) 
    index =0

    def __init__(self, nPeriods, nNodes):
        self.statuses = np.full(( nPeriods, nNodes ), PACKET_STATUS.NEVER_ARRIVED)
        self.start_times = np.full(( nPeriods, nNodes), -1.0)
        self.index =0

    def addToData(self, numpyArrayofStatuses, numpyArrayOfStartTimes): 
        self.statuses[self.index, :] = numpyArrayofStatuses
        self.start_times[self.index, :] = numpyArrayOfStartTimes

        self.index +=1

    def getData(self):
        return self.statuses, self.start_times



import numpy as np
class CountPacketOfAllTypesForEachNode(BaseCompressor): 

    def __init__(self, nPeriods, nNodes):
        maxStatus = max(map(int,PACKET_STATUS))
        self.counters = np.full( (nNodes,maxStatus +1), 0)
        

    def addToData(self, numpyArrayofStatuses, numpyArrayOfStartTimes): 
        for i,j in enumerate(numpyArrayofStatuses):
            self.counters[ i,j] +=1
    
    def getData(self):
        return self.counters




class FirstCheckinTimes(BaseCompressor):
    def __init__(self, nPeriods, nNodes): 
        self.checkinTimes = np.full(nNodes, None) 
        self.notCheckedIn = set ([i for i in range(nNodes)])
        self.numCheckedIn=0
        self.nNodes = nNodes
        self.period =0

    def addToData(self, numpyArrayofStatuses, numpyArrayOfStartTimes): 
        checkedIn = []
        self.period +=1
        for i in self.notCheckedIn: 
            if numpyArrayofStatuses[i] == PACKET_STATUS.RECEIVED: 
                self.checkinTimes[i] = self.period
                checkedIn.append(i)
        if checkedIn != []:
            for i in checkedIn:
                self.notCheckedIn.remove(i) 
            self.numCheckedIn+= len(checkedIn)
        
    def getData(self):
        return self.checkinTimes 
    def is_done(self): 
        return self.numCheckedIn ==self.nNodes