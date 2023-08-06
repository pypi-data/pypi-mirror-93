import osqp
import numpy as np
from scipy import sparse

class OsQpSolver:
    def __init__(self, show_progress_qp, tol_qp):
        self.options = {'verbose': show_progress_qp,
        'eps_rel': 1e-20, 'eps_abs': 1e-20,
        'eps_prim_inf': tol_qp, 'eps_dual_inf': tol_qp}

    def __call__(self, P, q, G, h):
        P = sparse.csc_matrix(P)
        A = sparse.csc_matrix(G)
        prob = osqp.OSQP()
        prob.setup(P, q, A, None, h, **self.options)
        res = prob.solve()
        return res.x
