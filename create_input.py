#!/bin/python3
import os,sys
num_jobs=9
f = open(sys.argv[1]+".config","w")
f.write("[global]\n")
f.write("runtime=60\n")
f.write("direct=1\n")
f.write("directory=./\n")
f.write("filesize=1G\n")
f.write(f"blocksize=16K\n")
f.write("readwrite=randrw\n")
f.write("loops=5\n")
f.write("\n")

for i in range(num_jobs):
    f.write(f"[job{i:.1f}]\n")
    f.write("numjobs=4\n")
    f.write(f"rwmixwrite={12.5*i}\n")

    #f.write("bssplit=4k/30:16K/60:64/10\n")
    f.write("filename=bench\n")
    #f.write("bssplit=\n")
    f.write("\n")
