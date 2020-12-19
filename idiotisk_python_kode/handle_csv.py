import numpy as np
from sys import stdin

csv_2D_list =   [line.strip().split(",") for line in stdin]
my_matrix = np.array(csv_2D_list ,ndmin=2, dtype=str)


print( my_matrix.shape )