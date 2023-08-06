# Copyright 2018-2019 CNRS, Ecole Polytechnique and Safran.
#
# This file is part of nullspace_optimizer.
#
# nullspace_optimizer is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# nullspace_optimizer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# A copy of the GNU General Public License is included below.
# For further information, see <http://www.gnu.org/licenses/>.

import numpy as np
import scipy.sparse.linalg as linalg
import time
from .optimizable import OptimizableBase, Optimizable, LightOptimizable

try:
    import colored as col

    def colored(text, color=None, attr=None):
        if color:
            text = col.stylize(text, col.fg(color))
        if attr:
            text = col.stylize(text, col.attr(attr))
        return text
except:
    def colored(text, color=None, attr=None):
        return text


def display(message, level=0, debug=0, color=None, attr=None, end='\n',
            flag=None):
    """ Display function with tunable level of verbosity

    INPUTS
    ------

    message        :   text to be printed
    level          :   level of importance of the message; will be actually
                       printed if debug >= level
    debug          :   current verbosity level
    color, attr    :   formattings with the `colored` package
    end            :   if set to '', will remove the final line carriage return
    flag           :   an extra indicator equal to None, 'stdout' or 'stderr',
                       the last two indicating that the text
                       passed to display comes from the standard output or
                       or error of a shell command.
                       Useful if display is overrided.
    """
    if color or attr:
        message = colored(message, color, attr)
    if debug >= level:
        print(message, end=end, flush=True)

def checkFullResults(results):
    """ Check the output dictionary in order to restart
        from the last iterate"""
    n = len(results['x'])
    group1 = ['J', 'G', 'H', 's', 'it']
    group2 = ['normxiJ', 'normxiJ_save', 'eps', 'muls', 'tolerance']
    for key in group1:
        if key not in results:
            raise Exception(
                f"Error, key {key} is missing in the results dictionary.")
        if len(results[key]) != n:
            raise Exception(f"Error, key {key} should have length n={n}.")
    for key in group2:
        if key not in results:
            raise Exception(
                f"Error, key {key} is missing in the results dictionary.")
        if len(results[key]) == n:
            results[key] = results[key][:-1]
        if len(results[key]) != n-1:
            raise Exception(
                f"Error, key {key} should have length n-1={n-1}.")
    x = results['x'][-1]
    it = results['it'][-1]
    s = results['s'][-1]
    normxiJ_save = np.asarray(results['normxiJ_save'][-1])
    muls = np.asarray(results['muls'][-1])
    for key in results.keys():
        if key not in ['normxiJ', 'normxiJ_save', 'eps', 'muls', 's', 'tolerance']:
            results[key] = results[key][:-1]
    return (x, it, s, normxiJ_save, muls)

class FullResults:
    _keys = ('it', 'x', 'J', 'G', 'H', 'muls', 'normxiJ', 'normxiJ_save', 'tolerance', 's', 'eps')

    def __init__(self, restart=None):
        self._results = restart

    def initialize(self):
        if self._results:
            # Allow to restart the optimization from the last result
            return checkFullResults(self._results)
        else:
            # Start from scratch
            self._results = {k: [] for k in self._keys}
            x = None
            it = 0
            s = 0 # Longueur du chemin d'optimization parcouru
            self._results['s'].append(s)
            normxiJ_save = None
            muls = None
            return (x, it, s, normxiJ_save, muls)

    def implementation(self):
        return self._results

    def save(self, key, value):
        self._results[key].append(value)

    def load(self, key):
        return self._results[key][-1]

class LightResults:
    _keys = ('it', 'x', 'J', 'G', 'H', 'muls', 'normxiJ', 'normxiJ_save', 'tolerance', 's', 'eps')

    def __init__(self, restart=None):
        self._results = restart

    def initialize(self):
        if self._results:
            # Restart from previous state
            x = self._results['x']
            it = self._results['it']
            s = self._results['s']
            normxiJ_save = np.asarray(self._results['normxiJ_save'])
            muls = np.asarray(self._results['muls'])
        else:
            # Start from scratch
            x = None
            it = 0
            s = 0
            normxiJ_save = None
            muls = None
            self._results = {k: None for k in self._keys}
            self._results['s'] = s
        return (x, it, s, normxiJ_save, muls)

    def implementation(self):
        return self._results

    def save(self, key, value):
        self._results[key] = value

    def load(self, key):
        return self._results[key]


def nlspace_solve(problem: Optimizable, params=None, results=None):
    """
    Solve the optimization problem
        min      J(x)
        x in V
        under the constraints
        g_i(x)=0  for all i=0..p-1
        h_i(x)<=0 for all i=0..q-1

    Usage
    -----
    results=nlspace_solve(problem: Optimizable, params: dict, results: dict)

    Inputs
    ------
    problem : an `~Optimizable` object corresponding to the optimization
              problem above.

    params  : (optional) a dictionary containing algorithm parameters
              (see below).

    results : (optional) a previous output of the `nlspace_solve` function.
              The optimization will keep going from the last input of
              the dictionary `results['x'][-1]`.
              Useful to restart an optimization after an interruption.

    Output
    ------
    results : dictionary containing
        results['x']       : optimization path
                             (x_0,x_1,...,x_n).
        results['J']       : values of the objective function along the path
                             (J(x_0),...,J(x_n))
        results['G']       : equality constraint values
                             (G(x_0),...,G(x_n))
        results['H']       : inequality constraints values
                             (H(x_0),...,H(x_n))
        results['muls']    : lagrange multiplier values
                             (mu(x_0),...,mu(x_n))
        results['normxiJ'] : norms of the nullspace step xiJ
        results['tolerance']:estimation of an uncertainty bound on the
                             constraints under which these can expect to be
                             satisfied. It is computed thanks to the formula:
                                tolerance = ||DC||_1 dt
        results['s']       : the optimization path length
                             (s(x_0),s(x_1),...,s(x_n))
                             with s(x(t))=\\int_0^t ||x'(\\tau)|| d\\tau


    Optional algorithm parameters
    -----------------------------

    params['alphaJ']   : (default 1) scaling coefficient for the null space
        step xiJ decreasing the objective function

    params['alphaC']   : (default 1) scaling coefficient for the Gauss Newton
        step xiC decreasing the violation of the constraints

    params['alphas']   : (optional) vector of dimension
        problem.nconstraints + problem.nineqconstraints containing
        proportionality coefficients scaling the Gauss Newton direction xiC for
        each of the constraints

    params['debug'] : Tune the verbosity of the output (default 0)
                      Set param['debug']=-1 to display only the final result
                      Set param['debug']=-2 to remove any output

    params['dt']       : (default : `problem.h_size`). Pseudo time-step
        expressed in a length unit. The descent step is normalized such that
            ||dxiJ||=alphaJ*dt ||dxiC||=alphaC*dt
        for the first params['itnormalisation'] iterations.  If `dt` is not
        set, then the update `dt`<-problem.h_size is made at every iteration
        (useful if problem.h_size depends on the current iterate x)

    params['itnormalisation']: (default 1) the iteration number after which the
        null space step xiJ is not normalized anymore

    params['K']: tunes the distance at which inactive inequality constraints
        are felt. Constraints are felt from a distance K*params['dt']

    params['maxit']    : Maximal number of iterations (default : 4000)

    params['maxtrials']: (default 3) number of trials in between time steps
        until the merit function decreases

    params['normalisation_norm'] : the euclidean norm used to normalize the
        descent direction.

    params['dual_norm'] : the dual norm of the norm provided by
        params['normalisation_norm'].

    params['normalize_tol'] : if >= 0 (default : 0),
        then xiJ is normalized every time the set of active constraints changes
        in addition to the first params['itnormalisation'] iterations.  The
        value of this parameter can be set to a strictly positive tolerance
        (e.g. 1e-7) to normalize only when a substantial discontinuity occurs
        in the multipliers. Useful if the optimizer is hesitating between
        active constraints. If set to a negative value, then no normalization
        is performed when the active set changes.

    params['provide_gradient']   : (default False).
        If set to True, then the algorithm will call problem.dJT, problem.dGT,
        problem.dHT to compute gradients

    params['tol']      : (default 1e-5) Algorithm stops when
            ||x_{n+1}-x_n||<params['tol'] * params['dt']
        or after params['maxit'] iterations.

    params['tol_merit'] : (default 0) a new iterate x_{n+1} is accepted if
        merit(x_{n+1})<(1+sign(merit(x_n)*params['tol_merit']))*merit(x_n)

    params['tol_qp'] : (default 1e-20) the tolerance for the qp solver

    params['show_progress_qp'] : (default False) If true, then the output of
        qp solver will be displayed between iterations.

    params['inner_prod_solver'] : 'umfpack' (default) or 'cg'. The solver used
        to invert the inner product when computing gradients.

    params['qp_solver'] : 'cvxopt' (default) or 'osqp'. The qp solver used to
        solve the dual problem.
    """
    abstract_results = FullResults(results)
    return nlspace_solve_impl(problem, params, abstract_results)

def nlspace_solve_light(problem: LightOptimizable, params=None, results=None, display=display):
    """
    Solve the optimization problem
        min      J(x)
        x in V
        under the constraints
        g_i(x)=0  for all i=0..p-1
        h_i(x)<=0 for all i=0..q-1

    Usage
    -----
    results=nlspace_solve_light(problem: LightOptimizable, params: dict, results: dict)

    In contrast with `nslpace_solve`, the output `results` contains only the last output of
    the optimization. It does not store the optimization path.

    Inputs
    ------
    problem : a `~LightOptimizable` object corresponding to the optimization
              problem above.

    params  : (optional) a dictionary containing algorithm parameters
              (see below).

    results : (optional) a previous output of the `nlspace_solve_light` function.
              The optimization will keep going from the design stored
              in the dictionary `results['x']`.
              Useful to restart an optimization after an interruption.

    Output
    ------
    results : dictionary containing
        results['x']            : current value of the design variable
                                  x_n
        results['J']            : current value of the objective function
                                  J(x_n)
        results['G']            : current values of the equality constraints
                                  G(x_n)
        results['H']            : current values of the inequality constraints
                                  H(x_n)
        results['muls']         : current Lagrange multiplier values
                                  \\mu(x_n)
        results['normxiJ']      : current norms of the nullspace step \\xi_J
        results['normxiJ_save'] : current normalisation of \\xi_J
        results['tolerance']    : estimation of an uncertainty bound on the
                                  constraints under which these can expect to be
                                  satisfied. It is computed thanks to the formula:
                                     tolerance = ||DC||_1 dt
        results['s']            : length of optimization path
                                  s(x_n)
                                  with s(x(t))=\\int_0^t ||x'(\\tau)|| d\\tau
    Parameters
    ----------

    These are the same than those of `nlspace_solve`.
    """
    abstract_results = LightResults(results)
    return nlspace_solve_impl(problem, params, abstract_results, display)

def nlspace_solve_impl(problem: OptimizableBase, params=None, abstract_results=None, display=display):
    if params is None:
        params = dict()
    alphaJ = params.get('alphaJ', 1)
    alphaC = params.get('alphaC', 1)
    maxit = params.get('maxit', 4000)
    maxtrials = params.get('maxtrials', 3)
    debug = params.get('debug', 0)
    normalisation_norm = params.get('normalisation_norm', np.inf)
    dual_norm = params.get('dual_norm', 1)
    itnormalisation = params.get('itnormalisation', 1)
    tol_merit = params.get('tol_merit', 0)
    inner_prod_solver = params.get('inner_prod_solver', 'umfpack')
    dt = params.get('dt', problem.h_size)
    K = params.get('K', 0.1)
    provide_gradient = params.get('provide_gradient', False)
    tol_qp = params.get('tol_qp', 1e-20)
    show_progress_qp = params.get('show_progress_qp', False)
    normalize_tol = params.get(
        'normalize_tol', 0)
    tol = params.get('tol', 1e-5*dt)
    alphas = np.asarray(params.get(
        'alphas', [1]*(problem.nconstraints+problem.nineqconstraints)))
    qp_solver = params.get('qp_solver', 'cvxopt')

    p = problem.nconstraints

    if qp_solver == 'osqp':
        from .osqp_interface import OsQpSolver
        qpSolver = OsQpSolver(show_progress_qp, tol_qp)
    else:
        from .cvx_interface import CvxQpSolver
        qpSolver = CvxQpSolver(show_progress_qp, tol_qp)

    def compute_norm(x):
        if normalisation_norm == np.inf:
            return np.linalg.norm(x, np.inf)
        elif normalisation_norm == 2:
            return np.sqrt(np.mean(x**2))
        else:
            return normalisation_norm(x)

    def getTilde(C, eps=0):
        tildeEps = C[p:] >= -eps
        tildeEps = np.asarray(np.concatenate(([True]*p, tildeEps)), dtype=bool)
        return tildeEps

    def getEps(C, dC):
        if dC.shape[0] == 0:
            return (0, [])
        if normalisation_norm == np.inf:
            norm1 = (np.sum(abs(dC[p:, :]), 1))
        elif normalisation_norm == 2:
            norm1 = (np.linalg.norm(abs(dC[p:, :])))
        else:
            norm1 = np.apply_along_axis(dual_norm, 1, abs(dC[p:,:]))
        eps = norm1*dt*K
        tildeEps = getTilde(C, eps)
        return (eps, tildeEps)

    def eliminate(A):
        if not 0 in A.shape:
            _, R = np.linalg.qr(A.T)
            indices = np.diag(R)!=0
        else:
            indices = []
        return indices

    x, it, s, normxiJ_save, muls = abstract_results.initialize()

    if x is None:
        x = problem.x0()

    (J, G, H) = problem.eval(x)

    normdx = 1  # current value for x_{n+1}-x_n
    if muls is None:
        muls = np.zeros(len(G) + len(H))

    # If is not a manifold, compute and factorize the inner product matrix
    # only once
    if not problem.is_manifold:
        A = problem.inner_product(x)
        if inner_prod_solver == 'umfpack':
            solve = linalg.factorized(A)

    while normdx > tol and it <= maxit:
        abstract_results.save('it', it)
        abstract_results.save('J', J)
        abstract_results.save('G', G)
        abstract_results.save('H', H)
        abstract_results.save('x', x)
        problem.accept(abstract_results.implementation())
        x = abstract_results.load('x')

        display('\n', 1, debug)
        display(f'{it}. J='+format(J, '.4g')+' ' +
                'G=['+",".join([format(x, '.4g') for x in G[:10]])+'] ' +
                'H=['+",".join([format(x, '.4g') for x in H[:10]])+']', 0, debug)

        display(f'x={x}', 5, debug)

        (dJ, dG, dH) = problem.eval_sensitivities(x)

        H = np.asarray(H)
        G = np.asarray(G)
        C = np.concatenate((G, H))

        dJ = np.asarray(dJ)
        dG = np.asarray(dG)
        dH = np.asarray(dH)
        dC = np.concatenate((dG, dH), axis=0)

        dt = params.get('dt', problem.h_size)

        (eps, tildeEps) = getEps(C, dC)
        abstract_results.save('eps', eps)
        tilde = getTilde(C)

        dCT = np.zeros(dC.shape).T
        if provide_gradient:
            # User provides dJT, dGT, dHT
            (dJT, dGT, dHT) = problem.eval_gradients(x)
            dCT = np.concatenate((dGT, dHT), axis=1)
        else:
            if problem.is_manifold:
                # A must be recomputed
                A = problem.inner_product(x)
                if hasattr(A, 'tocsc'):
                    A = A.tocsc()
                if inner_prod_solver == 'umfpack':
                    solve = linalg.factorized(A)
                if inner_prod_solver == 'cg':
                    def solve(x): return linalg.cg(A, x, tol=1e-7)[0]
            display(f"Factorize matrix and compute gradients with"
                    + f"{inner_prod_solver}...", 7, debug, color="magenta")
            cpu = time.process_time()
            dJT = solve(dJ)
            for i in (x for x in range(dC.shape[0]) if tildeEps[x]):
                dCT[:, i] = solve(dC[i, :])
            cpu = time.process_time() - cpu
            display(
                f"Done -- total time={format(cpu,'.02f')}", 7, debug,
                color="magenta")
        # Solve the dual problem to obtain the new set of active constraints
        ind = eliminate(dC[tildeEps, :]) # Independent constraints
        tildeQp = np.full(len(tildeEps),False)
        tildeQp[tildeEps] = ind
        qtildeQpEps = sum(np.where(tildeQp)[0]>=p)
        pQpEps = sum(np.where(tildeQp)[0]<p)
        Ps = dC[tildeQp, :].dot(dCT[:, tildeQp])
        qs = dJ.dot(dCT[:, tildeQp])
        Gs = np.concatenate((np.zeros((qtildeQpEps, pQpEps)), -np.eye(qtildeQpEps)), axis=1)
        hs = np.zeros((qtildeQpEps, 1))
        prevmuls = muls.copy()
        muls.fill(0.0)
        if problem.nconstraints+problem.nineqconstraints==0:
            hat = []
        else:
            hat = np.asarray([True]*problem.nconstraints+[False]*problem.nineqconstraints)
        if pQpEps + qtildeQpEps > 0:
            muls[tildeQp] = qpSolver(Ps, qs, Gs, hs)
            oldmuls = muls.copy()
            hat[p:] = muls[p:] > 30*tol_qp

            #Ignore duplicate constraints during the projection
            hat[np.logical_not(tildeQp)] = False

            # Compute null space direction xiJ
            try:
                dCdCTinv = np.linalg.inv(dC[hat, :].dot(dCT[:, hat]))
            except Exception:
                display(
                    "Warning, constraints are not qualified, using "
                    "pseudo-inverse.", -1, debug, color="red")
                dCdCTinv = np.linalg.pinv(dC[hat, :].dot(dCT[:, hat]))
            muls = np.zeros(len(C))
            muls[hat] = -dCdCTinv.dot(dC[hat, :].dot(dJT))

            if not np.all(muls[p:] >= 0):
                display("Warning, the active set has not been predicted "
                        + "correctly Using old lagrange multipliers", 1,
                        debug, color="orange_4a")
                muls = oldmuls.copy()

        abstract_results.save('muls', muls)
        display(f"Lagrange multipliers: {muls[:10]}", 5, debug)
        xiJ = dJT + dCT.dot(muls)

        # Compute range step direction xiC
        indicesEps = np.logical_or(tilde, hat)
        try:
            dCtdCtTinv = np.linalg.inv(
                dC[indicesEps, :].dot(dCT[:, indicesEps]))
        except Exception:
            display("Warning, constraints are not qualified. "
                    + "Using pseudo-inverse.", 1, debug, color="orange_4a")
            dCtdCtTinv = np.linalg.pinv(
                dC[indicesEps, :].dot(dCT[:, indicesEps]))
        xiC = dCT[:, indicesEps].dot(
            dCtdCtTinv.dot(C[indicesEps]*alphas[indicesEps]))

        normxiJ = compute_norm(xiJ)
        abstract_results.save('normxiJ', normxiJ)
        if it < itnormalisation or \
           (normalize_tol >= 0 and
            not np.all((muls[p:] > normalize_tol)
                       == (prevmuls[p:] > normalize_tol))):
            normxiJ_save = normxiJ
            abstract_results.save('normxiJ_save', normxiJ_save)
            AJ = (alphaJ * dt) / (1e-9 + normxiJ)
            display(f"Normalisation of the xiJ direction, itnormalisation={max(itnormalisation, it + 1)}",
                level=5, debug=debug)
        else:
            abstract_results.save('normxiJ_save', normxiJ_save)
            AJ = alphaJ*dt / max(1e-9 + normxiJ, normxiJ_save)
        AC = min(0.9, alphaC*dt / max(compute_norm(xiC), 1e-9))

        # Make updates with merit function
        dx = -AJ*xiJ-AC*xiC
        normdx = np.linalg.norm(dx, 2)
        success = 0
        abstract_results.save('tolerance', np.sum(abs(dC), 1)*dt)

        merit = AJ*(J+muls.dot(C))+0.5*AC * \
            C[indicesEps].dot(dCtdCtTinv.dot(C[indicesEps]))
        for k in range(maxtrials):
            newx = problem.retract(x, (0.5**k)*dx)
            (newJ, newG, newH) = problem.eval(newx)
            newC = np.concatenate((newG, newH))
            newmerit = AJ*(newJ+muls.dot(newC))+0.5*AC * \
                newC[indicesEps].dot(dCtdCtTinv.dot(newC[indicesEps]))
            if newmerit < (1+np.sign(merit)*tol_merit)*merit:
                success = 1
                break
            else:
                display("Warning, merit function did not decrease " +
                        f"(merit={merit}, newmerit={newmerit})"
                        + f"-> Trial {k+1}", 0, debug, color="red")
        if not success:
            display(
                "All trials have failed, passing to the next iteration.", 0, debug,
                color="red")
        x = newx
        it += 1
        s += (0.5**k)*np.linalg.norm(dx, np.inf)
        (J, G, H) = (newJ, newG, newH)

        abstract_results.save('s', s)

    abstract_results.save('J', J)
    abstract_results.save('G', G)
    abstract_results.save('H', H)
    abstract_results.save('x', x)
    abstract_results.save('it', it)
    problem.accept(abstract_results.implementation())

    display('\n', -1, debug)
    display('Optimization completed.', -1, debug)
    display(f'{it}. J='+format(J, '.4g')+' ' +
            'G=['+",".join([format(x, '.4g') for x in G[:10]])+'] ' +
            'H=['+",".join([format(x, '.4g') for x in H[:10]])+']', -1, debug,
            color="blue")
    return abstract_results.implementation()
