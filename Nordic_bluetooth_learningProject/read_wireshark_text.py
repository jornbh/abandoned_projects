# A simple text-analyzer for reading the wireshark-output



################    PARAMETERS             #############################
PACKETS_EXPECTED = 10000
LIST_OF_EXPCTED_PHRASES_IN_PACKET = ["Mr Garrison"]
LIST_OF_ILLEGAL_PHRASES_IN_PACKET = ["Malformed"]

ID ="aa:12:34:56:78:9a"



#####################################################################"##"
from sys import stdin


def get_wireshark_lines():
    out = []
    for line in stdin:
        if line.strip() != "":
            FW = line.strip().split()[0]
            if FW != "Bluetooth" and FW != "Nordic" and FW != "No." and FW != "Frame":
                if FW !="[Malformed":
                    out.append(line.strip())
    return out

def count_packets(ID, lines): 
    relevant_lines =[ i for i in lines          if ID in i]
    malformed      =[ i for i in relevant_lines if not is_valid_custom_test(i)       ]
    return (len(relevant_lines), len(malformed))


def is_valid_custom_test(test_packet):
    good = True
    for j in LIST_OF_EXPCTED_PHRASES_IN_PACKET:
        if j not in test_packet:
            
            good = False
            break
    if good == True: 
        for j in LIST_OF_ILLEGAL_PHRASES_IN_PACKET:
            if j in test_packet:
                good = False
                break
    return good



def main():
    
    lines= get_wireshark_lines()
    packets_received, malformed_packets = count_packets(ID, lines)

    print("Received packets:", packets_received,"/",PACKETS_EXPECTED)
    print("Malformed packets:", malformed_packets)
    print("Packets that never arrived:", PACKETS_EXPECTED-packets_received)
    print( 100*packets_received/ (packets_received+ malformed_packets) , "%  of the received packets were correct")
    print(100*packets_received/ (PACKETS_EXPECTED) , "%  Arrived correctly")


main()



