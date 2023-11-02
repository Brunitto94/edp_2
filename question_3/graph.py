#!/usr/bin/python3

import argparse
import numpy as np
import matplotlib.pyplot as plt
import json


def get_read_lat_deciles(data):
    job = data["jobs"][0]["read"]

    comp_lat = [value for percentile, value in job["clat_ns"]["percentile"].items() if int(float(percentile)) % 10 == 0]
    lat = [value for percentile, value in job["lat_ns"]["percentile"].items() if int(float(percentile)) % 10 == 0]
        
    return comp_lat, lat


parser = argparse.ArgumentParser()
parser.add_argument("input", type=argparse.FileType("r"), help="The file containing the json output")
parser.add_argument("-o", "--output", type=str, help="Output filename")
args = parser.parse_args()

# Extract useful data from the json output
data = json.load(args.input)
args.input.close()

completion_latency, latency = get_read_lat_deciles(data)

plt.style.use("../plot_params.mplstyle")

fig, ax = plt.subplots(1, figsize=(7, 7), layout="constrained")

x = np.arange(1, len(completion_latency) + 1)

# ax.plot(x, completion_latency, marker="o", label="Completion latency")
ax.plot(x, latency, marker="o")#, label="Latency")
ax.set_title("Latencies for a task with different request sizes")
ax.set_xlabel("Decile")
ax.set_ylabel("Latency (ns)")
# ax.legend()

if args.output is not None:
    plt.savefig(args.output, dpi=300)
else:
    plt.show()
