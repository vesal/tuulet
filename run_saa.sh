#!/bin/bash 
source /home/vesal/aurinko/saa/saa/bin/activate 
cd /home/vesal/aurinko/saa
echo -e "=======================\n$(date)\n" >> saa.txt
python saa.py >> saa.txt
