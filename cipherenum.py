from enum import Enum

###########################
# Cipher Enumerated Types #
###########################

class CipherType(Enum):
    RAIL_FENCE = 1

    def __str__(self):
        return self.name


    
