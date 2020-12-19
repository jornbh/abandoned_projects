# import cv2
import numpy as np
import matplotlib.pyplot as plt 
import  scipy.ndimage as scipy_img




# heightmap = np.zeros( (100,100))


# base_sigma = 1
# N = 2
# for i in range(N):
#     dh = np.random.random( heightmap.shape)
#     heightmap+= dh*( np.abs((1+heightmap)/ (1+np.mean(heightmap))) )
#     sigma = base_sigma*len(heightmap)/(30+(3*i/N))
#     heightmap =scipy_img.gaussian_filter(heightmap, sigma)


# print("range [",np.min(heightmap), np.max(heightmap), "]")
# plt.imshow( heightmap, cmap = "gray")
# plt.show()


# C:\Users\Jorn\Documents\code\Python\idiotisk_python_kode\Bilde_ting