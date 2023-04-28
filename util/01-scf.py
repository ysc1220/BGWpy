import os
import sys
import json

from BGWpy import QeScfTask

from util.job_script import JS

with open("../general.json") as fil:
    general_settings    =   json.load(fil)
with open("../qe.json") as fil:
    scf_settings    =   json.load(fil)

scf_task    =   QeScfTask(
    dirname =   "../QE/01-scf",
    **general_settings,
    ngkpt   =   [14, 14, 2]
)
scf_task.input.update_params(scf_settings)

js  =   JS(header = {
    "job-name": "01-scf",
    "time": "48:00:00",
    "ntasks": 128,
    "partition": "compute"
})
js.run_TMPDIR   =   False
scf_task.js =   js

scf_task.write()
scf_task.submit()

