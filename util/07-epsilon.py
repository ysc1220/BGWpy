import os
import sys
import json

from pymatgen.core import Structure
from BGWpy import EpsilonTask

from util.job_script import JS

########################
ngkpt   =   []
kstr    =   ""
kstr_job    =   ""
for k in sys.argv[1:4]:
    ngkpt.append(int(k))
    kstr        +=  "_"+k
    kstr_job    +=  k
submit  =   False
if len(sys.argv) == 5:
    submit  =   bool(int(sys.argv[4]))
nodes   =   8
#########################

structure   =   Structure.from_file("../ibrav.cif")

with open("../general.json") as fil:
    general_settings    =   json.load(fil)
general_settings["nproc"]   =   128*nodes
suffix  =   "real"
if general_settings["flavor_complex"]:  suffix  =   "cplx"

epsilon_task    =   EpsilonTask(
    dirname     =   f"../BGW/07-epsilon{kstr}",
    structure   =   structure,
    ngkpt       =   ngkpt,

    wfn_fname   =   f"../QE/02-wfn{kstr}/wfn.{suffix}",
    wfnq_fname  =   f"../QE/03-wfnq{kstr}/wfn.{suffix}",

    **general_settings,
)

js  =   JS(header = {
    "job-name": f"07-epsilon{kstr_job}",
    "time":     "48:00:00",
    "nodes":    nodes,
    "ntasks":   general_settings["nproc"],
    "partition":    "compute"
})
epsilon_task.js =   js

epsilon_task.write()
if submit:
    epsilon_task.submit()

