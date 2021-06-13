#!/usr/bin/python

import time
import os

prevDay = -1
while True:
    currDay = time.gmtime().tm_mday
    currWeekDay = time.gmtime().tm_wday
    if currWeekDay == 6 and currDay != prevDay:
        print("Sending recipes...")
        os.system("python3 main.py -c 4 -v -r")
        print("Recipes sent!\n")
        prevDay = currDay
    time.sleep(60 * 5)
