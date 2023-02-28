import os
import sys
import matplotlib.pyplot as plt

from util.basic import read_file

kstr    =   ""
for p in sys.argv[1:9]:
    kstr    +=  "_"+p

os.chdir("../BGW/10-absorption"+kstr)

plt.rcParams.update({"font.size": 16})
plt.figure(figsize = (10, 4))

spec    =   read_file("absorption_eh.dat")
plt.plot(spec[0], spec[1], "C0-")

stick   =   read_file("eigenvalues.dat")
norm    =   max(spec[1])/max(stick[1])*0.8

for row in zip(stick[0], stick[1]):
    if row[1] < 0.5:    plt.plot(row[0], 0, "C0o")
    else:   plt.plot([row[0], row[0]], [0, row[1]*norm], "C0-")

plt.xlabel("Energy (eV)")
plt.yticks([], [])
plt.ylabel("$\epsilon_2$")

plt.savefig("spec.png", bbox_inches = "tight")
