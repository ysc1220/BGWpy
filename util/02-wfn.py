import os
import sys
import json

from pymatgen.core import Structure
from BGWpy import QeBgwFlow

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
nodes   =   1
nbands  =   2000
########################


structure   =   Structure.from_file("../ibrav.cif")

with open("../general.json") as fil:
    general_settings    =   json.load(fil)
general_settings["PWFLAGS"] =   "-nk 4"
general_settings["nproc"]   =   128*nodes
general_settings["qshift"]  =   [0, 0, 0]

with open("../qe.json") as fil:
    scf_settings        =   json.load(fil)
scf_settings["nbnd"]    =   nbands

wfn_flow    =   QeBgwFlow(
    dirname     =   f"../QE/02-wfn{kstr}",
    structure   =   structure,
    ngkpt       =   ngkpt,

    savedir     =   "../QE/01-scf/qe.save",

    rhog_flag   =   True,

    **general_settings,
)
wfn_flow.wfntask.input.update_params(scf_settings)

js  =   JS(header = {
    "job-name": f"02-wfn{kstr_job}",
    "time":     "48:00:00",
    "nodes":    nodes,
    "ntasks":   general_settings["nproc"],
    "partition":    "compute"
})
wfn_flow.js =   js

wfn_flow.write()
if submit:
    wfn_flow.submit()

