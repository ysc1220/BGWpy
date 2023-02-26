import os
import sys
import json

from pymatgen.core import Structure
from BGWpy import QeBgwFlow

from util.job_script import JS

ngkpt   =   []
for k in sys.argv[1:4]:
    ngkpt.append(int(k))

structure   =   Structure.from_file("../AgSePh_prim.cif")
with open("../general.json") as fil:
    general_settings    =   json.load(fil)
with open("../qe.json") as fil:
    scf_settings    =   json.load(fil)
scf_settings["max_seconds"] =   210000
scf_settings["nbnd"]    =   160

CWD =   os.getcwd()
dirname =   f"{CWD}/../QE/02-wfn_{ngkpt[0]}_{ngkpt[1]}_{ngkpt[2]}"
savedir =   f"{CWD}/../QE/01-scf/qe.save"
wfn_flow    =   QeBgwFlow(
    dirname     =   dirname,
    structure   =   structure,
    savedir     =   savedir,
    **general_settings,
    ngkpt   =   ngkpt,
)
wfn_flow.wfntask.input.update_params(scf_settings)

js  =   JS(header = {
    "job-name": f"02-wfn{ngkpt[0]}{ngkpt[1]}{ngkpt[2]}",
    "time": "72:00:00",
    "ntasks": general_settings["nproc"]
})
js.run_TMPDIR   =   False
wfn_flow.js =   js

wfn_flow.write()
#wfn_flow.submit()

#with open("LOG", "a") as fil:
#    wfn_flow.report(file = fil)

