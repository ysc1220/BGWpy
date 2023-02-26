import os
import sys
import json

from pymatgen.core import Structure
from BGWpy import EpsilonTask

ngkpt   =   []
kstring =   ""
for k in sys.argv[1:4]:
    ngkpt.append(int(k))
    kstring +=  "_"+k

structure   =   Structure.from_file("../AgSePh_prim.cif")

epsilon_input_files =   {
    "wfn_fname":    f"../QE/02-wfn{kstring}/wfn.real",
    "wfnq_fname":   f"../QE/03-wfnq{kstring}/wfn.real",
    "ngkpt": ngkpt,
    "qshift": [0.001, 0.001, 0],
    "ecuteps": 10,
    "scfout_fname": "../QE/01-scf/scf.out"
}

with open("../general.json") as fil:
    general_settings    =   json.load(fil)

epsilon_task    =   EpsilonTask(
    dirname =f"../BGW/07-epsilon_{ngkpt[0]}_{ngkpt[1]}_{ngkpt[2]}",
    structure   =   structure,
    **epsilon_input_files,
    **general_settings
)
from util.job_script import JS
js  =   JS(header = {
    "job-name": f"07-epsilon{ngkpt[0]}{ngkpt[1]}{ngkpt[2]}",
    "time": "168:00:00",
    "ntasks": general_settings["nproc"]
})
js.run_TMPDIR   =   False
epsilon_task.js =   js

epsilon_task.write()
epsilon_task.submit()
