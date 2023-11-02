#!/usr/bin/python3

import argparse
import numpy as np
import matplotlib.pyplot as plt
import json,glob

def get_rw_bw(data):
    read_bw = []
    write_bw = []
    
    for job in data["jobs"]:
        read_bw.append(job["read"]["bw"])
        write_bw.append(job["write"]["bw"])

    return read_bw, write_bw


parser = argparse.ArgumentParser()
parser.add_argument("input", type=argparse.FileType("r"), help="The file containing the json output")
# parser.add_argument("-o", "--output", type=str, help="Output filename")
args = parser.parse_args()

# Extract useful data from the json output
var_data = json.load(args.input)
args.input.close()

read_bw, write_bw = get_rw_bw(var_data)
"""
p = np.array([1,2,4])
list=glob.glob("split_*.json")
read = np.zeros(3)

for i,cur in zip(range(3),list) :
    a,_ = get_rw_bw(json.load(open(cur,"r")))
    read[i] = a[0]

plt.plot(p,read)
plt.show()
"""
print("Bandwidth: ", read_bw[0])
