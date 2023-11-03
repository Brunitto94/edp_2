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
parser.add_argument("-s", "--sequential", type=argparse.FileType("r"), help="The file containing the sequential output")
parser.add_argument("-r", "--random", type=argparse.FileType("r"), help="The file containing the random output")
parser.add_argument("-o", "--output", type=str, help="Output file suffix")
args = parser.parse_args()

seq_data = json.load(args.sequential)
args.sequential.close()

rand_data = json.load(args.random)
args.random.close()


seq_read_bw, seq_write_bw = get_rw_bw(seq_data)
rand_read_bw, rand_write_bw = get_rw_bw(rand_data)

plt.style.use("../plot_params.mplstyle")

# First plot. Two figures, one for sequential the other for random
fig, (ax_read, ax_write) = plt.subplots(1, 2, figsize=(14, 7), layout="constrained")

x = np.arange(0, 101, 12.5)
ax_read.plot(x, seq_read_bw, marker="o", label="séquentiel")
ax_read.plot(x, rand_read_bw, marker="o", label="aléatoire")

# ax_read.set_title("Bandwidth for I/O operations with 100 to 0% of reads")
# ax_read.set_xlabel("Percentage of reads")
# ax_read.set_ylabel("Bandwidth (KiB/s)")
ax_read.set_title("Bande passante pour des tâches I/O avec 100 à 0% de lectures", wrap=True)
ax_read.set_xlabel("Pourcentage de lectures")
ax_read.set_ylabel("Bande passante (ko/s)")
ax_read.set_xticks(x)
ax_read.set_xticklabels([f"{100 - p}%" for p in x])
ax_read.legend()

ax_write.plot(x, seq_write_bw, marker="o", label="séquentiel")
ax_write.plot(x, rand_write_bw, marker="o", label="aléatoire")

# ax_write.set_title("Bandwidth for I/O operations with 0 to 100% of writes", wrap=True)
# ax_write.set_xlabel("Percentage of writes")
# ax_write.set_ylabel("Bandwidth (KiB/s)")
ax_write.set_title("Bande passante pour des tâches I/O avec O à 100% d'écritures", wrap=True)
ax_write.set_xlabel("Pourcentage d'écritures")
ax_write.set_ylabel("Bande passante (ko/s)")
ax_write.set_xticks(x)
ax_write.set_xticklabels([f"{p}%" for p in x])
ax_write.legend()

if args.output is not None:
    plt.savefig("separated_" + args.output, dpi=300)
else:
    plt.show()


# Second plot, all lines on the same plot + log scale
fig, ax = plt.subplots(1, figsize=(8, 6), layout="constrained")

x = np.arange(0, 101, 12.5)

ax.plot(x, seq_read_bw, marker="o", label="lecture séquentielle")
ax.plot(x, rand_read_bw, marker="o", label="lecture aléatoire")

ax.plot(x, seq_write_bw, marker="o", label="écriture séquentielle")
ax.plot(x, rand_write_bw, marker="o", label="écriture aléatoire")

ax.set_title("Bande passante pour des tâches I/O avec 100 à 0% de lectures", wrap=True)
ax.set_xlabel("Pourcentage de lectures")
ax.set_ylabel("Bande passante (ko/s)")
ax.set_xticks(x)
ax.set_xticklabels([f"{p}%" for p in x])
# ax.set_yscale("symlog")
ax.set_ylim(0, 1.1 * ax.get_ylim()[1])
# ax.legend(loc="lower center")
ax.legend()

if args.output is not None:
    plt.savefig("merged_" + args.output, dpi=300)
else:
    plt.show()
