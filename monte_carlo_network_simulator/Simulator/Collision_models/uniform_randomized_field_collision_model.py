import numpy as np
import random as R
import sys 
sys.path.append("./../")
import physical_parameters as PAR
from packet_statuses import PACKET_STATUS
import numpy as np
from functools import reduce


# Tests for corruption on all fields
def randomizedFieldTransmisionModel(senderStartIndex, to_node,  startTimes, nodeIDs, packetDuration,bitsPerMilisecond,  signalStrengthModel):

    

    if any_addressFieldColissions(senderStartIndex, to_node, startTimes,nodeIDs, packetDuration, signalStrengthModel):
        
        listeningUntil = startTimes[senderStartIndex]+ PAR.addressFieldPosition_ms+ PAR.addressFieldDuration_ms
        return PACKET_STATUS.ADDRESS_ERROR, listeningUntil

    is_lengthCorrupted, lengthField_new = lengthFieldColisions(senderStartIndex, to_node, startTimes,nodeIDs, packetDuration, bitsPerMilisecond,signalStrengthModel)
    listening_until = ((lengthField_new)/ bitsPerMilisecond)+ startTimes[senderStartIndex] + PAR.payloadFieldPosition_ms
    
    if  is_lengthCorrupted == True:
        return PACKET_STATUS.LENGTH_ERROR, listening_until

    elif any_payloadCollisions(senderStartIndex, to_node, startTimes,nodeIDs, packetDuration, signalStrengthModel):

        return PACKET_STATUS.PAYLOAD_ERROR, listening_until
    else:
        return PACKET_STATUS.RECEIVED, listening_until




# IMPLEMENTATION 
##############################################################################################################
def lengthFieldColisions(senderStartIndex, to_node, startTimes,nodeIDs, packetDuration,bitsPerMilisecond, signalStrengthModel):
    recvStart = startTimes[senderStartIndex]
    lengthField_start = recvStart+ PAR.lengthFieldPosition_ms
    lengthField_End = recvStart+ PAR.lengthFieldPosition_ms + PAR.lengthFieldDuration_ms
    corruptionMask = 0
    nNodes = len(startTimes)


    # Check forward in time
    ind = senderStartIndex +1
    while ind < nNodes and startTimes[ind] < lengthField_End:  # searching forwards TODO Handle end of list
        el = startTimes[ind]        

        overlap = lengthField_End- el
        corruptionMask = lengthCorruption(lengthField_start, el+ overlap, lengthField_End,corruptionMask  )
        ind+=1
        break

    

    # Checking earlier packets
    ind = senderStartIndex-1
    el = startTimes[ind]
    while ind >= 0 and startTimes[ind]+ packetDuration > lengthField_start : 
        el = startTimes[ind]
        

        corruptionMask = lengthCorruption(lengthField_start, lengthField_start, el + packetDuration, corruptionMask)
        ind -=1
        break

    if corruptionMask ==0: 
        return False, PAR.lengthField
    else: 
        return True, min( PAR.maxLengthField , PAR.lengthField ^corruptionMask ) 



def lengthCorruption( lengthField_start, overlap_start, overlap_end, packetEndTime_old):
    overlap_bits = (overlap_end-overlap_start)*PAR.bits_per_ms
    corruption_mask = R.randint(0, (1<< int(overlap_bits) ))
    displacement = (overlap_start -lengthField_start)*PAR.bits_per_ms
    packetEndTime_new = packetEndTime_old ^ ( corruption_mask << int(displacement) )& 0x3F
    return packetEndTime_new






def any_addressFieldColissions( senderStartIndex, to_node, startTimes,nodeIDs, packetDuration, signalStrengthModel):

    addressField_start = startTimes[senderStartIndex] + PAR.lengthFieldPosition_ms
    addressField_end = addressField_start + PAR.addressFieldDuration_ms    
    return is_fieldCorrupted(addressField_start,  
                             addressField_end,
                             senderStartIndex,  
                             startTimes, 
                             PAR.addressFieldDuration_ms, 
                             packetDuration, 
                             nodeIDs,
                             to_node,
                             signalStrengthModel)


def any_payloadCollisions( senderStartIndex, to_node, startTimes,nodeIDs, packetDuration, signalStrengthModel): 
    payloadField_start = startTimes[senderStartIndex] + PAR.payloadFieldPosition_ms
    payloadField_end = startTimes[senderStartIndex]+ packetDuration - PAR.crcDuration_ms
    payload_duration = payloadField_end - payloadField_start


    return is_fieldCorrupted(payloadField_start,  
                             payloadField_end,
                             senderStartIndex,  
                             startTimes, 
                             payload_duration, 
                             packetDuration, 
                             nodeIDs,
                             to_node,
                             signalStrengthModel)









# Test if an arbitraty field is corrupted by any of the other packages
def is_fieldCorrupted(field_start, field_end, senderIndex, startTimes, field_duration, packDuration, nodeIDs, toID, signalStrengthModel):
  
    # Check forward in time
    ind = senderIndex+1
    if ind < len(startTimes):
        el = startTimes[ind]
        while el < field_end:
            p_msCorrupted = PAR.p_msCorrupted
            if is_fieldCorruptedByPacket( field_start, field_end, el, el+ packDuration, p_msCorrupted): 
                return True
            ind +=1
            if ind >= len(startTimes):
                break
            el = startTimes[ind]



    # Check backward in time
    ind = senderIndex-1
    el = startTimes[ind]
    while el + packDuration > field_end and ind>=0 : 
        p_msCorrupted = PAR.p_msCorrupted
        el = startTimes[ind]
        if is_fieldCorruptedByPacket( field_start, field_end, el, el+ packDuration, p_msCorrupted):

            return True 
        ind -=1 
    return False





def is_fieldCorruptedByPacket(receivingField_start, receivingField_end, disturbance_start, disturbance_end, p_msCorrupted): 


    if receivingField_start>  disturbance_end:
        return False
    elif disturbance_start > receivingField_end: 
        return False
    else: 
        overlap1 = receivingField_end- disturbance_start
        overlap2 = disturbance_end - receivingField_start
        if overlap1 > overlap2:
            overlap = overlap1
        else:
            overlap = overlap2
    p_corrupted = 1 - (1- p_msCorrupted)**overlap
    if R.random() < p_corrupted:
        return True
    else:
        return False





