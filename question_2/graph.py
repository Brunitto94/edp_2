#!/usr/bin/python3

import argparse
import numpy as np
import matplotlib.pyplot as plt
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
parser.add_argument("-o", "--output", type=str, help="Output filename")
args = parser.parse_args()

# Extract useful data from the json output
var_data = json.load(args.input)
args.input.close()

var_read_bw, var_write_bw = get_rw_bw(var_data)

block_sizes = []
for job in var_data["jobs"]:
    block_sizes.append(job["job options"]["bs"])

plt.style.use("../plot_params.mplstyle")

# Plot the data
fig, (ax_read, ax_write) = plt.subplots(1, 2, figsize=(14, 7), layout="constrained")

x = np.arange(len(var_read_bw))

ax_read.plot(x, var_read_bw, marker="o")

ax_read.set_title("Bande passante en lecture pour des tailles de requêtes allant jusqu'à 1Mo", wrap=True)
ax_read.set_xlabel("Taille de requête (Octets)")
ax_read.set_ylabel("Bande passante (ko/s)")
ax_read.set_xticks(x)
ax_read.set_xticklabels(block_sizes)

ax_write.plot(x, var_write_bw, marker="o")

# ax_write.set_title("Write bandwidth for request sizes up to 1MB")
ax_write.set_title("Bande passante en écriture pour des tailles de requêtes allant jusqu'à 1Mo", wrap=True)
ax_write.set_xlabel("Taille de requête (Octets)")
ax_write.set_ylabel("Bande passante (ko/s)")
ax_write.set_xticks(x)
ax_write.set_xticklabels(block_sizes)

if args.output is not None:
    plt.savefig(args.output, dpi=300)
else:
    plt.show()
