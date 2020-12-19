
import numpy as np
from packet_statuses import PACKET_STATUS

# Hopefully gives less running-time
def simpleTransmisionModel(startIndex, to_node,  start_times, nodeIDs, packetDuration,bitsPerMilisecond,  signalStrengthModel): 
    
    # ! Readable version of the code
    # is_overlap = False

    # #TODO  Implement model for different signal strengths
    # if startIndex < len(start_times)-1 :
    #     is_overlap = is_overlap or start_times[startIndex]+ packetDuration > start_times[startIndex+1 ]
    # if startIndex > 0:
    #     is_overlap = is_overlap or start_times[startIndex-1] + packetDuration > start_times[startIndex]

    # if is_overlap == True: 
    #     packetStatus = PACKET_STATUS.PAYLOAD_ERROR
    # else: 
    #     packetStatus = PACKET_STATUS.RECEIVED



    # return packetStatus, start_times[startIndex]+ packetDuration


    #! Same functionality as the above code, but faster ( And that is needed )
    if ( ((startIndex < len(start_times)-1) and start_times[startIndex]+ packetDuration > start_times[startIndex+1 ] ) 
        or (( startIndex > 0) and start_times[startIndex-1] + packetDuration > start_times[startIndex]) ):
        return PACKET_STATUS.PAYLOAD_ERROR, start_times[startIndex]+ packetDuration
    else: 
        return PACKET_STATUS.RECEIVED, start_times[startIndex]+ packetDuration


