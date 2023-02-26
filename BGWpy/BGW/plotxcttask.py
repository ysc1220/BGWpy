from .bgwtask import BGWTask

__all__ = ["PlotxctTask"]

class PlotxctTask(BGWTask):
    """Exciton wavefunction plot"""

    _TASK_NAME  =   "Plotxct"
    _input_fname    =   "plotxct.inp"
    _output_fname   =   "plotxct.out"

    def __init__(self, dirname, **kwargs):

        super(PlotxctTask, self).__init__(dirname, **kwargs)
        if "flavor_complex" in kwargs:
            self._flavor_complex    =   bool(kwargs["flavor_complex"])

        extra_lines =   kwargs.get("extra_lines", [])
        extra_variables =   kwargs.get("extra_variables", {})


