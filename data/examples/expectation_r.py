#!/usr/bin/env python

import numpy as np
from horton import context, BeckeMolGrid, log
from iodata import load_one
from gbasis.evals.eval import evaluate_basis
from gbasis.wrappers import from_iodata


# Load the Gaussian output from file from HORTON's test data directory.
fn_fchk = context.get_fn("test/water_sto3g_hf_g03.fchk")
# Replace the previous line with any other fchk file, e.g. fn_fchk = 'yourfile.fchk'.
mol = load_one(fn_fchk)

# Specify the integration grid
grid = BeckeMolGrid(mol.atcoords, mol.atnums, mol.atnums, mode="keep")

# # Get the spin-summed density matrix
one_rdm = mol.one_rdms.get("post_scf", mol.one_rdms.get("scf"))
basis, coord_types = from_iodata(mol)
basis_grid = evaluate_basis(basis, grid.points, coord_type=coord_types)
rho = np.einsum("ab,bp,ap->p", one_rdm, basis_grid, basis_grid, optimize=True)
#!/usr/bin/env python

# Compute the expectation value of |r|.
r = (grid.points[:, 0] ** 2 + grid.points[:, 1] ** 2 + grid.points[:, 2] ** 2) ** 0.5
expt_r = grid.integrate(rho, r)
if log.do_medium:
    log("EXPECTATION VALUE OF |R|: {0}".format(expt_r))


# CODE BELOW IS FOR horton-regression-test.py ONLY. IT IS NOT PART OF THE EXAMPLE.
rt_results = {"expt_r": expt_r}
# BEGIN AUTOGENERATED CODE. DO NOT CHANGE MANUALLY.
rt_previous = {
    "expt_r": 11.05810248532503,
}
