import os
import sys
import json

from pymatgen.core import Structure
from BGWpy import SigmaTask

from util.job_script import JS

#########################
ngkpt   =   []
kstr    =   ""
kstr_job    =   ""
for k in sys.argv[1:4]:
    ngkpt.append(int(k))
    kstr        +=  "_"+k
    kstr_job    +=  k
ibnd_min    =   121
ibnd_max    =   144
nodes       =   16
submit      =   False
if len(sys.argv) >= 5:
    submit  =   bool(int(sys.argv[4]))
rerun       =   False
if len(sys.argv) == 6:
    rerun   =   bool(int(sys.argv[5]))
#########################
extra_lines     =   [
    "screening_semiconductor",
    "dont_use_vxcdat"
]
if rerun:
    extra_lines.append("eqp_outer_corrections")

structure   =   Structure.from_file("../ibrav.cif")

with open("../general.json") as fil:
    general_settings    =   json.load(fil)
general_settings["nproc"]   =   128*nodes
suffix  =   "real"
if general_settings["flavor_complex"]:  suffix  =   "cplx"

sigma_task      =   SigmaTask(
    dirname     =   f"../BGW/08-sigma{kstr}",
    structure   =   structure,
    ngkpt       =   ngkpt,

    wfn_co_fname    =   f"../QE/02-wfn{kstr}/wfn.{suffix}",
    rho_fname       =   f"../QE/02-wfn{kstr}/rho.real",
    vxc_fname       =   f"../QE/02-wfn{kstr}/vxc.real",

    eps0mat_fname   =   f"../BGW/07-epsilon{kstr}/eps0mat",
    epsmat_fname    =   f"../BGW/07-epsilon{kstr}/epsmat",

    ibnd_min        =   ibnd_min,
    ibnd_max        =   ibnd_max,
    extra_lines     =   extra_lines,

    **general_settings,
)

if rerun:
    dirname =   sigma_task.dirname
    if not os.path.exists(dirname+"/bk"):
        os.mkdir(dirname+"/bk")
    if os.path.isfile(dirname+"/bk/sigma.out"):
        print("Output files already exists in bk folder. Move this first.")
        sys.exit()
    os.system(f"mv {dirname}/*dat {dirname}/sigma* {dirname}/bk")
    BGWDIR  =   os.environ["BGWDIR"]
    os.system(f"python {BGWDIR}/../Sigma/eqp.py eqp0 {dirname}/bk/sigma_hp.log {dirname}/eqp_outer.dat")
    sigma_task.update_link(sigma_task.wfn_co_fname, "WFN_outer")

js  =   JS(header = {
    "job-name": f"08-sigma{kstr_job}",
    "time":     "48:00:00",
    "nodes":    nodes,
    "ntasks":   general_settings["nproc"],
    "partition":    "compute"
})
sigma_task.js =   js

sigma_task.write()
if submit:
    sigma_task.submit()

