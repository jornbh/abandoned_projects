# DEFAULT PHUSICAL LARAMETERS 


# From nRF252 datasheet
crystalClockFrequency = 16* 10**6 # 16 MHz
oscilatorDrift_RC_PPM = 250 
oscilatorDrift_crystal_PPM = 40 # +- Maximum allowed frequency tollerance for using the BLE radio
oscilator_drift_ppm = oscilatorDrift_crystal_PPM
 # 30 ppm is a rough estimate from measuremetns ) 



# Just a default value ( Can be changed by the user)
bits_per_ms = 1000

# Just an assumption, who knows if this is correct
p_bitCorrupted = 1/4.0
p_msCorrupted = 1-  (1- p_bitCorrupted)**bits_per_ms



# Delete this
packetSize_bits = 369 # bits
packetDuration_ms = packetSize_bits/bits_per_ms
packetProcessingTime_ms = 0.133



# From the bluetooth low energy standard for advertisement packets (Only correct if bits_per_ms are correct)
addressFieldPosition_ms=   8/bits_per_ms
addressFieldDuration_ms=  32/bits_per_ms
lengthFieldPosition_ms =  48/bits_per_ms
lengthFieldDuration_ms =   6/bits_per_ms
payloadFieldPosition_ms=  56/bits_per_ms
crcDuration_ms         =  24/bits_per_ms


#  From BLE standard 
maxLengthField = 37 
lengthField = packetSize_bits- (8 +32 +16) # Value the length field needs to have for the packet to be packetSize bits long



def init_physicalParameters( 
                                new_bits_per_ms= bits_per_ms,
                                new_packetSize_bits = packetSize_bits,
                                new_packetDuration = packetDuration_ms,
                                new_p_bitCorrupted = p_bitCorrupted,
                                new_oscliatorDrift_ppm= oscilatorDrift_crystal_PPM,
                                new_packetProcessingTime_ms = packetProcessingTime_ms
                                ): 


    
    global bits_per_ms
    global p_bitCorrupted
    global p_msCorrupted
    global packetSize_bits
    global packetDuration_ms
    global packetProcessingTime_ms
    global addressFieldPosition_ms
    global addressFieldDuration_ms
    global lengthFieldPosition_ms
    global lengthFieldDuration_ms
    global payloadFieldPosition_ms
    global crcDuration_ms
    global lengthField
    global oscilator_drift_ppm
    if new_packetDuration != packetDuration_ms: 
        new_packetSize_bits =  round(new_packetDuration/ new_bits_per_ms)


    bits_per_ms     = new_bits_per_ms
    packetSize_bits = new_packetSize_bits
    p_bitCorrupted  =  new_p_bitCorrupted
    
    packetDuration_ms = new_packetSize_bits/ new_bits_per_ms

    addressFieldPosition_ms=   8/new_bits_per_ms
    addressFieldDuration_ms=  32/new_bits_per_ms
    lengthFieldPosition_ms =  48/new_bits_per_ms
    lengthFieldDuration_ms =   6/new_bits_per_ms
    payloadFieldPosition_ms=  56/new_bits_per_ms
    crcDuration_ms         =  24/new_bits_per_ms

    lengthField = packetSize_bits- (8 +32 +16) # Value the length field needs to have for the packet to be packetSize bits long

    packetProcessingTime_ms = new_packetProcessingTime_ms
    oscilator_drift_ppm = new_oscliatorDrift_ppm