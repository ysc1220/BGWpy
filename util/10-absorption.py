import os
import sys
import json

from pymatgen.core import Structure
from BGWpy import AbsorptionTask

###########################
params  =   []
for p in sys.argv[1:11]:
    params.append(int(p))
ngkpt       =   params[:3]
ngkpt_fi    =   params[3:6]
nval, ncon  =   params[6:8]
nval_co, ncon_co    =   params[8:10]
submit  =   False
if len(sys.argv) >= 12:
    submit  =   bool(int(sys.argv[11]))
nproc       =   32
if len(sys.argv) == 13:
    nproc   =   int(sys.argv[12])
###########################

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
general_settings["nproc"]   =   nproc
suffix  =   "real"
if general_settings["flavor_complex"]:  suffix  =   "cplx"

structure   =   Structure.from_file("../ibrav.cif")

absorption_task =   AbsorptionTask(
    dirname     =   f"../BGW/10-absorption{kstr}{kstr_fi}{nstr}",
    structure   =   structure,
    ngkpt       =   ngkpt,

    wfn_co_fname    =   f"../QE/04-wfn_fi{kstr}/wfn.{suffix}",
    wfn_fi_fname    =   f"../QE/04-wfn_fi{kstr_fi}/wfn.{suffix}",
    wfnq_fi_fname   =   f"../QE/03-wfnq{kstr_fi}/wfn.{suffix}",

    eps0mat_fname   =   f"../BGW/07-epsilon{kstr}/eps0mat",
    epsmat_fname    =   f"../BGW/07-epsilon{kstr}/epsmat",
    eqp_fname       =   f"../BGW/08-sigma{kstr}/eqp1.dat",

    bsexmat_fname   =   f"../BGW/09-kernel{kstr}_{nval_co}_{ncon_co}/bsexmat",
    bsedmat_fname   =   f"../BGW/09-kernel{kstr}_{nval_co}_{ncon_co}/bsedmat",

    nbnd_val        =   nval,
    nbnd_cond       =   ncon,
    nbnd_val_co     =   nval_co,
    nbnd_cond_co    =   ncon_co,
    nbnd_val_fi     =   nval,
    nbnd_cond_fi    =   ncon,

    extra_lines     =   [
        "use_symmetries_coarse_grid",
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
    "time":     "48:00:00",
    "nodes":    1,
    "ntasks":   general_settings["nproc"],
    "partition": "compute"
})
js.run_TMPDIR   =   False
absorption_task.js  =   js

absorption_task.write()
if submit:
    absorption_task.submit()


