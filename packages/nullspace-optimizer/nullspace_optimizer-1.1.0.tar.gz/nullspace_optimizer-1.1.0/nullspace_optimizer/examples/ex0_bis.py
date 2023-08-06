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
try:
    import matplotlib.cm as cm
    import matplotlib.mlab as mlab
    import matplotlib.pyplot as plt
    from nullspace_optimizer.examples.draw import *
    with_plot = True
    plt.ion()
except Exception:
    with_plot = False


class basicProblemDegenerate(EuclideanOptimizable):
    def __init__(self):
        super().__init__(2)
        self.nconstraints = 0
        self.nineqconstraints = 3

    def x0(self):
        return [1.5, 2.25]

    def J(self, x):
        return x[1]+0.3*x[0]

    def dJ(self, x):
        return [0.3, 1]

    def H(self, x):
        return [-x[1]+1.0/x[0], -(3-x[0]-x[1]), 0*x[0]]

    def dH(self, x):
        return [[-1.0/x[0]**2, -1], [1, 1], [0,0]]


def run_problem_1(**other_params):
    params = {'alphaC': 1, 'debug': 0, 'alphaJ': 1, 'dt': 0.1, 'maxtrials': 1}
    params.update(other_params)
    results = nlspace_solve(basicProblemDegenerate(), params)
    return results


def run_problem_equalized_1(**other_params):
    params = {'alphaC': 1, 'debug': 0, 'alphaJ': 1, 'dt': 0.1, 'maxtrials': 1}
    params.update(other_params)
    resultsEqualized = nlspace_solve(
        EqualizedOptimizable(basicProblemDegenerate()), params)
    resultsEqualized['x'] = [list(x[0])+list(x[1])
                             for x in resultsEqualized['x']]
    return resultsEqualized


def restart_problem_1(results, **other_params):
    resultsCopy = results.copy()
    for key in results:
        resultsCopy[key] = results[key].copy()[:100]
    params = {'alphaC': 1, 'debug': 0, 'alphaJ': 1, 'dt': 0.1, 'maxtrials': 1}
    params.update(other_params)
    return nlspace_solve(basicProblemDegenerate(), params, resultsCopy)

def main():
    results = run_problem_1()
    resultsEqualized = run_problem_equalized_1()
    print(f"Method of slack ended in {len(resultsEqualized['J'])} iterations.")
    print(f"Nullspace method ended in {len(results['J'])} iterations.")

    input("\nWill test restarting, press any key")
    resultsNew = restart_problem_1(results)

    print("\nResults after restart:")
    for key in resultsNew:
        print("{0:<10} before restart: \t".format(key), len(results[key]),
              " \t after restart:\t", len(resultsNew[key]))

    print("")
    print("Optimum :")
    print(results['x'][-1])
    print("Comparison with restarting : ")
    print(resultsNew['x'][-1])

if __name__ == "__main__":
    main()
