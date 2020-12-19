import re
from operator import __add__
print("HI")


with open("vakt_html.txt", "r") as f: 
    lines = [ line.strip() for line in f ]

    reg_start = re.compile('.*<div class="d-text">.*')
    reg_end = re.compile("</div>")
    starts = ([reg_start.findall(line) for line in lines])
    ends = ([reg_end.findall(line) for line in lines])
    pairs = map( __add__, starts, ends)
    for i in range(len(starts) -2):
        if len(starts[i]) >0:
            print(lines[i+1])
    # print( *list(pairs), sep="\n")

 
