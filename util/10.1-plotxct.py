import sys

from BGWpy import PlotxctTask
from util.job_script import JS

ngkpt       =   sys.argv[1:4]
ngkpt_fi    =   sys.argv[4:7]
nval, ncon  =   sys.argv[7:9]
plot_state  =   int(sys.argv[9])

plotxcttask =   PlotxctTask(
    ngkpt   =   ngkpt,
    ngkpt_fi    =   ngkpt_fi,
    nval    =   nval,
    ncon    =   ncon,
    plot_state  =   plot_state,
    supercell_size  =   [15, 3, 3],
    flavor_complex  =   False
)

js  =   JS(header = {
    "job-name": f"x{plot_state:03d}",
})
plotxcttask.js  =   js

plotxcttask.write()
plotxcttask.submit()

