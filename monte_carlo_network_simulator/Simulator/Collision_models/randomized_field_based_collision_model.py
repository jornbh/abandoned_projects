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
    return newLengthFieldCollision( senderStartIndex, to_node, startTimes,nodeIDs, packetDuration, bitsPerMilisecond, signalStrengthModel)
   
######################################################################


def updateProb(x,y):
    return (1-x)*y + x*(1-y)

def newLengthFieldCollision(senderStartIndex, to_node, startTimes,nodeIDs, packetDuration, bitsPerMs, signalStrengthModel):
    p_bits_forward, p_bits_backward = gatherProbabilities(senderStartIndex, to_node, startTimes,nodeIDs, packetDuration, bitsPerMs, signalStrengthModel)
    

    p_tot = [ 0 for i in p_bits_forward]
    temp =0 
    for ind,el in enumerate(p_bits_forward):
        temp = updateProb(temp, el)
        p_tot[ind] = temp

    temp =0
    for ind, el in reversed(list(enumerate(p_bits_backward))):
        temp = updateProb(temp, el)
        p_tot[ind] = updateProb(p_tot[ind], temp)
    

    bits = np.random.binomial(1, p=p_tot)
    compress = lambda tot, new: new + (tot<<1)
    corruptionMask = reduce(compress, bits, 0)

    if corruptionMask == 0:
        return False, 0
    else:
        return True, min(PAR.maxLengthField, PAR.lengthField^corruptionMask)





def gatherProbabilities( senderStartIndex, to_node, startTimes,nodeIDs, packetDuration, bitsPerMs, signalStrengthModel):
    recvStart = startTimes[senderStartIndex]
    lengthField_start = recvStart+ PAR.lengthFieldPosition_ms
    lengthField_End = recvStart+ PAR.lengthFieldPosition_ms + PAR.lengthFieldDuration_ms
    nNodes = len(startTimes)
    get_n_bits = lambda start,end: int(round(((end-start))*bitsPerMs))
    n_bits = get_n_bits(lengthField_start, lengthField_End)

    p_bits_forward = [0 for i in range(n_bits+1)] # prob of bit i is given by all before it

    p_bits_backward = [0 for i in range(n_bits+1)]
    getOverlap = lambda start, end: get_n_bits(   max( start, lengthField_start), min(end, lengthField_End))

    # Check backwards
    ind = senderStartIndex-1
    el = startTimes[ind]
    while ind >= 0 and startTimes[ind]+ packetDuration > lengthField_start : 
        el = startTimes[ind]
        lastOverlap = getOverlap(el, el+packetDuration)
        p_corrupted = signalStrengthModel( senderStartIndex, to_node, nodeIDs[ind])
        p_bits_backward[lastOverlap] = updateProb(p_bits_backward[lastOverlap], p_corrupted )
        ind -=1

    ind = senderStartIndex+1

    while ind < nNodes and startTimes[ind] < lengthField_End:  # searching forwards TODO Handle end of list
        el = startTimes[ind]
        firstOverlap = n_bits - getOverlap(el, el+packetDuration)     
        p_corrupted = signalStrengthModel( senderStartIndex, to_node, nodeIDs[ind])
        p_bits_forward[firstOverlap] = updateProb(p_bits_forward[firstOverlap], p_corrupted)
        ind+=1
    

    return p_bits_forward[:-1], p_bits_backward[1:]


######################################################################





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
        p_msCorrupted = signalStrengthModel(nodeIDs[senderIndex], toID,nodeIDs[ind] )
        while el < field_end:
            if is_fieldCorruptedByPacket( field_start, field_end, el, el+ packDuration, p_msCorrupted): 
                return True
            ind +=1
            if ind >= len(startTimes):
                break
            el = startTimes[ind]



    # Check backward in time
    ind = senderIndex-1
    el = startTimes[ind]
    p_msCorrupted = signalStrengthModel(nodeIDs[senderIndex], toID, nodeIDs[ind] )
    while el + packDuration > field_end and ind>=0 : 
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





