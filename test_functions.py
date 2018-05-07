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
