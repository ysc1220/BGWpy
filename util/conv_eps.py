import os

direcs  =   []
for direc in list(os.walk("../BGW"))[0][1]:
    if "07-epsilon" in direc:
        direcs.append(direc)

for direc in sorted(direcs):
    with open("../BGW/"+direc+"/epsilon.out") as fil:
        for line in fil:
            if "Head of Epsilon" in line:
                eps =   float(line.split()[6])
                print(direc, eps)
                break
