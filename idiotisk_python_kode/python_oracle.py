"""
An oracle I will try to call from erlang to see if the library works
"""
import numpy as np
import scipy.linalg 

HIDDEN_matrix = np.random( (10,10) )

def get_score_of_list(list):
    if len(list) != 10:
        return "Wrong length"
    arr = np.array(list)
    score = np.sum( np.abs( HIDDEN_matrix*arr ) )
    return score



def crash_me(): 
    return "Hello" + 10 