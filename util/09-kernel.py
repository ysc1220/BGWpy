import os
import sys
import json

from pymatgen.core import Structure
from BGWpy import KernelTask
from util.job_script import JS

##########################
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
nodes   =   4
submit  =   False
if len(sys.argv) == 7:
    submit  =   bool(int(sys.argv[6]))
##########################
extra_lines     =   [
    "use_symmetries_coarse_grid",
    "screening_semiconductor"
]

with open("../general.json") as fil:
    general_settings    =   json.load(fil)
general_settings["nproc"]   =   128*nodes
suffix  =   "real"
if general_settings["flavor_complex"]:  suffix  =   "cplx"

structure   =   Structure.from_file("../ibrav.cif")

kernel_task =   KernelTask(
    dirname     =   f"../BGW/09-kernel{kstr}{nstr}",
    structure   =   structure,
    ngkpt       =   ngkpt,

    wfn_co_fname    =   f"../QE/04-wfn_fi{kstr}/wfn.{suffix}",
    eps0mat_fname   =   f"../BGW/07-epsilon{kstr}/eps0mat",
    epsmat_fname    =   f"../BGW/07-epsilon{kstr}/epsmat",

    nbnd_val        =   nval,
    nbnd_cond       =   ncon,

    extra_lines     =   extra_lines,

    **general_settings
)

js  =   JS(header = {
    "job-name": f"09-kernel{jstr}",
    "time":     "48:00:00",
    "nodes":    nodes,
    "ntasks":   general_settings["nproc"],
    "partition":    "compute"
})
js.before_job   =   "ulimit -s unlimited\n"
kernel_task.js   =   js

kernel_task.write()
if submit:
    kernel_task.submit()


