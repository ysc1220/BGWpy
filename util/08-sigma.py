import os
import sys
import json

from pymatgen.core import Structure
from BGWpy import SigmaTask

ngkpt   =   []
kstring =   ""
for k in sys.argv[1:4]:
    ngkpt.append(int(k))
    kstring +=  "_"+k

ngkpt_co    =   []
kstring_co  =   ""
for k in sys.argv[4:7]:
    ngkpt_co.append(int(k))
    kstring_co  +=  "_"+k

structure   =   Structure.from_file("../AgSePh_prim.cif")

with open("../general.json") as fil:
    general_settings    =   json.load(fil)

extra_lines =   [
    "screening_semiconductor",
    "dont_use_vxcdat",
    "dont_use_hdf5",
]

sigma_input_files   =   {
    "ngkpt":            ngkpt_co,
    "wfn_co_fname":     f"../QE/02-wfn{kstring_co}/wfn.real",
    "rho_fname":        f"../QE/02-wfn{kstring_co}/rho.real",
    "vxc_fname":        f"../QE/02-wfn{kstring_co}/vxc.real",

    "eps0mat_fname":    f"../BGW/07-epsilon{kstring}/eps0mat",
    "epsmat_fname":     f"../BGW/07-epsilon{kstring}/epsmat",

    "ibnd_min": 119,
    "ibnd_max": 142,

    "extra_lines":  extra_lines
}

sigma_task  =   SigmaTask(
    dirname =   f"../BGW/08-sigma{kstring}{kstring_co}",
    structure   =   structure,
    **sigma_input_files,
    **general_settings
)

kstring =   kstring.replace("_", "")
kstring_co  =   kstring_co.replace("_", "")

from util.job_script import JS
js  =   JS(header = {
    "job-name": f"08-sigma{kstring}{kstring_co}",
    "time":     "168:00:00",
    "ntasks":   40
})
js.run_TMPDIR   =   False
js.before_job   =   "ulimit -s unlimited\n"
sigma_task.js   =   js

sigma_task.write()
sigma_task.submit()

