#!/usr/bin/python3

import argparse
# import numpy as np
# import matplotlib.pyplot as plt
import json


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

print("Bandwidth: ", read_bw[0])
