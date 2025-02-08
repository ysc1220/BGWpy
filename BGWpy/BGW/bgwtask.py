from __future__ import print_function
from ..config import flavors, default_runscript
from ..core import MPITask, IOTask

# Public
__all__ = ['BGWTask']

class BGWTask(MPITask, IOTask):
    """Base class for BerkeleyGW calculations."""
    _TAG_JOB_COMPLETED = 'TOTAL'
    _use_hdf5 = flavors['use_hdf5']
    _flavor_complex = flavors['flavor_complex']
    def __init__(self, dirname, **kwargs):
        super(BGWTask, self).__init__(dirname, **kwargs)
        self.runscript.append(default_runscript['header_BGW'])

