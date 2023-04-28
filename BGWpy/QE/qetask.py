from __future__ import print_function

import os

from ..config import flavors
from ..core.util import exec_from_dir
from ..core import MPITask, IOTask
from ..DFT import DFTTask

# Public
__all__ = ['QeTask']


class QeTask(DFTTask, IOTask):
    """Base class for Quantum Espresso calculations."""

    _TAG_JOB_COMPLETED = 'JOB DONE'
    _use_hdf5_qe = flavors['use_hdf5_qe']

    def __init__(self, dirname, **kwargs):
        """
        Arguments
        ---------

        dirname : str
            Directory in which the files are written and the code is executed.
            Will be created if needed.

        Keyword arguments
        -----------------

        See also:
            BGWpy.DFT.DFTTask

        """

        super(QeTask, self).__init__(dirname, **kwargs)

        self.prefix = kwargs.get('prefix', "qe")
        #self.pseudo_key =   kwargs.get("pseudo_key", ".")
        self.savedir = kwargs.get("savedir", self.prefix + '.save')

        self.runscript.header.append("module purge")
        self.runscript.header.append("module load slurm cpu gcc/9.2.0 openmpi quantum-espresso/6.7.0-openblas")
        self.mpirun =   'mpirun --map-by core --mca btl_openib_if_include "mlx5-2:1" --mca btl openib,self,vader'
        self.nproc_flag =   ""
        self.nproc      =   ""

        self.runscript['PW'] = kwargs.get('PW', 'pw.x')
        self.runscript['PWFLAGS'] = kwargs.get('PWFLAGS', '')

    def exec_from_savedir(self):
        original = os.path.realpath(os.curdir)
        if os.path.realpath(original) == os.path.realpath(self.dirname):
            return exec_from_dir(self.savedir)
        return exec_from_dir(os.path.join(self.dirname, self.savedir))

    def write(self):
        #self.check_pseudos()
        self.input.find_pseudo()
        super(QeTask, self).write()
        with self.exec_from_dirname():
            print("Writing %s/%s"%(os.getcwd(), self._input_fname))
            self.input.calc.write_input(self.input.atoms)
            if not os.path.exists(self.savedir):
                os.mkdir(self.savedir)

    # Yikes! I have to recopy the property. python3 would be so much better...
    @property
    def pseudo_dir(self):
        return self._pseudo_dir

    @pseudo_dir.setter
    def pseudo_dir(self, value):
        if os.path.realpath(value) == value.rstrip(os.path.sep):
            self._pseudo_dir = value
        else:
            self._pseudo_dir = os.path.relpath(value, self.dirname)
        if 'input' in dir(self):
            if 'control' in dir(self.input):
                self.input.control['pseudo_dir'] = self._pseudo_dir

