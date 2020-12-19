import subprocess
from sys import stdin

def get_from_url(url, includes =["*"], no_includes=[]):
    html = run_cmd( [ "curl", url])
    return_values = filter_lines(html,includes, no_includes)
    return return_values


def filter_lines(html, includes, no_includes):
    first_step = include_lines(html, includes)
    out = remove_lines(first_step, no_includes)    
    return out



def include_lines( html, includes):
    wholes= [term for term in includes if "*" not in term]
    out = [i for i in html if     any(j in i for j in wholes)]
    rest =[i for i in html if not any(j in i for j in includes)]
    splits = [ i.split("*") for i in includes if "*" in i]
    for line in rest:
        for [term1,term2] in splits:
            p1 = line.find(term1)
            if p1 != (-1):
                p2 = line[p1+1:].find(term2)
                if p1 < p2:  
                    out.append(line)
                    break
    return out
        
def remove_lines(html, removes):
    wholes = [i for i in removes if "*" not in i]
    first = [ i for i in html if not any(j in i for j in wholes)]
    splits = [ i.split("*") for i in removes if "*" in i]
    out = []
    for line in first:             
        add = True
        for [term1, term2] in splits:
            p1 = line.find(term1)
            if p1 != -1:
                if line[p1+1:].find(term2) > p1:
                    add = False 
                    break

        if add== True:
            out.append(line)
    return out





def extract_url(line,url):
    link = line.split("href=")[1].split("\"")[0]
    if "www." not in link:
        slpit1 = url.slpit(".")
        base = split1[0]
        ending = split1[1].split("/")[0]
        return base+ending+link
    else:
        return link

def run_cmd(command_list):
    retur_val = subprocess.Popen( command_list, stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split("\n")
    return retur_val



def main():
    html = [line for line in stdin]
    url = "https://stackoverflow.com/questions/3368969/find-string-between-two-substrings"

    get_from_url(url, includes=["img"])

if __name__ == '__main__':
    main()