import os
import sys
import json

from pymatgen.core import Structure
from pymatgen.io.vasp.inputs import Kpoints
from BGWpy import QeScfTask

from util.qe import QE
from util.job_script import JS

sys.path.append("../QE")
from settings import *

structure   =   Structure.from_file("../AgSePh_prim.cif")

with open("../general.json") as fil:
    general_settings    =   json.load(fil)
with open("../qe.json") as fil:
    scf_settings    =   json.load(fil)
scf_settings["max_seconds"] =   210000
scf_settings["nbnd"]    =   160

scf_task    =   QeScfTask(
    dirname =   "../QE/01-scf",
    structure   =   structure,
    **general_settings,
    ngkpt   =   [14, 14, 2]
)
scf_task.input.update_params(scf_settings)

js  =   JS(header = {
    "job-name": "01-scf",
    "time": "72:00:00",
    "ntasks": general_settings["nproc"]
})
js.run_TMPDIR   =   False
scf_task.js =   js

scf_task.write()
scf_task.submit()

