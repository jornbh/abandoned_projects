import numpy as np 
import matplotlib.pyplot as plt
from math import pi
from sys import stdin
step = 0.001
X = np.arange(0, 1, step)

multples = [
            1,
            -2, 
            -3,
            # -7*3,
            # -3,
            # 45, 
            # -15
            ]

w = 2*pi

for i in multples: 
    Y = np.sin( w*i*X)
    plt.plot(X,Y)
plt.show()