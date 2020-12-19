# Removes the random-looking name-endings of certain files if you know their common ending
# Moves the results to a subfolder named output (Does not create it)
import shutil
import subprocess as SP


ending = "Wii U"
encoding = ".mp3"

Proc = SP.Popen("ls", stdout =SP.PIPE)
list = Proc.communicate()[0].decode().split("\n")

for num, el in enumerate(list):
    if encoding in el and ending in el:
        new_name =el.split(ending)[0]+ending+encoding
        shutil.move(el, "./output/"+new_name)
        print(el, "./output/"+new_name)

