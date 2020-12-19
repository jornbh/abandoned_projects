import enum



class PACKET_STATUS(enum.IntEnum):
    RECEIVED        = 0
    PAYLOAD_ERROR   = 1
    ADDRESS_ERROR   = 2
    LENGTH_ERROR    = 3
    NEVER_ARRIVED   = 4

    @staticmethod
    def list():
        return {'RECEIVED', 0, 'PAYLOAD_ERROR',1,'ADDRESS_ERROR',2,'LENGTH_ERROR',3,'NEVER_ARRIVED',4}

    #enum.auto() can be used if everything is suposed to be unique


