import sys
import xml.etree.ElementTree as ET
import numpy as np
from util.data import HARTREE2EV

xml_fname   =   sys.argv[1]
tree    =   ET.parse(xml_fname)
root    =   tree.getroot().find("output").find("band_structure")
Exml    =   root.find("ks_energies").find("eigenvalues")

Es  =   []
for elem in Exml.text.split():
    Es.append(float(elem))
Es  =   np.array(Es)*HARTREE2EV

iHOMO   =   int(float(root.find("nelec").text))//2-1
idx     =   np.array(range(len(Es)))[np.logical_and(Es > Es[iHOMO]-2,
                                                    Es < Es[iHOMO]+4)]

print("Index of HOMO:", iHOMO)
print("Energies around HOMO:")
for i, E in enumerate(Es[iHOMO-20:iHOMO+20]):
    line    =   f"{i+iHOMO-20}\t{E:.2f}"
    if i == 20: line    +=  "\tHOMO"
    if i == 21: line    +=  "\tLUMO"
    print(line)
print("Indices within HOMO-2eV - HOMO+4eV:")
print(idx)

ibnd_min    =   idx[0]//4*4
ibnd_max    =   (idx[-1]//4+1)*4
print("Suggested ibnd:", ibnd_min, ibnd_max)

