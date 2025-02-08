import os
import sys
import json

from pymatgen.core import Structure
from BGWpy import QeScfTask

from util.job_script import JS

######################
ngkpt   =   [12, 4, 4]
submit  =   False
if len(sys.argv) == 2:
    submit  =   bool(int(sys.argv[1]))
######################

structure   =   Structure.from_file("../ibrav.cif")

with open("../general.json") as fil:
    general_settings    =   json.load(fil)

with open("../qe.json") as fil:
    scf_settings        =   json.load(fil)

scf_task    =   QeScfTask(
    dirname     =   "../QE/01-scf",
    structure   =   structure,
    ngkpt       =   ngkpt,
    **general_settings,
)
scf_task.input.update_params(scf_settings)

js  =   JS(header = {
    "job-name": "01-scf",
    "time":     "48:00:00",
    "ntasks":   general_settings["nproc"],
    "partition":    "compute"
})
js.run_TMPDIR   =   False

scf_task.js =   js

scf_task.write()
if submit:
    scf_task.submit()

