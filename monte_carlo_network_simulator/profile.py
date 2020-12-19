import subprocess
import sys

# sys.path.append( "./Simulator/Network_models")
# sys.path.append( "./Simulator/Collision_models")
# sys.path.append( "./Simulator/Signal_strength_models")
# sys.path.append( "./Simulator/")

# # import cProfile
# # import re

# import bandwidth_with_drift



cmd = "py -m cProfile -s cumtime -o timeProfile.txt ./Simulator/Network_model/main.py "
# 
proc = subprocess.Popen(cmd, stderr = subprocess.PIPE)
result = proc.communicate()
print(result)
# import pstats
# p = pstats.Stats('timeProfile.txt')
# p.sort_stats('cumulative').print_stats(10)


