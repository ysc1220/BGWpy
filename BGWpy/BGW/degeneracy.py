
import os
import subprocess
import numpy as np
from ..core import fortran_str
from ..core import Task

__all__ =  ['DegeneracyTask']


class DegeneracyTask(Task):

    def __init__(self,
                 wfn_fname="WFN",
                 executable='degeneracy_check.x',
                 dirname='',
                 **kwargs):

        self.wfn_fname  =   os.path.join(dirname, wfn_fname)
        self.executable = executable
        self.dirname = dirname

    def get_number_bands(self):
        try:
            print("Running degeneracy_check.x ...")
            result  =   subprocess.run([self.executable, self.wfn_fname],
                           capture_output = True)
        except OSError as E:
            message = (str(E) + '\n\n' +
            79 * '=' + '\n\n' +
            'Could not find the executable degeneracy_check.x\n' +
            'Please make sure it is available for execution.\n' +
            'On a computing cluster, you might do this my loading the module:\n' +
            '    module load berkeleygw\n' +
            "If you compiled BerkeleyGW yourself, " +
            "make sure that the 'bin' directory\n" +
            'of BerkeleyGW is listed in your PATH environment variable.\n' +
            '\n' + 79 * '=' + '\n')

            raise OSError(message)

        number_bands    =   0
        for line in str(result.stdout).split("\\n"):
            line    =   line.split()
            if len(line) == 1 and line[0].isnumeric():
                number_bands    =   int(line[0])

        if number_bands == 0:
            raise OSError("Something wrong with degeneracy_check.x")

        print("number_bands:", number_bands)
        return number_bands

