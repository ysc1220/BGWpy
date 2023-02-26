import os
import sys
import json

from pymatgen.core import Structure
from BGWpy import KernelTask

params  =   []
for p in sys.argv[1:6]:
    params.append(int(p))
ngkpt       =   params[:3]
nval, ncon  =   params[3:]
kstr    =   ""
for k in ngkpt:
    kstr    +=  "_"+str(k)
nstr    =   f"_{nval}_{ncon}"
jstr    =   (kstr+nstr).replace("_", "")

with open("../general.json") as fil:
    general_settings    =   json.load(fil)
general_settings["nproc"]   =   1

structure   =   Structure.from_file("../"+general_settings["cifname"])

kernel_task =   KernelTask(
    dirname     =   f"../BGW/09-kernel{kstr}{nstr}",
    structure   =   structure,
    ngkpt       =   ngkpt,

    wfn_co_fname    =   f"../QE/02-wfn{kstr}/wfn.real",
    eps0mat_fname   =   f"../BGW/07-epsilon{kstr}/eps0mat",
    epsmat_fname    =   f"../BGW/07-epsilon{kstr}/epsmat",

    nbnd_val        =   nval,
    nbnd_cond       =   ncon,

    extra_lines     =   [
        "use_symmetries_coarse_grid",
        "screening_semiconductor"
    ],

    **general_settings
)

from util.job_script import JS
js  =   JS(header = {
    "job-name": f"09-kernel{jstr}",
    "time":     "168:00:00",
    "ntasks":   general_settings["nproc"]
})
js.run_TMPDIR   =   False
js.before_job   =   "ulimit -s unlimited\n"
kernel_task.js   =   js

kernel_task.write()
kernel_task.submit()


