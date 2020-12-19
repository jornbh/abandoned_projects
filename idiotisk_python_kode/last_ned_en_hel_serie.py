import os
import subprocess
import sys
import shutil
# Laster ned en serie fra crunchyroll, fordi det er fremdeles bedre enn piratkopiering
# Kopierer det også til en pasende directory
def main():
    args = sys.argv
    if len(args) != 2 and (len(args) != 4 and args[2].strip() != "--skip"):
        print('Not right')
        print(args)
        return False
    
    URL = args[1]
    Name = URL.split(".com/")[1]
    Path = "/home/jorn/Documents/Annet/janky_stuff/crunchyroll"
    os.system("mkdir " + Path + "/"+ Name)
    cmd = [ 'curl', URL ]
    output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]

    Base = URL.split(".com")[0] + ".com"
    lines = output.decode("utf-8").split('\n')


    urls = get_urls( Base, lines)
    urls.reverse()
    if args[2].strip() == "--skip":
        skip_ind = int(args[3])
        urls  = urls[skip_ind:]
    for i in urls:
        pass
    #! uncomment to download
    old_files = subprocess.Popen( ["ls"], stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split("\n")
    download_for_all(urls, old_files, Path+"/"+Name)


def move_files(old_files, Path):
    all_files = subprocess.Popen( ["ls"], stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split("\n")
    new_files =[]
    for i in all_files:
        if i not in old_files:
            new_files.append(i.strip())
    for i in new_files:
        shutil.move(i, Path+"/"+ i) 
    return 1


def get_urls(Web_page, lines):
    i =0
    output =[]
    urls = []
    for line in lines:
        line = line.strip()
        if "<a href" in line:
            if "episode" in line.lower():
                Processed_line = line.strip().split('\"')
                urls.append(Processed_line[1])
                output.append(line)
                i+=1
    Final = []
    for line in urls:
        Final.append(Web_page+line)
    return Final


def download_for_all(urls, old_files, Path):

    for j in urls:
        os.system(" youtube-dl --sub-lang enUS  --write-sub " +j)
        move_files(old_files, Path)
    return True


if __name__ == '__main__':
    main()
