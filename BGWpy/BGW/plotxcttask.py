from .bgwtask import BGWTask
from ..core import BasicInputFile

__all__ = ["PlotxctTask"]

def list2str(l):
    val =   ""
    for elem in l:  val +=  " "+str(elem)
    return val

def list2_str(l):
    val =   ""
    for elem in l:  val +=  "_"+str(elem)
    return val

class PlotxctTask(BGWTask):
    """Exciton wavefunction plot"""

    _TASK_NAME  =   "Plotxct"
    _input_fname    =   "plotxct.inp"
    _output_fname   =   "plotxct.out"

    def __init__(self, dirname = None, **kwargs):
        kstr    =   list2_str(kwargs["ngkpt"])
        kstr_fi =   list2_str(kwargs["ngkpt_fi"])
        nstr    =   list2_str([kwargs["nval"], kwargs["ncon"]])
        plot_spin   =   kwargs.get("plot_spin", 1)
        plot_state  =   kwargs["plot_state"]
        if dirname is None:
            dirname =   f"../BGW/10-absorption{kstr}{kstr_fi}{nstr}/x{plot_state:03d}"

        super(PlotxctTask, self).__init__(dirname, **kwargs)
        if "flavor_complex" in kwargs:
            self._flavor_complex    =   bool(kwargs["flavor_complex"])
        suff    =   "cplx" if self._flavor_complex else "real"

        extra_lines =   kwargs.get("extra_lines", [])
        extra_variables =   kwargs.get("extra_variables", {})

        extra_variables["plot_spin"]    =   plot_spin
        extra_variables["plot_state"]   =   plot_state
        scfinp_fname    =   kwargs.get("scfinp_fname", "../../../QE/01-scf/scf.pwi")

        supercell_size  =   kwargs["supercell_size"]
        if not "hole_position" in kwargs:
            hole_position   =   [round(x/2, 1) for x in supercell_size]
        else:
            hole_position   =   kwargs["hole_position"]

        extra_variables.update({
            "plot_state":       plot_state,
            "supercell_size":   list2str(supercell_size),
            "hole_position":    list2str(hole_position)
        })

        self.input  =   BasicInputFile(
            extra_variables,
            extra_lines
        )
        self.input.fname    =   self._input_fname

        # Prepare links
        self.wfn_fi_fname   =   kwargs.get("wfn_fi_fname",
                                f"../QE/04-wfn{kstr_fi}/wfn.{suff}")
        self.wfnq_fi_fname  =   kwargs.get("wfnq_fi_fname",
                                f"../QE/03-wfnq{kstr_fi}/wfn.{suff}")
        self.eigvec_fname   =   kwargs.get("eigvec_fname",
                                f"../BGW/10-absorption{kstr}{kstr_fi}{nstr}/eigenvectors")

        # Set up the run script
        self.runscript["PLOTXCT"]   =   f"plotxct.{suff}.x"
        self.runscript.append("$MPIRUN $PLOTXCT &> {}".format(self._output_fname))

        self.runscript.append(f"python $BGWDIR/../Visual/volume.py {scfinp_fname} espresso xct.{plot_state:06d}_s{plot_spin}.a3Dr a3dr x{plot_state:03d}.cube cube false re true")

    @property
    def wfn_fi_fname(self):
        return self._wfn_fi_fname

    @wfn_fi_fname.setter
    def wfn_fi_fname(self, value):
        self._wfn_fi_fname  =   value
        self.update_link(value, "WFN_fi")

    @property
    def wfnq_fi_fname(self):
        return self._wfnq_fi_fname

    @wfnq_fi_fname.setter
    def wfnq_fi_fname(self, value):
        self._wfnq_fi_fname =   value
        self.update_link(value, "WFNq_fi")

    @property
    def eigvec_fname(self):
        return self._eigvec_fname

    @eigvec_fname.setter
    def eigvec_fname(self, value):
        self._eigvec_fname  =   value
        self.update_link(value, "eigenvectors")

    def write(self):
        super(PlotxctTask, self).write()
        with self.exec_from_dirname():
            self.input.write()


