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

from nullspace_optimizer import *
import numpy as np
import nullspace_optimizer.examples.draw as draw


class basicProblem(EuclideanOptimizable):
    def __init__(self):
        super().__init__(2)
        self.nconstraints = 0
        self.nineqconstraints = 2

    def x0(self):
        return [1.5, 2.25]

    def J(self, x):
        return x[1]+0.3*x[0]

    def dJ(self, x):
        return [0.3, 1]

    def H(self, x):
        return [-x[1]+1.0/x[0], -(3-x[0]-x[1])]

    def dH(self, x):
        return [[-1.0/x[0]**2, -1], [1, 1]]


def run_problem_1(**other_params):
    params = {'alphaC': 1, 'debug': 0, 'alphaJ': 1, 'dt': 0.1, 'maxtrials': 1}
    params.update(other_params)
    results = nlspace_solve(basicProblem(), params)
    return results


def run_problem_equalized_1(**other_params):
    params = {'alphaC': 1, 'debug': 0, 'alphaJ': 1, 'dt': 0.1, 'maxtrials': 1}
    params.update(other_params)
    resultsEqualized = nlspace_solve(
        EqualizedOptimizable(basicProblem()), params)
    resultsEqualized['x'] = [list(x[0])+list(x[1])
                             for x in resultsEqualized['x']]
    return resultsEqualized


def restart_problem_1(results, **other_params):
    resultsCopy = results.copy()
    for key in results:
        resultsCopy[key] = results[key].copy()[:100]
    params = {'alphaC': 1, 'debug': 0, 'alphaJ': 1, 'dt': 0.1, 'maxtrials': 1}
    params.update(other_params)
    return nlspace_solve(basicProblem(), params, resultsCopy)


class basicProblem2(EuclideanOptimizable):
    def __init__(self):
        super().__init__(2)
        self.nineqconstraints = 2
        self.nconstraints = 0

    def x0(self):
        return [1.5, 2.25]

    def J(self, x):
        return (x[0]-2)**2+(x[1]-2)**2

    def dJ(self, x):
        return [2*(x[0]-2), 2*(x[1]-2)]

    def H(self, x):
        return [-x[1]+1.0/x[0], -(3-x[0]-x[1])]

    def dH(self, x):
        return [[-1.0/x[0]**2, -1], [1, 1]]


def run_problem_equalized_2(**other_params):
    params = {'alphaC': 0.2, 'alphaJ': 1, 'dt': 0.1}
    params.update(other_params)
    resultsEqualized = nlspace_solve(
        EqualizedOptimizable(basicProblem2()), params)
    resultsEqualized['x'] = [list(x[0])+list(x[1])
                             for x in resultsEqualized['x']]
    return resultsEqualized


def run_problem_2(**other_params):
    params = {'alphaC': 0.2, 'alphaJ': 1, 'dt': 0.1}
    params.update(other_params)
    return nlspace_solve(basicProblem2(), params)


class parabProblem(EuclideanOptimizable):
    def __init__(self):
        super().__init__(2)
        self.nconstraints = 0
        self.nineqconstraints = 2

    def x0(self):
        return [3, 3]

    def J(self, x):
        return x[1]**2+(x[0]+3)**2

    def dJ(self, x):
        return [2*(x[0]+3), 2*x[1]]

    def H(self, x):
        return [-x[0]**2+x[1], -x[1]-x[0]-2]

    def dH(self, x):
        return [[-2*x[0], 1], [-1, -1]]


def run_problem_parab(**other_params):
    params = {'alphaC': 0.2, 'alphaJ': 1,  'dt': 0.1}
    params.update(other_params)
    return nlspace_solve(parabProblem(), params)


def run_problem_parab_equalized(**other_params):
    params = {'alphaC': 0.2, 'alphaJ': 1,  'dt': 0.1}
    params.update(other_params)
    resultsEqualized = nlspace_solve(
        EqualizedOptimizable(parabProblem()), params)
    resultsEqualized['x'] = [list(x[0])+list(x[1])
                             for x in resultsEqualized['x']]
    return resultsEqualized


def run_problem_parab_osqp(**other_params):
    params = {'alphaC': 0.2, 'alphaJ': 1,  'dt': 0.1, 'qp_solver': 'osqp'}
    params.update(other_params)
    return nlspace_solve(parabProblem(), params)


def main(**options):
    results = run_problem_1(**options)
    resultsEqualized = run_problem_equalized_1(**options)
    print(f"Method of slack ended in {len(resultsEqualized['J'])} iterations.")
    print(f"Nullspace method ended in {len(results['J'])} iterations.")

    input("\nWill test restarting, press any key")
    resultsNew = restart_problem_1(results, **options)

    print("\nResults after restart:")
    for key in resultsNew:
        print("{0:<10} before restart: \t".format(key), len(results[key]),
              " \t after restart:\t", len(resultsNew[key]))

    print("")
    print("Optimum :")
    print(results['x'][-1])
    print("Comparison with restarting : ")
    print(resultsNew['x'][-1])

    draw.ion()
    draw.drawProblem(basicProblem(), XLIM=[0.2, 2.8], YLIM=[
                     0.2, 2.8], resolution=200)
    draw.drawData(resultsEqualized, 'EQUALIZED', 'green', x0=True)
    draw.drawData(results, 'NLSPACE', 'blue')

    draw.figure()
    draw.drawMuls(results, 'NLSPACE')
    draw.legend()

    draw.figure()
    draw.drawJ(results)
    draw.drawJ(resultsEqualized, 'EQUALIZED', linestyle='--')
    draw.legend()

    draw.show()

    input("\nWill run basic problem 2. Press any key")
    draw.close('all')

    resultsEqualized = run_problem_equalized_2(**options)
    draw.drawData(resultsEqualized, 'EQUALIZED',
                  'green', loc='lower left', x0=True)

    results = run_problem_2(**options)
    print("")
    print("Optimum :")
    print(results['x'][-1])
    print(f"Method of slack ended in {len(resultsEqualized['J'])} iterations.")
    print(f"Nullspace method ended in {len(results['J'])} iterations.")
    draw.drawProblem(basicProblem2(), XLIM=[0.04, 3], YLIM=[
                     0.2, 2.7], resolution=200)
    draw.drawData(results, 'NLSPACE', 'blue', loc='lower left')

    draw.figure()
    draw.drawMuls(results, 'NLSPACE')
    draw.legend()

    draw.figure()
    draw.drawJ(results)
    draw.drawJ(resultsEqualized, 'EQUALIZED', linestyle='--')
    draw.legend()

    draw.figure()
    draw.drawC(results)
    draw.drawC(resultsEqualized, 'EQUALIZED', linestyle='--')
    draw.legend()

    input("\nWill run parab problem. Press any key")
    draw.close('all')

    draw.drawProblem(parabProblem(), XLIM=[-3.5, 5], YLIM=[-1.3, 3.2])
    resultsEqualized = run_problem_parab_equalized(**options)
    draw.drawData(resultsEqualized, 'EQUALIZED',
                  'green', loc='lower right', x0=True)

    resultsOSQP = run_problem_parab_osqp(**options)
    draw.drawData(resultsOSQP, 'NLSPACE (OSQP)', 'orange',
                  loc='lower right', x0=True, linestyle='-')

    results = run_problem_parab(**options)
    print("")
    print("Optimum :")
    print(results['x'][-1])
    print(f"Method of slack ended in {len(resultsEqualized['J'])} iterations.")
    print(
        f"Nullspace method (CVXOPT) ended in {len(results['J'])} iterations.")
    print(
        f"Nullspace method (OSQP) ended in {len(resultsOSQP['J'])} iterations.")
    draw.drawData(results, 'NLSPACE', 'blue', loc='lower right')

    draw.figure()
    draw.drawMuls(results, 'NLSPACE (CVXOPT)')
    draw.drawMuls(resultsOSQP, 'NLSPACE (OSQP)', linestyle='--')
    draw.legend()

    draw.figure()
    draw.drawJ(results)
    draw.drawJ(resultsOSQP, linestyle=':')
    draw.drawJ(resultsEqualized, 'EQUALIZED', linestyle='--')
    draw.legend()

    draw.figure()
    draw.drawC(resultsOSQP, linestyle=':')
    draw.drawC(resultsEqualized, 'EQUALIZED', linestyle='--')
    draw.legend()

    draw.show()
    input("Press any key to close all plots")
    draw.close('all')


if __name__ == "__main__":
    import sys
    options = dict()
    if '--osqp' in sys.argv:
        options.update(qp_solver='osqp')
    if '--qpverbose' in sys.argv:
        options.update(show_progress_qp=True)
    main(**options)
