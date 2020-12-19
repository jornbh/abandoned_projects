# Will add  swap_background.sh as a crontab task when it is time

# Check if it's to early to start the script
today=$(date +%s)
release_date=$(date -d 2019-01-20 +%s)

if [ $today -le $release_date ];
then
    exit  # Too early
fi  





# Add a new task to crontab 

# Path to called dir
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ITERATION_FILE="swap_background.sh"
PERIOD="*/5 * * * *" # Run every 5th minute
FULL_PATH=${DIR}/${ITERATION_FILE}
CRONTAB_LINE="${PERIOD} bash $FULL_PATH"


echo "$CRONTAB_LINE" 
crontab_contents=$(crontab -l)
if [[ $crontab_contents == *"$CRONTAB_LINE"* ]]
then 

echo "Line already in crontab: $CRONTAB_LINE"

else 

echo "Line not in crontab, adding it now"
(crontab -l; echo "$CRONTAB_LINE") | crontab -


fi


cd ~
cd Desktop
echo "To remove these files go to $DIR and check the REDME" > STOP_THE_WALLPAPER.txt