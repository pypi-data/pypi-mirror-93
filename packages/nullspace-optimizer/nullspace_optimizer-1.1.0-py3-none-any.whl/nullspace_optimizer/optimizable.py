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
import scipy.sparse as sp


class OptimizableBase:
    """
    An abstract class whose instance can be passed as an input to
    nlspace_solve. An OptimizableBase object describes a
    constrained minimization problem of the form

        min      J(x)
       x in X

       under the constraints
        g_i(x)=0  for all i=0..p-1
        h_i(x)<=0 for all i=0..q-1

    Attributes
    ----------
    nconstraints     : number of equality constraints g_i
    nineqconstraints : number of inequality constraints h_i
    h_size           : characteristic length scale used by the optimizer
                       to normalize descent directions and compute accuracy
                       bounds.
    is_manifold      : indicate whether the optimization domain X is a manifold
                       (in that case the inner product matrix shall be
                       recomputed and refactorized at every evaluation of a new
                       iterate x) or a Euclidean space.
    """

    def __init__(self):
        self._nconstraints = 0
        self._nineqconstraints = 0
        self._is_manifold = True
        self._h_size = 1.0e-2

    @property
    def nconstraints(self):
        return self._nconstraints

    @property
    def nineqconstraints(self):
        return self._nineqconstraints

    @property
    def is_manifold(self):
        return self._is_manifold

    @property
    def h_size(self):
        return self._h_size

    def x0(self):
        """Returns the initialization."""
        return None

    def J(self, x):
        """Compute the value of the objective function at the point x."""
        return None

    def G(self, x):
        """Returns a list [g1,g2,...,gp] of the equality constraint
        values at x"""
        return []

    def H(self, x):
        """Returns a list [h1,h2,...,hp] of the inequality constraint
        values at x"""
        return []

    def dJ(self, x):
        """Returns the value of the Fréchet derivative of J at x.
        This must be a list or numpy array."""
        return None

    def dG(self, x):
        """Returns a list of the Fréchet derivatives of each of
        the equality constraints at x:
                [ [dg1dx1, dg1dx2,...,dg1dxk],
                  [dg2dx1,dg2dx2,...,dg2dxk],
                    ...
                  [dgpdx1, dgpdx2,...,dgpdxk] ]
        """
        return []

    def dH(self, x):
        """Returns a list of the Fréchet derivatives of each of
        the equality constraints at x:
                [ [dh1dx1, dh1dx2,...,dh1dxk],
                  [dh2dx1,dh2dx2,...,dh2dxk],
                    ...
                  [dhqdx1, dhqdx2,...,dhqdxk] ]
        """
        return []

    def dJT(self, x):
        """Returns the gradient of J at x.
        This must be implemented if no inner product is given.
        dJT(x) should return the solution of

                A * dJT(x) = dJ(x)

        where A is the chosen inner product.
        In particular, dJ(dJT(x)) should always be positive.
        """
        return None

    def dGT(self, x):
        """Returns the transpose of dG with respect to some inner product.
        This must be implemented if no inner product is given.
        dGT(x) should return a column matrix [ dG1T dG2T ... dGpT ]
        where each vector dGiT is the solution to

            A * dGiT(x) = dGi(x)

        where A is the chosen inner product.
        """
        return []

    def dHT(self, x):
        """Returns the transpose of dH with respect to some inner product.
        This must be implemented if no inner product is given.
        dHT(x) should return a column matrix [ dH1T dH2T ... dHpT ]
        where each vector dHiT is the solution to

            A * dHiT(x) = dHi(x)

        where A is the chosen inner product.
        """
        return []

    def eval(self, x):
        """Returns the triplet (J(x),G(x),H(x))"""
        return (self.J(x), self.G(x), self.H(x))

    def eval_sensitivities(self, x):
        """Returns the triplet (dJ(x),dG(x),dH(x))"""
        dJ = self.dJ(x)
        if self.nconstraints == 0:
            dG = np.empty((0, len(dJ)))
        else:
            dG = self.dG(x)
        if self.nineqconstraints == 0:
            dH = np.empty((0, len(dJ)))
        else:
            dH = self.dH(x)
        return (dJ, dG, dH)

    def eval_gradients(self, x):
        """Returns the triplet (dJT(x),dGT(x),dHT(x))
        Is used by nslpace_solve method only if self.inner_product returns
        None"""
        dJT = self.dJT(x)
        if self.nconstraints == 0:
            dGT = np.empty((0, len(dJT))).T
        else:
            dGT = self.dGT(x)
        if self.nineqconstraints == 0:
            dHT = np.empty((0, len(dJT))).T
        else:
            dHT = self.dHT(x)
        return (dJT, dGT, dHT)

    def inner_product(self, x):
        """Returns the inner product matrix at `x`.
        Output:
            A  :  a n-by-n matrix where n=len(dJ(x))
        """
        return None

    def retract(self, x, dx):
        """
        The retraction that explicit how to move from `x` by a step `dx`
        to obtain the new optimization point.

        Inputs:
            x  : current point
            dx : step (a vector of length len(dJ(x)))

        Output: the new optimized point after a step dx.
            newx = retract(x, dx)
        """
        return None


class Optimizable(OptimizableBase):
    @OptimizableBase.nconstraints.setter
    def nconstraints(self, nc):
        self._nconstraints = nc

    @OptimizableBase.nineqconstraints.setter
    def nineqconstraints(self, nic):
        self._nineqconstraints = nic

    @OptimizableBase.is_manifold.setter
    def is_manifold(self, im):
        self._is_manifold = im

    @OptimizableBase.h_size.setter
    def h_size(self, hs):
        self._h_size = hs

    def accept(self, results):
        """
        This function is called by nlspace_solve:
            - at the initialization
            - every time a new guess x is accepted on the optimization
              trajectory
        This allows to perform some post processing operations along the
        optimization trajectory. The function does not return any output but
        may update the dictionary `results` which may affect the optimization.
        Notably, the current point is stored in
            results['x'][-1]
        and an update of its value will be taken into account by nlspace_solve.

        Inputs:
            `results` : the current dictionary of results (see the function
                nlspace_solve)
        """
        pass


class EuclideanOptimizable(Optimizable):
    """An optimizable class for optimization in Euclidean space
    of dimension `n`.

    Usage
    -----
    >>> optim = EuclideanOptimizable(n);

    where n is the dimension of the space.
    The inner product matrix is automatically set to the identity of size `n`
    The retraction is the usual translation:
         x_{n+1} = x_n + dx

    Attribute:
        `n`  : The dimension of the Euclidean space.
    """

    def __init__(self, n):
        super().__init__()
        self.n = n
        self.is_manifold = False

    def inner_product(self, x):
        return sp.eye(self.n, format='csc')

    def retract(self, x, dx):
        return x+dx


class EqualizedOptimizable(Optimizable):
    """An Optimizable object automatically converts all inequality constraints
    into equality constraints with the method of slack variables.

    Usage
    -----
    >>> equalizedProblem = EqualizedOptimizable(problem)

    The optimizable object `problem` corresponds to the minimization program
        min J(x)
         x
        g_i(x) =  0 for i=1...p
        h_i(x) <= 0 for i=1..q

    The `equalizedProblem` corresponds to the equivalent program
        min J(x)
        (x, z)

        g_i(x)        = 0 for i=1..p
        h_i(x)+z_i**2 = 0 for i=1..q

    Optimization points for the `EqualizedOptimizable` object are tuples of the
    form `(x,z)` with `x` an optimization point for `problem` and `z` a list of
    size `q`.

    Initialization is built with the rule
    zi(0) = sqrt(2 |h_i(x(0))|) for i=1..q

    The inner product chosen on the z variable is the usual Euclidean inner
    product.  Derivatives with respect to the z variable are appended at the
    end of the derivative arrays with respect to x.
    """

    def __init__(self, problem):
        super().__init__()
        if problem.nineqconstraints == 0:
            raise Exception("Error, problem does not feature inequality "
                            "constraints")
        self.problem = problem
        self.nconstraints = problem.nconstraints+problem.nineqconstraints
        self.nineqconstraints = 0
        self.is_manifold = problem.is_manifold
        self.h_size = max(self.problem.h_size, 1e-4)

    def x0(self):
        x0 = self.problem.x0()
        (J, G, H) = self.problem.eval(x0)
        z = [np.sqrt(2 * abs(h)) for h in H]
        self._Optimizable__currentJ_x = (x0, z)
        newG = G+[h+0.5*zi**2 for (h, zi) in zip(H, z)]
        (self._Optimizable__J, self._Optimizable__G,
         self._Optimizable__H) = (J, newG, [])
        return (x0, z)

    def J(self, x):
        return self.problem.J(x[0])

    def G(self, x):
        oldG = self.problem.G(x[0])
        oldH = self.problem.H(x[0])
        oldH = [h+0.5*zi**2 for (h, zi) in zip(oldH, x[1])]
        return oldG+oldH

    def H(self, x):
        return []

    def dJ(self, x):
        return np.concatenate((self.problem.dJ(x[0]),
                               [0.0]*self.problem.nineqconstraints))

    def dG(self, x):
        old_dG = self.problem.dG(x[0])
        old_dG = [np.concatenate(
            (dgi, [0.0]*self.problem.nineqconstraints)) for dgi in old_dG]
        old_dH = self.problem.dH(x[0])
        old_dH = [np.concatenate((old_dH[i], [0.0]*i, [x[1][i]],
                                  [0.0]*(self.problem.nineqconstraints-i-1)))
                  for i in range(self.problem.nineqconstraints)]
        return old_dG+old_dH

    def dH(self, x):
        return []

    def inner_product(self, x):
        Aold = self.problem.inner_product(x[0])
        A = sp.block_diag(
            (Aold, *(1,)*self.problem.nineqconstraints), format='csc')
        return A

    def retract(self, x, dx):
        retractedOld = self.problem.retract(
            x[0], dx[:(-self.problem.nineqconstraints)])
        retractedZi = x[1]+dx[-self.problem.nineqconstraints:]
        return (retractedOld, retractedZi)

    def accept(self, results: dict):
        newresults = results.copy()
        newresults['H'] = [[gi-0.5*zi**2 for (gi, zi) in
                            zip(G[self.problem.nconstraints:], X[1])]
                           for (G, X) in zip(results['G'], results['x'])]
        newresults['G'] = [G[:self.problem.nconstraints] for G in results['G']]
        newresults['x'] = [x[0] for x in results['x']]
        self.problem.accept(newresults)


def checkOptimizable(problem: Optimizable, x, eps=1e-6):
    """
    Check the implementation of derivatives by using finite differences

    Input
    -----

    problem : an instance of the Optimizable class
    x       : a guess point
    eps     : increment for evaluating the finite difference

    """
    (J, G, H) = problem.eval(x)
    (dJ, dG, dH) = tuple(map(np.asarray, problem.eval_sensitivities(x)))
    if problem.is_manifold:
        # A must be recomputed
        A = problem.inner_product(x)
        import scipy.sparse.linalg as linalg
        if hasattr(A, 'tocsc'):
            A = A.tocsc()
            solve = linalg.factorized(A)
        dC = np.concatenate((dG, dH), axis=0)
        dJT = solve(dJ)
        dCT = np.zeros(dC.shape).T
        for i in (x for x in range(dC.shape[0])):
            dCT[:, i] = solve(dC[i, :])
    n = dC.shape[0]+1
    coeffs=  np.random.rand(n)
    #dx = coeffs[0]*dJ+dCT.dot(coeffs[1:])
    dx = dJT
    dx = dx/np.linalg.norm(dx,np.inf)*eps
    newx = problem.retract(x, dx)
    (newJ, newG, newH) = tuple(map(
        np.asarray, problem.eval(newx)))
    (checkJ, checkG, checkH) = ((newJ-J), (newG-G), (newH-H))
    (compareJ, compareG, compareH) = (dJ.dot(dx), dG.dot(dx), dH.dot(dx))
    print(f"J={J},G={G},H={H}")
    print(f"newJ={newJ},newG={newG},newH={newH}")
    print("Numerical sensitivities:")
    print(f"dJ.dx : \t expected {compareJ} vs. obtained {checkJ}")
    print(f"dG.dx : \t expected \n {compareG} \n vs. obtained \n {checkG}")
    print(f"dH.dx : \t expected \n {compareH} \n vs. obtained \n {checkH}")


class LightOptimizable(OptimizableBase):
    """
    A LightOptimizable class used by `nlspace_solve_light`. The `accept` method
    takes as an input the dictionary `result` which contains the current point
    of the optimization path.
    """
    def accept(self, results):
        """
        This function is called by nlspace_solve:
            - at the initialization
            - every time a new guess x is accepted on the optimization
              trajectory
        This allows to perform some post processing operations along the
        optimization trajectory. The function does not return any output but
        may update the dictionary `results` which may affect the optimization.
        Notably, the current point is stored in
            results['x']
        and an update of its value will be taken into account by nlspace_solve_light.

        In contrast with an `Optimizable` object, the dictionary result
        contains only information about the last point of the optimization path.
        (i.e. results['x'] is the current point, results['J'] the current objective
        function value, etc..., instead of being lists).

        Inputs:
            `results` : the current dictionary of results
        """
        pass


class LightEuclideanOptimizable(LightOptimizable):
    """A LightOptimizable class for optimization in Euclidean space
    of dimension `n`.

    Usage
    -----
    >>> optim = LightEuclideanOptimizable(n);

    where n is the dimension of the space.
    The inner product matrix is automatically set to the identity of size `n`
    The retraction is the usual translation:
         x_{n+1} = x_n + dx

    Attribute:
        `n`  : The dimension of the Euclidean space.
    """

    def __init__(self, n):
        super().__init__()
        self.n = n
        self._is_manifold = False

    def inner_product(self, x):
        return sp.eye(self.n, format='csc')

    def retract(self, x, dx):
        return x+dx


class TailOptimizable(Optimizable):
    """An adapter to convert a LightOptimizable into an Optimizable.

    Usage
    -----
    >>> opt = TailOptimizable(light_opt)
    """
    def __init__(self, impl: LightOptimizable):
        self.impl = impl
        self.nconstraints = impl.nconstraints
        self.nineqconstraints = impl.nineqconstraints
        self.is_manifold = impl.is_manifold
        self.h_size = impl.h_size

    def x0(self):
        return self.impl.x0()

    def J(self, x):
        return self.impl.J(x)

    def G(self, x):
        return self.impl.G(x)

    def H(self, x):
        return self.impl.H(x)

    def dJ(self, x):
        return self.impl.dJ(x)

    def dG(self, x):
        return self.impl.dG(x)

    def dH(self, x):
        return self.impl.dH(x)

    def dJT(self, x):
        return self.impl.dJT(x)

    def dGT(self, x):
        return self.impl.dGT(x)

    def dHT(self, x):
        return self.impl.dHT(x)

    def inner_product(self, x):
        return self.impl.inner_product(x)

    def retract(self, x, dx):
        return self.impl.retract(x, dx)

    def accept(self, results):
        tailResults = {}
        for k, v in results.items():
            if len(v) > 0:
                tailResults[k] = v[-1]
        self.impl.accept(tailResults)


class AppendOptimizable(LightOptimizable):
    """An adapter to convert an Optimizable into a LightOptimizable.

    Usage
    -----
    >>> light_opt = AppendOptimizable(opt)
    """
    def __init__(self, impl: Optimizable):
        self.impl = impl
        self._nconstraints = impl.nconstraints
        self._nineqconstraints = impl.nineqconstraints
        self._is_manifold = impl.is_manifold
        self._h_size = impl.h_size
        self._accumulatedResults = {}

    @property
    def accumulatedResults(self):
        return self._accumulatedResults

    def x0(self):
        return self.impl.x0()

    def J(self, x):
        return self.impl.J(x)

    def G(self, x):
        return self.impl.G(x)

    def H(self, x):
        return self.impl.H(x)

    def dJ(self, x):
        return self.impl.dJ(x)

    def dG(self, x):
        return self.impl.dG(x)

    def dH(self, x):
        return self.impl.dH(x)

    def dJT(self, x):
        return self.impl.dJT(x)

    def dGT(self, x):
        return self.impl.dGT(x)

    def dHT(self, x):
        return self.impl.dHT(x)

    def inner_product(self, x):
        return self.impl.inner_product(x)

    def retract(self, x, dx):
        return self.impl.retract(x, dx)

    def accept(self, results):
        for k, v in results.items():
            self._accumulatedResults.setdefault(k, []).append(v)
        self.impl.accept(self._accumulatedResults)
