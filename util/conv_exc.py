import os

import matplotlib.pyplot as plt

direcs  =   []
for direc in list(os.walk("../BGW"))[0][1]:
    if "10-absorption" in direc:
        direcs.append(direc)
direcs  =   sorted(direcs)

Es  =   []
for direc in direcs:
    with open("../BGW/"+direc+"/eigenvalues.dat") as fil:
        lines   =   fil.readlines()
    Eexc    =   float(lines[4].split()[0])
    print(direc, Eexc)
    Es.append(Eexc)

plt.plot(direcs, Es, "o")
plt.ylabel("First excitation energy (eV)")

plt.savefig("conv_exc.png", bbox_inches = "tight")

