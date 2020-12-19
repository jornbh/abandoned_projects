#!/bin/bash -e

# When called from crontab, not all variables are set => Swapping backgrounds does not work
# => We must set them ourselves => We use the magic internet-code


#Internet code (Works only on periodic tasks)
user=$(whoami)

fl=$(find /proc -maxdepth 2 -user $user -name environ -print -quit)
while [ -z $(grep -z DBUS_SESSION_BUS_ADDRESS "$fl" | cut -d= -f2- | tr -d '\000' ) ]
do
#   echo "$user $fl"
  fl=$(find /proc -maxdepth 2 -user $user -name environ -newer "$fl" -print -quit)
done

export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS "$fl" | cut -d= -f2-)

# End of internet code 



# Gives the directory of the source folder
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $DIR 
cd ../Pictures
PICTURE_PATH=$(pwd)

COMMAND="gsettings set org.gnome.desktop.background picture-uri file://"


# This is usually itterating over all files sorted randomly, but here it is only one file
ls $PICTURE_PATH | grep '.png\|.JPG\|.PNG' |sort -R | head -1 | while read PIC; do 
    $COMMAND$PICTURE_PATH/${PIC}
    echo $PICTURE_PATH/${PIC}
done

echo DONE
# echo "HELLO" >> ${DIR}/log.txt

