import os
from .pwscfinput import PWscfInput


def get_scf_input(prefix, pseudo_key, structure, kpts, wtks):
    """Construct a Quantum Espresso scf input."""
    inp = PWscfInput(pseudo_key = pseudo_key)

    inp.control.update(
        prefix = prefix,
        pseudo_dir = os.environ["PSEUDODIR"],
        calculation = 'scf',
        )

    inp.electrons.update(
        electron_maxstep = 100,
        conv_thr = 1.0e-6,
        mixing_mode = 'plain',
        mixing_beta = 0.7,
        mixing_ndim = 8,
        diagonalization = 'david',
        diago_david_ndim = 4,
        diago_full_acc = True,
        )

    inp.set_kpoints_crystal(kpts, wtks)
    inp.structure = structure

    return inp


def get_bands_input(prefix, pseudo_key, structure, kpts, wtks, nbnd=None):
    """Construct a Quantum Espresso bands input."""
    inp = get_scf_input(prefix, pseudo_key, structure, kpts, wtks)
    inp.control['calculation'] = 'bands'
    if nbnd is not None:
        inp.system['nbnd'] = nbnd
    return inp



