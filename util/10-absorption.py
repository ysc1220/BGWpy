import os
import sys
import json

from pymatgen.core import Structure
from BGWpy import AbsorptionTask

params  =   []
for p in sys.argv[1:9]:
    params.append(int(p))
ngkpt       =   params[:3]
ngkpt_fi    =   params[3:6]
nval, ncon  =   params[6:8]

kstr    =   ""
for k in ngkpt:
    kstr    +=  "_"+str(k)
kstr_fi =   ""
for k in ngkpt_fi:
    kstr_fi +=  "_"+str(k)
nstr    =   f"_{nval}_{ncon}"
jstr    =   (kstr+nstr).replace("_", "")

with open("../general.json") as fil:
    general_settings    =   json.load(fil)

structure   =   Structure.from_file("../"+general_settings["cifname"])

absorption_task =   AbsorptionTask(
    dirname     =   f"../BGW/10-absorption{kstr}{kstr_fi}{nstr}",
    structure   =   structure,
    ngkpt       =   ngkpt,

    wfn_co_fname    =   f"../QE/02-wfn{kstr}/wfn.real",
    wfn_fi_fname    =   f"../QE/02-wfn{kstr_fi}/wfn.real",
    wfnq_fi_fname   =   f"../QE/03-wfnq{kstr_fi}/wfn.real",

    eps0mat_fname   =   f"../BGW/07-epsilon{kstr}/eps0mat",
    epsmat_fname    =   f"../BGW/07-epsilon{kstr}/epsmat",
    eqp_fname       =   f"../BGW/08-sigma{kstr}/eqp1.dat",

    bsexmat_fname   =   f"../BGW/09-kernel{kstr}{nstr}/bsexmat",
    bsedmat_fname   =   f"../BGW/09-kernel{kstr}{nstr}/bsedmat",

    nbnd_val        =   nval,
    nbnd_cond       =   ncon,
    nbnd_val_co     =   nval+2,
    nbnd_cond_co    =   ncon+2,
    nbnd_val_fi     =   nval,
    nbnd_cond_fi    =   ncon,

    extra_lines     =   [
        "no_symmetries_coarse_grid",
        "no_symmetries_fine_grid",
        "no_symmetries_shifted_grid",
        "screening_semiconductor",
        "use_velocity",
        "gaussian_broadening",
        "eqp_co_corrections"
    ],

    extra_variables =   {
        "energy_resolution":    0.15
    },

    **general_settings
)

from util.job_script import JS
js  =   JS(header = {
    "job-name": f"10-absorption{jstr}",
    "time":     "168:00:00",
    "ntasks":   general_settings["nproc"]
})
js.run_TMPDIR   =   False
js.before_job   =   "ulimit -s unlimited\n"
absorption_task.js  =   js

absorption_task.write()
#absorption_task.submit()


