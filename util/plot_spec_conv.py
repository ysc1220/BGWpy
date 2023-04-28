import os
import sys
import numpy as np
import matplotlib.pyplot as plt

from util.basic import read_file

direcs  =   []
for direc in list(os.walk("../BGW"))[0][1]:
    if "10-absorption" in direc:
        direcs.append(direc)

plt.rcParams.update({"font.size": 16})
plt.figure(figsize = (10, 4))

for direc in sorted(direcs):
    print(direc)
    spec    =   read_file(f"../BGW/{direc}/absorption_eh.dat")
    norm    =   max(spec[1])
    plt.plot(spec[0], np.array(spec[1])/norm,
             label = direc.replace("10-absorption_", ""))

plt.legend()
plt.xlabel("Energy (eV)")
plt.yticks([], [])
plt.ylabel("$\epsilon_2$")

plt.savefig("spec_conv.png", bbox_inches = "tight")


