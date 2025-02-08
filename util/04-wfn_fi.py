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
nbands  =   160
#########################

structure   =   Structure.from_file("../ibrav.cif")

with open("../general.json") as fil:
    general_settings    =   json.load(fil)
general_settings["nproc"]   =   128
general_settings["qshift"]  =   [0, 0, 0]

with open("../qe.json") as fil:
    scf_settings    =   json.load(fil)
scf_settings["nbnd"]    =   nbands

wfn_flow    =   QeBgwFlow(
    dirname     =   f"../QE/04-wfn_fi{kstr}",
    structure   =   structure,
    ngkpt       =   ngkpt,

    savedir     =   f"../QE/01-scf/qe.save",

    **general_settings,
)
wfn_flow.wfntask.input.update_params(scf_settings)

js  =   JS(header = {
    "job-name": f"04-wfn_fi{kstr_job}",
    "time": "48:00:00",
    "nodes": 1,
    "ntasks": general_settings["nproc"],
    "partition": "compute"
})
wfn_flow.js =   js

wfn_flow.write()
if submit:
    wfn_flow.submit()


