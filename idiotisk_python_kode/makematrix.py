#!/usr/bin/env python3
# Can take the pasted output from a spreadsheet and make a latex-matrix
from sys import stdin
import re
#litterally took 3 mins
print("\\begin{bmatrix}")
cellMat = []
maxWidth = 0
maxes = None
for line in stdin:
    line = line.replace(" ", "\t")
    List = line.strip().split("\t")
    if maxes == None: 
        maxes = [ len(i) for i in List]
    for ind, el in enumerate(List): 
        maxes[ind] = max( maxes[ind], len(el))
    cellMat.append( List)
    maxWidth = max( maxWidth, len( max( cellMat[-1], key = len))    )

adjust = lambda x: x.rjust(maxWidth)
out = [ i for i in cellMat]



for ind, el in enumerate(cellMat):
    # out[ind] = [i.rjust(maxes(ind)) for i in el]
    # print(el)
    out[ind] = [i.rjust(maxes[ind2]) for ind2, i in enumerate(el)]


for i in out: 
    print("\t", " & ".join(i), "\\\\")

print("\\end{bmatrix}")