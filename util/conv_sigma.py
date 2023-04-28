import os
import matplotlib.pyplot as plt

direcs  =   []
for direc in list(os.walk("../BGW"))[0][1]:
    if "08-sigma" in direc:
        direcs.append(direc)
direcs  =   sorted(direcs)

BGs =   []
for direc in sorted(direcs):
    direc
    iHOMO, HOMO, LUMO   =   0, 0, 0
    with open("../BGW/"+direc+"/sigma.out") as fil:
        for line in fil:
            if "Highest occupied band" in line:
                iHOMO   =   int(line.split()[6])

    with open("../BGW/"+direc+"/eqp1.dat") as fil:
        for line in fil:
            if line.split()[1] == str(iHOMO):
                HOMO    =   float(line.split()[3])
            if line.split()[1] == str(iHOMO+1):
                LUMO    =   float(line.split()[3])
                break

    print(direc, HOMO, LUMO, LUMO-HOMO)
    BGs.append(LUMO-HOMO)

plt.plot(direcs, BGs, "o")
plt.ylabel("Band gap (eV)")

plt.savefig("conv_sigma.png", bbox_inches = "tight")

