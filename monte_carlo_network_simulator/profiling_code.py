""" To profile the code import cProfile and re into main.py and run:
$ python3 -m cProfile -o [output_save_path] main.py

This will run the code and store the results in [output_save_path] In this script we can load and print the results. 
Our experience is that the profiling should be done without the GUI because we are mainly interested in optimizing the actual simulation and not the graphical rendering"""


import cProfile
import re
import pstats

output_save_path = 'profiling.txt'


p = pstats.Stats(output_save_path)
p.sort_stats('time').print_stats(30)
p.sort_stats('cumulative').print_stats(30)
p.sort_stats('ncalls').print_stats(30)