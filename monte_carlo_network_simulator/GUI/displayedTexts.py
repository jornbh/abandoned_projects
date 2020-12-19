import sys
sys.path.append('..\\Simulator')

from packet_statuses import PACKET_STATUS
#Change this file to display change the text in the program 


# GENERAL TEXTS
#############################################################################

simulatorTitle = "Simple simulator"

# Top-bar oparations

exitProgram = "Exit"

#############################################################################
# SIMULATOR-PAGE TEXTS
#############################################################################

# Universal input-parameters
nNodes                       = "Number of nodes"                                    
nRetransmits                 = "Number of packets sent per node"                    
txPeriod                     = "Transmission period [ms]"                           
jitterMax_ms                 = "Max jitter [ms]"                                    
driftMax_ppm                 = "Max clock drift [ppm]"                              
packetLength_bits            = "Packet length [bits]"                               
bitsPerMilisecond            = "Bit rate [kbps]"                                    
is_nodesSyncronized          = "Are nodes synchronized at start [True/False]"       
receivedPacketProcessingTime = "Receiver deadtime between successfull receives [ms]"
failedPacketProcessingTime   = "Receiver deadtime between faulty packets [ms]"      



# Semi-universal input-parameters
numberOfSimulations    = "Number of simulations"
faultTolerance_percent = "Percentile-limit [%]"


#Page Titles 
title_bandwidthAtTransmittingNode = "Bandwidth at transmitting node" 
title_bandwidthAtGatewayNode = "Bandwidth at gateway node"             
title_checkInTime            = "Checkin-time"

# DESCRIPTIONS 
#############################################################################
description_bandwidthAtTransmittingNode= """
The three line visualizes the spread of the simulation result
over different values of "number of nodes" \n
Max, Min and Avg are calculated from all the samples from all the simulation"""





description_checkinTime = ("The boxplot shows the variation in the simulation results.\n" +
                            "The box (if visible) will encompass the average sample value (periods before Check-In)\n" +
                            "and reach from the 24.65 percentile to the 75.35 percentile\n" +
                            "i.e. 50% of the samples. The blue line is the median of the samples\n" +
                            "The whiskers are user-defined and will reach from 0 percentile to the \"100-minus-fault_tolerence\" percentile. \n"+
                            "Samples that lie outside these limits are showed as dots/outliers\n"+
                            "x-Percentile: Value where x % of all measured points are less that or equal to x "
                            )


desxription_bandwidthAtGatewayNode = ("The plots shows bandwidth and interference at the gateway\n" +
                            "i.e. the combined bandwidth of all node-gateway paths. \n" +
                            "The percentages are all percentages of all packets transmitted.\n" +
                            "CRC errors are packets with corrupt PDU-header, Payload or CRC fields.\n" +
                            "Address errors are packets with corrupt Access Address.\n" +
                            "Arrived while busy are packets that were dropped because they arrived during processing time."+
                            "x-Percentile: Value where x % of all measured points are less that or equal to x "
                            
        )



#############################################################################
# PRINTED RESULTS FROM SIMULATION ( White box underneath input-parameters)
#############################################################################
preSimulationMessage = "Press start to begin simulation..."

progressStatusLabel = "Status: "
progressStatusFirstRunningMessage = "Running"
progressStatusWhenFinished = "Finished"

Outliers=     "Outliers: "
UpperWhisker ="Upper Whisker: "
UpperBox=     "Upper Box: "
Median =      "Median: "
LowerBox=     "Lower Box: "
LowerWhisker= "Lower Whisker: "

simulationTimeLabel = "Simulation-time: "
logFilesLocationLabel = 'Log-files location'

#############################################################################
# TEXT FOR PLOTS
#############################################################################
# Gateway 
gateway_plotTitle       =  "Bandwidth and interference at the Gateway Node"     
gateway_bandwidth_axis  = "Bandwidth\n[kbps]"  
gateway_CRCErrors_axis=  "CRC\nerrors\n[%]"
gateway_addressErrors_axis= "Access\nAddress\nerrors\n[%]"
gateway_arrivedWhileBusy_axis="Arrived\nwhile busy\n[%]"
gateway_nNodes_axis = "Number of nodes"

         

gateway_upperLine_fun        =    lambda faultTolerance_percent: str( 100- faultTolerance_percent)+ "-Percentile"  
gateway_averageLine      =     "Average"   
gateway_lowerLine_fun        =     lambda faultTolerance_percent: str(faultTolerance_percent)+"-Percentile"




# #Transmitter 
transmitter_plotTitle = "Bandwidth and interference at the Gateway Node"
transmitter_nNodes_axis = "Number of nodes"        
transmitter_bandwidth_axis  = "Bandwidth\n[kbps]"       

transmitter_upperLine_fun      =  lambda faultTolerance_percent: str( 100- faultTolerance_percent)+ "-Percentile"  
transmitter_averageLine        =   "Average" 
transmitter_lowerLine_fun      =  lambda faultTolerance_percent: str(faultTolerance_percent)+"-Percentile"






#############################################################################
# Description text at the start of the Log files
##########################################################################################################################################################
logDescription_checkInTime_parsed = ("Each row is a simulation and each column is a node.\n" +
                        "The value of each element is the check-in time for a node in a simulation.\n" +
                        "If a node never made check-in, that instance is removed from the matrix.\n"
                        "See RawResults for results grouped by simulations, including instances of never-checked-in\n")

logDescription_bandwidthAtGatewayNode_parsed = ("First array is the x-values(number of nodes) of all datapoints\n" +
                        "2nd-4th array is the y-values of max, avg and min bandwidth\n" +
                        "5th-7th array is the y-values of max avg, min CRC-errors.\n" +
                        "8th-9th array is the y-values of max, avg, min Access Address-errors\n" +
                        "10th-12th array is the y-values of max, avg, min Never Arrived-occurences\n")

logDescription_bandwidthAtTransmittingNodes_parsed = ( "The 1st array is the x-values (number of nodes) of each data point \n" +
                                    "The 2nd-4th arrays are y-values of max, avg, and min values of bandwidth corresponding to the x-values\n")

logDescription_checkInTime_raw = ("Rows = A single simulation (Lasts until all nodes checks in or until we reach \" number of packets per node \"\n" +
                                "Columns = Transmitting Nodes\n" +
                                "Values = Number of periods before that node checked in\n")

logDescription_bandwidthAtGatewayNode_raw = ("Rows = performance of 1 node during the whole simulation \n"
                    +"Columns = the different outcomes of a packet send \n"
                    +"Values = how many packets had that specific outcome during the simulation\n" +
                    "Explanation of values: <Packet outcome: Column number>: " +
                    str(list(PACKET_STATUS))+ '\n')

logDescription_bandwidthAtTransmittingNodes_raw = ("Rows = Periods\n" +
                    "Columns = Transmitting Nodes.\n" +
                    "Values = Result of the packet sent by this node\n" +
                    "Explanation of values:  <Packet outcome: Column number>: " +
                    str(list(PACKET_STATUS))+ '\n')

########################################################################################################################

# About-text
aboutLabel = "About..."
aboutText = (
"""Simple Simulator\n
Version v0.1\n
Copyright 2018 Nordic Semiconductor ASA

Simulates a circle/sphere topology where the gateway is 
equidistant to all the transmittors. Advertisment only on one channel."""
)

