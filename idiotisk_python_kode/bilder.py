import os
import subprocess
import sys
import last_ned_en_hel_serie
import threading
import queue
#!    curl _url_ > filnavn.ending 
#!          Gjør det mulig å laste ned bilder fra nettet
# cmd = [ 'curl', URL ]
# output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
# URL = "https://www.youtube.com/watch?v=OXGBsSc6f-c"
# cmd = ["ls"]
# output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]

def main():
    URL = "https://serebii.net/"
    #print(Out)
    Q = queue.Queue()
    dive(URL, URL, 1, Q)
    links=[]
    while  not Q.empty(): 
        links.append(Q.get())
    links.sort()
    for i in set(links):
        print(i)
        pass

def dive(URL, link, depth, Q):
    cmd = ["curl", link]
    print("DIVE")
    Raw = subprocess.Popen( cmd,stdout=subprocess.PIPE, stderr = subprocess.DEVNULL ).communicate()[0] # quiet
    
    #Raw = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0] #noisy 
    #print(Raw)
    try:
        Out = Raw.decode("ISO-8859-1") # For pokemon-site(?)
    except:
        print("ERROR")
        return 
    new_links = []
    for line in Out.split("\n"):
        # if "img src" in line.lower():
        #     pic_URL = (line.split("img src=")[1].split("\"")[1])
        #     info = line.split(pic_URL)[0]
        #     try:
        #         Name = info.split("users/")[1].split("/")[1].split("\">")[0]
        #         print(Name.ljust(30,' ')+ pic_URL)
        #     except:
        #         if "www." not in pic_URL:
        #             #print(line)
        #             print(URL[:-1]+pic_URL)
        #         else:
        #             print(pic_URL)
        if "href" in line:
            try:
                link = line.split("href=")[1].split("\"")[1]
                if "www." not in link and "/" in link:
                    #print(URL[:-1]+link)
                    new_links.append(URL[:-1]+link)
                # print(line)
            except:
                #print("ERROR", line.split("href=")[1])
                pass
        # if ".png" in line:
        #print(line)   
    threads = []
    if depth <= 0:
        pass
    else: 
        all_links = []
        
        for new_link in new_links:
            threads.append(threading.Thread( target = dive, args=(URL, new_link, depth-1, Q)))  # Dette ser ut som noe man bør paralellisere
            threads[-1].start()
    for i in threads:
        i.join()
    for i in new_links:
        Q.put(i)



if __name__ == '__main__':
    main()