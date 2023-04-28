import os
import sys
import json

from pymatgen.core import Structure
from BGWpy import QeBgwFlow

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
general_settings["nproc"]   =   32
structure   =   Structure.from_file("../ibrav.cif")
with open("../qe.json") as fil:
    scf_settings    =   json.load(fil)
scf_settings["nbnd"]    =   300

CWD =   os.getcwd()
wfn_flow    =   QeBgwFlow(
    structure   =   structure,
    dirname     =   f"{CWD}/../QE/05-wfnq_co{kstr}",
    savedir     =   f"{CWD}/../QE/01-scf/qe.save",
    **general_settings,
    ngkpt   =   ngkpt,
)
wfn_flow.wfntask.input.update_params(scf_settings)

js  =   JS(header = {
    "job-name": f"05-wfnq_co{kstr_job}",
    "time": "48:00:00",
    "nodes": 1,
    "ntasks": general_settings["nproc"],
})
js.run_TMPDIR   =   False
wfn_flow.js =   js

wfn_flow.write()
wfn_flow.submit()


