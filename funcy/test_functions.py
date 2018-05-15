"""Unittests for the functions module."""

from funcy import functions
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

def test_abs():
    """Tests that the absolute value of functions works."""
    f = abs(functions.x)
    assert isinstance(f, functions.Function)
    assert f.eval(-5) == 5
    f = abs(functions.sin)
    for i in range(100):
        assert f.eval(i) >= 0

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
    assert math.isclose(fd(0), f(0), abs_tol=1e-7)
    assert math.isclose(fd(3), f(3), abs_tol=1e-7)
    fd = functions.log.derivative()
    f = 1/functions.x
    assert math.isclose(fd(3), f(3), abs_tol=1e-7)
    assert math.isclose(fd(43), f(43), abs_tol=1e-7)
    # Tests that the behaviour of the derivative is not broken in weird points.
    f = abs(functions.x).derivative()
    # Should be 0 since the algorithm takes point on equal distances around the point
    assert f.eval(0) == 0
    f = abs(functions.sin).derivative()
    assert f.eval(0) == 0

def test_integrate():
    """Tests the integral of functions"""
    f = functions.sin
    assert math.isclose(f.integrate(0, math.pi, tol=1e-10), 2, abs_tol=1e-10)
    assert math.isclose(f.integrate(0, math.pi*2, tol=1e-10), 0, abs_tol=1e-10)
    f = functions.x
    assert math.isclose(f.integrate(0, 2, tol=1e-10), 2, abs_tol=1e-10)
    f = 1/functions.x
    assert math.isclose(f.integrate(1, math.e, tol=1e-10), 1, abs_tol=1e-10)
    # Generalized integrals tested below
    f = 1/(functions.x**0.5)
    assert math.isclose(f.integrate(0, 1, tol=1e-10), 2, abs_tol=1e-10)
    f = 1/((functions.x**2)**(1/3))
    assert math.isclose(f.integrate(0, 1, tol=1e-10), 3, abs_tol=1e-10)
    # Test some divergent integrals
    f = 1/(functions.x**2)
    assert math.isnan(f.integrate(0,1))
    f = 1/(functions.x - 1)**2
    assert math.isnan(f.integrate(0,2))

def test_norm():
    """Tests the norm function in the functions module."""
    assert math.isnan(functions.norm(functions.exp))
    assert math.isnan(functions.norm(functions.sin))
    assert math.isnan(functions.norm(functions.tan))
    assert math.isnan(functions.norm(functions.x))
    f = functions.exp(-functions.x**2)
    norm = math.sqrt(math.sqrt(math.pi/2))
    assert math.isclose(functions.norm(f, tol=1e-5), norm, abs_tol=1e-5)
    norm = math.sqrt(math.pi)
    assert math.isclose(functions.norm(f, norm_type="L1", tol=1e-5), norm, abs_tol=1e-5)
    f = f * functions.sin
    norm = math.sqrt(1/4 * (math.sqrt(2*math.pi) - math.sqrt(2*math.pi/math.e)))
    assert math.isclose(functions.norm(f, tol=1e-5), norm, abs_tol=1e-5)
    f = 1/functions.x
    assert math.isnan(functions.norm(f))
    f = f**2
    assert math.isnan(functions.norm(f))
