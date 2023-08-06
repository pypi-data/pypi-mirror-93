import numpy as np
import numpy.testing as npt

from nullspace_optimizer.examples import ex0, ex1, ex2, ex3


def test_ex0_basic1():
    results = ex0.run_problem_1()
    actual = results['x'][-1]
    expected = np.asarray([1.82573056, 0.54772595])
    npt.assert_allclose(actual, expected, rtol=1.0e-5)

def test_ex0_basic1_restart():
    results = ex0.run_problem_1()
    resultsRestart = ex0.restart_problem_1(results)
    for key in results:
        npt.assert_equal(len(resultsRestart[key]), len(results[key]))
    npt.assert_allclose(resultsRestart['x'][-1], results['x'][-1])

def test_ex0_basic2():
    results = ex0.run_problem_2()
    actual = results['x'][-1]
    expected = np.asarray([1.5, 1.5])
    npt.assert_allclose(actual, expected, rtol=1.0e-5)

def test_ex0_parab():
    results = ex0.run_problem_parab()
    actual = results['x'][-1]
    expected = np.asarray([-2.5, 0.5])
    npt.assert_allclose(actual, expected, rtol=1.0e-5)

def test_ex1():
    results = ex1.run_problems()
    expected = np.asarray([-np.sqrt(1 - 0.7**2), -0.7])
    for r in results:
        actual = r['x'][-1]
        npt.assert_allclose(actual, expected)

def test_ex2():
    results = ex2.run_problems()
    solutions = ([0.5, 0.0], [-1.0, -1.2], [-1.0, 0.5], [-1.0, -0.5], [-1.0, 1.0])
    for r, e in zip(results, solutions):
        actual = r['x'][-1]
        expected = np.asarray(e)
        npt.assert_allclose(actual, expected, rtol=0.01)

def test_ex3():
    results = ex3.run_problems()
    actual = results['x'][-1]
    expected = np.zeros((2,))
    npt.assert_allclose(actual, expected, atol=5.0e-4)