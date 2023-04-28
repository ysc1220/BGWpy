import os
import sys
import json

from pymatgen.core import Structure
from BGWpy import EpsilonTask

from util.job_script import JS

ngkpt   =   []
kstr    =   ""
kstr_job    =   ""
for k in sys.argv[1:4]:
    ngkpt.append(int(k))
    kstr        +=  "_"+k
    kstr_job    +=  k

with open("../general.json") as fil:
    general_settings    =   json.load(fil)
structure   =   Structure.from_file("../ibrav.cif")
general_settings["nproc"]   =   128*24
js  =   JS(header = {
    "job-name": f"07-epsilon{kstr_job}",
    "time":     "48:00:00",
    "nodes":    24,
    "ntasks":   general_settings["nproc"],
    "partition":    "compute"
})
js.run_TMPDIR   =   False

epsilon_task    =   EpsilonTask(
    dirname     =   f"../BGW/07-epsilon{kstr}",
    structure   =   structure,
    wfn_fname   =   f"../QE/02-wfn{kstr}/wfn.real",
    wfnq_fname  =   f"../QE/03-wfnq{kstr}/wfn.real",
    ngkpt       =   ngkpt,
    kshift      =   [0.5, 0.5, 0,5],
    **general_settings,
)

epsilon_task.js =   js

epsilon_task.write()
#epsilon_task.submit()

