"""Unittests for the functions module."""

import functions
import math

def test_eval():
    """Unittests for the eval functions."""
    assert functions.exp.eval(0) == 1
    assert functions.sin.eval(0) == 0
    assert functions.x.eval(functions.exp.eval(0)) == 1

def test_call():
    """Unittests for using the functions as callables"""
    assert functions.exp(0) == 1
    f = functions.exp(functions.log)
    assert f(3.3) == 3.3

def test_addition():
    """Tests the addition of functions."""
    f = functions.exp + functions.sin
    assert isinstance(f, functions.Function)
    f = functions.exp + functions.exp
    assert f.eval(0) == 2
    f = functions.exp + 2
    assert f.eval(0) == 3
    f = 3 + functions.sin
    assert f.eval(0) == 3

def test_subtraction():
    """Tests the subtraction of functions."""
    f = functions.exp - functions.sin
    assert isinstance(f, functions.Function)
    f = functions.exp - functions.exp
    assert f.eval(0) == 0
    f = functions.exp - 2
    assert f.eval(0) == -1
    f = 3 - functions.exp
    assert f.eval(0) == 2

def test_multiplication():
    """Tests the multiplication of functions."""
    f = functions.exp * functions.sin
    assert isinstance(f, functions.Function)
    f = functions.exp * functions.exp
    assert f.eval(0) == 1
    f = functions.exp * 2
    assert f.eval(0) == 2
    f = 3 * functions.exp
    assert f.eval(0) == 3

def test_divition():
    """Tests the division of functions."""
    f = functions.exp / functions.sin
    assert isinstance(f, functions.Function)
    f = functions.exp / functions.exp
    assert f.eval(0) == 1
    f = functions.exp / 2
    assert f.eval(0) == 0.5
    f = functions.exp / functions.sin #Is undefined at x=0
    assert math.isnan(f.eval(0))
    f = 1 / functions.x
    assert f.eval(2) == 0.5

def test_negation():
    """Tests the negation of functions."""
    f = -functions.exp
    assert f.eval(0) == -1

def test_pow():
    """Tests the exponentiation of functions"""
    f = functions.exp ** functions.sin
    assert isinstance(f, functions.Function)
    f = functions.exp ** functions.log
    assert f.eval(1) == 1
    f = (functions.exp ** 2) ** functions.log
    assert f.eval(2) == 16
    f = 3 ** functions.sin
    assert f.eval(0) == 1

def test_derivative():
    """Tests the derivative of functions"""
    f = functions.exp
    fd = f.derivative() # should be approximately the same as f
    assert isinstance(fd, functions.Function)
    # The two point numerical method for differentiation ensures that f'(x) = f.derivative(x) + O(dx^2).
    # Since dx^2 is 1e-8 we know that the result is at least 1e-7 close.
    assert math.isclose(fd(0), f(0), rel_tol=1e-7)
    assert math.isclose(fd(3), f(3), rel_tol=1e-7)
    fd = functions.log.derivative()
    f = 1/functions.x
    assert math.isclose(fd(3), f(3), rel_tol=1e-7)
    assert math.isclose(fd(43), f(43), rel_tol=1e-7)

def test_integral():
    """Tests the integral of functions"""
    f = functions.sin
    assert math.isclose(f.integral(0, math.pi, tol=1e-10), 2, rel_tol=1e-10)
    assert math.isclose(f.integral(0, math.pi*2, tol=1e-10), 0, abs_tol=1e-10)
    f = functions.x
    assert math.isclose(f.integral(0, 2, tol=1e-10), 2, rel_tol=1e-10)
    f = 1/functions.x
    assert math.isclose(f.integral(1, math.e, tol=1e-10), 1, rel_tol=1e-10)
    f = 1/(functions.x**0.5)
    # Since this is a generalized integral we cannot have the same tolerance
    assert math.isclose(f.integral(0, 1, tol=1e-10), 2, rel_tol=1e-3)
    f = 1/((functions.x**2)**(1/3))
    # Again this is a generalized integral
    assert math.isclose(f.integral(0, 1, tol=1e-10), 3, rel_tol=1e-3)
