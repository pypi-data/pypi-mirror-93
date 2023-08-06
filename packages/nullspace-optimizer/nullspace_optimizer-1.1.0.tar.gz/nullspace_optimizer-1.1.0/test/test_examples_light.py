import numpy as np
import numpy.testing as npt

from nullspace_optimizer.examples import ex0_light, ex0
from nullspace_optimizer.nullspace import nlspace_solve, nlspace_solve_light
from nullspace_optimizer.optimizable import AppendOptimizable, TailOptimizable


def test_light_problem_1():
    results, _ = ex0_light.run_problem_1()
    actual = results['x']
    expected = np.asarray([1.82573056, 0.54772595])
    npt.assert_allclose(actual, expected, rtol=1.0e-5)

def test_light_problem1_restart():
    results, fullResults = ex0_light.run_problem_1()
    resultsRestart, fullResultsRestart = ex0_light.run_restart_problem_1()
    for k, v in results.items():
        npt.assert_equal(resultsRestart[k], v)
    for k, v in fullResults.items():
        npt.assert_equal(fullResultsRestart[k], v)

def run_adapted_problem_1():
    params = {'alphaC': 1, 'debug': 0, 'alphaJ': 1, 'dt': 0.1, 'maxtrials': 1}
    pb = TailOptimizable(ex0_light.BasicProblem())
    results = nlspace_solve(pb, params)
    return results

def restart_adapted_problem_1(results):
    resultsCopy = results.copy()
    for key in results:
        resultsCopy[key] = results[key].copy()[:100]
    params = {'alphaC': 1, 'debug': 0, 'alphaJ': 1, 'dt': 0.1, 'maxtrials': 1}
    pb = TailOptimizable(ex0_light.BasicProblem())
    return nlspace_solve(pb, params, resultsCopy)

def test_ex0_basic1():
    results = run_adapted_problem_1()
    actual = results['x'][-1]
    expected = np.asarray([1.82573056, 0.54772595])
    npt.assert_allclose(actual, expected, rtol=1.0e-5)

def test_ex0_basic1_restart():
    results = run_adapted_problem_1()
    resultsRestart = restart_adapted_problem_1(results)
    for key in results:
        npt.assert_equal(len(resultsRestart[key]), len(results[key]))
    npt.assert_allclose(resultsRestart['x'][-1], results['x'][-1])

def run_roundtrip_problem_1():
    params = {'alphaC': 1, 'debug': 0, 'alphaJ': 1, 'dt': 0.1, 'maxtrials': 1}
    inner_pb = AppendOptimizable(ex0.basicProblem())
    results = nlspace_solve(TailOptimizable(inner_pb), params)
    return (inner_pb, results)

def restart_roundtrip_problem_1(results):
    resultsCopy = results.copy()
    for key in results:
        resultsCopy[key] = results[key].copy()[:100]
    params = {'alphaC': 1, 'debug': 0, 'alphaJ': 1, 'dt': 0.1, 'maxtrials': 1}
    inner_pb = AppendOptimizable(ex0.basicProblem())
    results = nlspace_solve(TailOptimizable(inner_pb), params, resultsCopy)
    return (inner_pb, results)

def test_roundtrip_problem_1():
    _, results = run_roundtrip_problem_1()
    actual = results['x'][-1]
    expected = np.asarray([1.82573056, 0.54772595])
    npt.assert_allclose(actual, expected, rtol=1.0e-5)

def test_roundtrip_problem_1_restart():
    _, results = run_roundtrip_problem_1()
    _, resultsRestart = restart_roundtrip_problem_1(results)
    for key in results:
        npt.assert_equal(len(resultsRestart[key]), len(results[key]))
    npt.assert_allclose(resultsRestart['x'][-1], results['x'][-1])

def test_results_roundtrip_problem_1():
    pb, expected = run_roundtrip_problem_1()
    actual = pb.accumulatedResults
    assert actual == expected
