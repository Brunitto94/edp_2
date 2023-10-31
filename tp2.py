#!/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import json,glob

file = "output/rand_q1_1proc.json"
file = open(file,"r")
data = json.load(file)

p = np.arange(0,101,12.5)
variables = ["read","write"]

list = glob.glob("output/*.json")
for file in list:
    data=json.load(open(file,"r"))
    read_bw = []
    write_bw = []
    for job in data["jobs"]:
        read_bw.append(job[variables[0]]["bw"])
        write_bw.append(job[variables[1]]["bw"])
    plt.figure()
    plt.plot(read_bw)
    plt.plot(write_bw)
plt.show()
