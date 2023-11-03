#!/usr/bin/python3

import argparse
import numpy as np
import matplotlib.pyplot as plt
import json

from collections import defaultdict


def get_parallel_stats(data):
    nb_procs = []
    read_bws = []
    write_bws = []
    summed_read_bw = defaultdict(int)
    summed_write_bw = defaultdict(int)
    
    for job in data["jobs"]:
        nb_proc = int(job["job options"]["numjobs"])
        nb_procs.append(nb_proc)

        read_bw = job["read"]["bw"]
        read_bws.append(read_bw)
        summed_read_bw[nb_proc] += read_bw

        write_bw = job["write"]["bw"]
        write_bws.append(write_bw)
        summed_write_bw[nb_proc] += write_bw

    return {
        "nb_procs": nb_procs,
        "read": read_bws,
        "write": write_bws,
        "summed_read": summed_read_bw,
        "summed_write": summed_write_bw,
    }


parser = argparse.ArgumentParser()
parser.add_argument("input", type=argparse.FileType("r"), help="The file containing the json output")
parser.add_argument("-o", "--output", type=str, help="Output filename prefix")
args = parser.parse_args()

# Extract useful data from the json output
proc_data = json.load(args.input)
args.input.close()

stats = get_parallel_stats(proc_data)

# First plot
nb_procs = stats["summed_read"].keys()

read_means = [summed_bw / int(nb_proc) for nb_proc, summed_bw in stats["summed_read"].items()]
write_means = [summed_bw / int(nb_proc) for nb_proc, summed_bw in stats["summed_write"].items()]

x = np.arange(len(nb_procs))

plt.style.use("../plot_params.mplstyle")

fig, (ax_read, ax_write) = plt.subplots(1, 2, figsize=(14, 7), layout="constrained")

ax_read.bar(x, read_means)
# ax_read.set_title("Mean read bandwidth for jobs with 1 to 8 processes", wrap=True)
# ax_read.set_xlabel("Number of processes")
# ax_read.set_ylabel("Mean bandwidth (KiB/s)")
ax_read.set_title("Bande passante moyenne en lecture pour des jobs utilisant 1 à 8 processus", wrap=True)
ax_read.set_xlabel("Nombre de processus")
ax_read.set_ylabel("Bande passante moyenne (ko/s)")
ax_read.set_xticks(x)
ax_read.set_xticklabels(nb_procs)

ax_write.bar(x, write_means)
# ax_write.set_title("Mean write bandwidth for jobs with 1 to 8 processes", wrap=True)
# ax_write.set_xlabel("Number of processes")
# ax_write.set_ylabel("Mean bandwidth (KiB/s)")
ax_write.set_title("Bande passante moyenne en écriture pour des jobs utilisant 1 à 8 processus", wrap=True)
ax_write.set_xlabel("Nombre de processus")
ax_write.set_ylabel("Bande passante moyenne (ko/s)")
ax_write.set_xticks(x)
ax_write.set_xticklabels(nb_procs)

if args.output is not None:
    plt.savefig("mean_" + args.output, dpi=300)
else:
    plt.show()

# Second plot
x = [int(nb_proc) for nb_proc in nb_procs]
summed_read_bw = stats["summed_read"]
summed_write_bw = stats["summed_write"]

fig, (ax_read, ax_write) = plt.subplots(1, 2, figsize=(14, 7), layout="constrained")

ax_read.plot(x, summed_read_bw.values(), marker="o")
# ax_read.set_title("Cumulative read bandwidth for jobs with 1 to 8 parallel processes", wrap=True)
# ax_read.set_xlabel("Number of processes")
# ax_read.set_ylabel("Bandwidth (KiB/s)")
ax_read.set_title("Bande passante cumulée en lecture pour des jobs utilisant 1 à 8 processus", wrap=True)
ax_read.set_xlabel("Nombre de processus")
ax_read.set_ylabel("Bande passante (ko/s)")
ax_read.set_xticks(x)

ax_write.plot(x, summed_write_bw.values(), marker="o")
# ax_write.set_title("Cumulative write bandwidth for jobs with 1 to 8 parallel processes", wrap=True)
# ax_write.set_xlabel("Number of processes")
# ax_write.set_ylabel("Bandwidth (KiB/s)")
ax_write.set_title("Bande passante cumulée en écriture pour des jobs utilisant 1 à 8 processus", wrap=True)
ax_write.set_xlabel("Nombre de processus")
ax_write.set_ylabel("Bande passante (ko/s)")
ax_write.set_xticks(x)

if args.output is not None:
    plt.savefig("cumulative_" + args.output, dpi=300)
else:
    plt.show()
