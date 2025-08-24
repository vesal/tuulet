#!/bin/bash 
source /home/vesal/aurinko/saa/venv/bin/activate 
cd /home/vesal/aurinko/saa
echo -e "=======================\n$(date)\n" >> saa.txt
python saa.py >> saa.txt
echo -e "\n$(date)\n" >> saa.txt

echo -e "$(date)" >> sel.txt
DISPLAY=:99 xvfb-run -a python sel.py >> sel.txt
#echo -e "\n$(date)\n" >> sel.txt
