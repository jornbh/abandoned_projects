# Script for puting in the script that will activate the wallpaper cycling as a crontab-task

# We assume we are in the same folder as activateCycle.sh

# Make an empty crontab file if there is none 
crontab -e << EOF
^[wq
EOF

# Make sure we are in the correct folder, regardless of where we have been called from
SRC_LOCATION="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $SRC_LOCATION


SLEEPER_FILE="activateCycle.sh"
PERIOD="*/120 * * * *" # The script will be called every second hour 
RUN_FILE=${SRC_LOCATION}/${SLEEPER_FILE}
TASK_LINE="${PERIOD} bash $RUN_FILE"


# Add the sleeper file to crontab 
echo "$TASK_LINE" 
crontab_contents=$(crontab -l)
# crontab -l  | read crontab_contents
if [[ $crontab_contents == *"$TASK_LINE"* ]]
then 
echo "Line already in crontab: $TASK_LINE"

else 

echo "Line not in crontab, adding it now"
(crontab -l; echo "$TASK_LINE") | crontab -


fi




# Unzip all the pictures and move them to the correct folder
cd ../Pictures
unzip Absolutely\ disgusting.zip
cd Absolutely\ disgusting
mv * .. # All immages are now in Pictures
cd ..
rm Absolutely\ disgusting.zip
rm -r Absolutely\ disgusting