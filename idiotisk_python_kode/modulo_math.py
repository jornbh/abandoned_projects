import numpy as np 
import matplotlib.pyplot as plt
from math import pi
from sys import stdin


def sgn(x): 
    if x > 0: 
        return 1
    else: 
        return -1
frequencies = np.array([ (2-  i%4) * (i)  for i in range(3,100, 2)])

Tops = []
Bottoms = []
for freq in frequencies: 
    base = 1/(freq*2)
    # print(base)
    extremals= np.arange(base, 2*sgn(freq), 1/freq )
    signs = np.sin(extremals*np.pi*freq)

    Tops.append( [   el for ind, el in enumerate(extremals) if signs[ind] >0])
    Bottoms.append([ el for ind, el in enumerate(extremals) if signs[ind] <0])

# print(Tops)
print("Start")
for list_top in Tops: 
    for el_top in list_top: 
        for list_bot in Bottoms: 
            for el_bot in list_bot: 
                if el_bot == el_top: 
                    print("Yay", el_bot, el_top)
print("End")
print(frequencies)
print(np.sin(frequencies* np.pi*(3/2)))
print(np.sin(frequencies* np.pi*(1/2)))
