import sys

from pymatgen.core import Structure
from pymatgen.io.vasp.inputs import Kpoints

filname     =   "../AgSePh_prim.cif"

structure   =   Structure.from_file(filname)

for nks_per_vol in range(50, 1200, 50):
    kpoints     =   Kpoints.automatic_density_by_vol(structure, nks_per_vol)
    print(nks_per_vol, kpoints.kpts)

