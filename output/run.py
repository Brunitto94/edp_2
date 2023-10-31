#!/bin/python3

import glob,os

list = glob.glob('../config/*.config')

for cur in list:
    os.system(f"fio --output-format=json --output={cur[16:-7]}.json {cur}") 
