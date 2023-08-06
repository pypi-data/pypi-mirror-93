import numpy as np
import cvxopt as cvx


class CvxQpSolver:
    def __init__(self, show_progress_qp, tol_qp):
        self.options = {'show_progress': show_progress_qp,
        'reltol': tol_qp, 'abstol': tol_qp, 'feastol': tol_qp}

    def __call__(self, P, q, G, h, *args, **kwargs):
        Pcvx = cvx.matrix(P)
        qcvx = cvx.matrix(q)
        Gcvx = cvx.matrix(G)
        hcvx = cvx.matrix(h)
        res = cvx.solvers.qp(Pcvx, qcvx, Gcvx, hcvx, options=self.options)
        return np.asarray(res['x']).flatten()
