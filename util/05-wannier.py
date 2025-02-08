import os
import sys
import json

from pymatgen.core import Structure
from BGWpy import QeWfnTask
from BGWpy.Wannier90.wannier90 import Wannier90Input

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

wfntask     =   QeWfnTask(
    dirname     =   f"../QE/05-wannier",
    structure   =   structure,
    ngkpt       =   ngkpt,

    savedir     =   f"../QE/01-scf/qe.save",

    **general_settings,
)
wfntask.input.update_params(scf_settings)

os.chdir(wfntask.dirname)
wanniertask     =   Wannier90Input(
    structure   =   structure,
    nbnd        =   146,
    nwann       =   132,
    kbounds     =   [
        [0.5, 0, 0],
        [0, 0, 0],
        [0.5, 0.5, 0.5],
        [0, 0.5, 0.5],
        [0, 0, 0],
        [0, 0.5, 0]
    ],
    klabels     =   ["Z", "G", "M", "E", "G", "X"],
    mp_grid     =   ngkpt,
    kpts        =   [row[0] for row in wfntask.input.params.kpts],
    projections =   ["Ag : s;d", "S : p", "C: p", "O: p"],
)
with open("qe.win", "w") as fil:
    fil.write(str(wanniertask))

'''
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
'''

