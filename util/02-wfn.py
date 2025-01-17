import os
import sys
import json

from pymatgen.core import Structure
from BGWpy import QeBgwFlow

from util.job_script import JS

ngkpt   =   []
for k in sys.argv[1:4]:
    ngkpt.append(int(k))

with open("../general.json") as fil:
    general_settings    =   json.load(fil)
general_settings["qshift"]  =   [0, 0, 0]
general_settings["nproc"]   =   128
structure   =   Structure.from_file("../ibrav.cif")
with open("../qe.json") as fil:
    scf_settings    =   json.load(fil)
scf_settings["nbnd"]    =   2000

CWD =   os.getcwd()
dirname =   f"{CWD}/../QE/02-wfn_{ngkpt[0]}_{ngkpt[1]}_{ngkpt[2]}"
savedir =   f"{CWD}/../QE/01-scf/qe.save"
wfn_flow    =   QeBgwFlow(
    dirname     =   dirname,
    structure   =   structure,
    savedir     =   savedir,
    **general_settings,
    ngkpt   =   ngkpt,
    kshift  =   [0.5, 0.5, 0.5]
)
wfn_flow.wfntask.input.update_params(scf_settings)

js  =   JS(header = {
    "job-name": f"02-wfn{ngkpt[0]}{ngkpt[1]}{ngkpt[2]}",
    "time": "48:00:00",
    "nodes": 1,
    "ntasks": general_settings["nproc"],
    "partition": "compute"
})
js.run_TMPDIR   =   False
wfn_flow.js =   js

wfn_flow.write()
wfn_flow.submit()


