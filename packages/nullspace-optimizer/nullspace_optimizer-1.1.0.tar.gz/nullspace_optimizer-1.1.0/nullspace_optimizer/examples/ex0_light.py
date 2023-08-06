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

from nullspace_optimizer.nullspace import nlspace_solve_light
from nullspace_optimizer.optimizable import LightEuclideanOptimizable
import numpy as np
import nullspace_optimizer.examples.draw as draw


class BasicProblem(LightEuclideanOptimizable):
    def __init__(self, accumulatedResults=None):
        super().__init__(2)
        self._nconstraints = 0
        self._nineqconstraints = 2
        if accumulatedResults is None:
            self._accumulatedResults = {}
        else:
            self._accumulatedResults = {k: v[:-1] for k, v in accumulatedResults.items()}

    @property
    def accumulatedResults(self):
        return self._accumulatedResults

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

    def accept(self, results):
        for k, v in results.items():
            if v is not None:
                self._accumulatedResults.setdefault(k, []).append(v)


def run_problem_1():
    params = {'alphaC': 1, 'debug': 0, 'alphaJ': 1, 'dt': 0.1, 'maxtrials': 1}
    pb = BasicProblem()
    results = nlspace_solve_light(pb, params)
    fullResults = pb.accumulatedResults
    return results, fullResults

def run_problem_1_short():
    params = {'alphaC': 1, 'debug': 0, 'alphaJ': 1, 'dt': 0.1, 'maxtrials': 1, 'maxit': 100}
    pb = BasicProblem()
    results = nlspace_solve_light(pb, params)
    fullResults = pb.accumulatedResults
    return results, fullResults

def run_restart_problem_1():
    resultsShort, fullResultsShort = run_problem_1_short()
    params = {'alphaC': 1, 'debug': 0, 'alphaJ': 1, 'dt': 0.1, 'maxtrials': 1}
    pb = BasicProblem(fullResultsShort)
    resultsRestart = nlspace_solve_light(pb, params, resultsShort)
    fullResultsRestart = pb.accumulatedResults
    return resultsRestart, fullResultsRestart

def main():
    results, fullResults = run_problem_1()
    print(f"Nullspace method ended in {results['it']} iterations.")

    input("\nWill test restarting, press any key")
    resultsNew, fullResultsNew = run_restart_problem_1()

    print("\nResults after restart:")
    for key in resultsNew:
        print("{0:<12} before restart: \t".format(key), len(fullResults[key]),
            " \t after restart:\t", len(fullResultsNew[key]))

    print("")
    print("Optimum :")
    print(results['x'])
    print("Comparison with restarting : ")
    print(resultsNew['x'])

    draw.ion()
    draw.drawProblem(BasicProblem(), XLIM=[0.2, 2.8], YLIM=[0.2, 2.8], resolution=200)
    draw.drawData(fullResults, 'NLSPACE', 'blue')

    draw.figure()
    draw.drawMuls(fullResults, 'NLSPACE')
    draw.legend()

    draw.figure()
    draw.drawJ(fullResults)
    draw.legend()

    draw.show()
    input("\nWill close all graphics. Press any key")
    draw.close('all')

if __name__ == "__main__":
    main()