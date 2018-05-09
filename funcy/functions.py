"""This module provides basic manipulation of mathematical functions.

Exported objects:
Function -- The base class for mathematical functions.
exp -- A Function instance relating to the exponential function.
sin -- A Function instance relating to the sine function.
arcsin -- A Function instance relating to the inverse sine function.
cos -- A Function instance relating to the cosine function.
arccos -- A Function instance relating to the inverse cosine function.
tan -- A Function instance relating to the tan function.
arctan -- A Function instance relating to the inverse tan function.
log -- A Function instance relating to the logarithmic function.
x -- A Function instance relating to the identity or (variable x) function.
sqrt -- A Function instance relating to the square root of x function.
"""

import math
from numbers import Number # Used only for checking isinstance(n, Number)
from multiprocessing import Process # Used by the plot method in the Function class

import matplotlib.pyplot as plt

__all__ = [
    'Function', 'exp', 'sin', 'arcsin', 'cos',
    'arccos', 'tan', 'arctan', 'log', 'x', 'sqrt'
    ]
__version__ = "1.0.0"
__author__ = "simmol"

class Function:
    """Class for creating and handling mathematical functions."""

    def __init__(self, func):
        """Set this functions eval method to return func(x).
        Where func is the function provided as input.

        Keyword arguments:
        func -- A function that takes a number as input and outputs another
                number according to some rule.
        """
        self._function = func

    def eval(self, num):
        """Return the evaluation of the function in the point "num"

        Keyword arguments:
        num -- A real number in the domain of the function
        """
        # This method is only here for the docstring otherwise it would be defined
        # in __init__ as self.eval = func and the user would have no clue as
        # to what eval actually does (except for the descriptive name of course).
        return self._function(num)

    def __call__(self, func_or_num):
        """If func_or_num is a real number return self.eval(func_or_num).
        If func_or_num is an instance of Function return a new Function
        instance whose eval returns self.eval(func_or_num(x)) for any input x.

        Keyword arguments:
        func_or_num -- An instance of Function OR a real number.

        Examples:   exp(sin), would return a new Function that evaluates according to e^(sin(x)).
                    exp(3), would return the same thing as exp.eval(3)
        """
        if isinstance(func_or_num, Number):
            return self.eval(func_or_num)

        elif isinstance(func_or_num, Function):
            def func(num):
                return self.eval(func_or_num(num))
            return Function(func)

        else:
            raise TypeError("can only call a function on a real number or another function.")

    def __neg__(self):
        """Return a new instance of Function that evaluates as -self.eval."""
        def func(arg):
            return -self.eval(arg)
        return Function(func)

    def __pos__(self):
        """Return self."""
        return self

    def __abs__(self):
        """Return an instance of Function that evaluates as |self.eval| i.e. abs(self.eval)"""
        return Function(lambda num: abs(self.eval(num)))

    def __add__(self, func_or_num):
        """Return an instance of Function whose eval method returns self.eval + func_or_num.

        Keyword arguments:
        func_or_num -- An instance of Function OR a real number.

        Example: exp + sin, would return a new Function that evaluates according to e^x + sin(x).
        """
        if isinstance(func_or_num, Function):
            def added(num):
                return self.eval(num) + func_or_num.eval(num)

        elif isinstance(func_or_num, Number):
            def added(num):
                return self.eval(num) + func_or_num

        else:
            raise TypeError("unsupported operand type for +.\
            Functions can only be added with real numbers or\
            other functions.")

        return Function(added)

    def __radd__(self, func_or_num):
        """Does self.__add__(func_or_num)"""
        return self.__add__(func_or_num)

    def __sub__(self, func_or_num):
        """Return an instance of Function whose eval method returns self.eval - func_or_num.

        Keyword arguments:
        func_or_num -- An instance of Function OR a real number.

        Example: exp - sin, would return a Function that evaluates to e^x - sin(x).
        """
        if isinstance(func_or_num, Function):
            def subtracted(num):
                return self.eval(num) - func_or_num.eval(num)

        elif isinstance(func_or_num, Number):
            def subtracted(num):
                return self.eval(num) - func_or_num

        else:
            raise TypeError("unsupported operand type for -.\
            Functions can only be subtracted with real numbers or\
            other functions.")

        return Function(subtracted)

    def __rsub__(self, func_or_num):
        """Does func_or_num - self"""
        negated = -self
        return negated.__add__(func_or_num)

    def __mul__(self, func_or_num):
        """Return an instance of Function whose eval method is self.eval * func_or_num.

        Keyword arguments:
        func_or_num -- An instance of Function OR a real number.

        Example: exp * sin, would return a Function that evaluates to e^x * sin(x).
        """
        if isinstance(func_or_num, Function):
            def multiplied(num):
                return self.eval(num) * func_or_num.eval(num)

        elif isinstance(func_or_num, Number):
            def multiplied(num):
                return self.eval(num) * func_or_num

        else:
            raise TypeError("unsupported operand type for *.\
            Functions can only be multiplied with real numbers or\
            other functions.")

        return Function(multiplied)

    def __rmul__(self, func_or_num):
        """Does self.__mul__(func_or_num)"""
        return self.__mul__(func_or_num)

    def __truediv__(self, func_or_num):
        """Return an instance of Function whose eval method is self.eval / func_or_num.

        Keyword arguments:
        func_or_num -- An instance of Function OR a real number.

        Example: exp / sin, would return a Function that evaluates to e^x / sin(x).
        """
        # Here special consideration is needed in order to
        # handle cases where func_or_num evaluates to 0
        if isinstance(func_or_num, Function):
            def divided(num):
                if func_or_num.eval(num) == 0:
                    return float("nan")
                return self.eval(num) / func_or_num.eval(num)

        elif isinstance(func_or_num, Number):
            if func_or_num == 0:
                def divided(num):
                    return float("nan")
            else:
                def divided(num):
                    return self.eval(num) / func_or_num

        else:
            raise TypeError("unsupported operand type for /.\
            Functions can only be divided with real numbers or\
            other functions.")

        return Function(divided)

    def __rtruediv__(self, func_or_num):
        """Does (1/self) * func_or_num instead"""
        def inverse(num):
            val = self.eval(num)
            if val == 0:
                return float("nan")
            return 1/val
        inversed = Function(inverse)
        return inversed.__mul__(func_or_num)

    def __pow__(self, func_or_num):
        """Return an instance of Function whose eval method is self.eval^func_or_num.

        Keyword arguments:
        func_or_num -- An instance of Function OR a real number.

        Example: exp^sin, would return a Function that evaluates to (e^x)^sin(x).
        """
        if isinstance(func_or_num, Function):
            def power(num):
                return self.eval(num) ** func_or_num.eval(num)

        elif isinstance(func_or_num, Number):
            def power(num):
                return self.eval(num) ** func_or_num

        else:
            raise TypeError("unsupported operand type for **.\
            Functions can only be raised by a real number or\
            another function.")

        return Function(power)

    def __rpow__(self, func_or_num):
        """Rewrite func_or_num^self as (e^self)^log(func_or_num)"""
        ln_func_or_num = Function(math.log)(func_or_num)
        exp_self = Function(math.exp)(self)
        return exp_self.__pow__(ln_func_or_num)


    def derivative(self, dx=0.0001):
        """Return a new instance of Function that evaluates to the derivative of this
        function in each point.

        Keyword arguments:
        dx --   a real number that determines the step in the two point difference method
                for calculating derivatives (defaults to 0.0001).

        Using the two point differential method ensures that the result is as close as O(dx^2).
        """
        def deriv(num, h=dx):
            if math.isnan(self.eval(num)):
                # Cannot calculate derivative in this point
                return float("nan")

            f_posh = self.eval(num+h)
            f_negh = self.eval(num-h)

            # Defaults to the one point difference method if either of the points is
            # nan. This means we happened to come across a singularity.
            if math.isnan(f_posh):
                f_posh = self.eval(num)
                h = h/2
            elif math.isnan(f_negh):
                f_negh = self.eval(num)
                h = h/2
            df = f_posh - f_negh
            return df/(2*h)

        return Function(deriv)

    def integral(self, start, end, tol=1e-5):
        """Return the definite integral from start to end of this function.

        Keyword arguments:
        start -- A real number being the startingpoint of the integral.
        end -- A real number being the endpoint of the integral.
        tol -- The the accepted tolerance of the evaluation (defaults to 1e-5).

        The algorithm uses a version of Simpson's 3/8 rule.
        https://en.wikipedia.org/wiki/Simpson%27s_rule#Simpson's_3/8_rule
        https://en.wikipedia.org/wiki/Adaptive_Simpson%27s_method
        """
        # If either endpoint is a singularity it is a generalized integral
        if math.isnan(self.eval(start)):
            start += tol**3 # Ensures the tolerance is met
        if math.isnan(self.eval(end)):
            end -= tol**3

        midpoint = (start + end)/2
        left = self._simpsons_rule(start, midpoint)
        right = self._simpsons_rule(midpoint, end)
        whole = self._simpsons_rule(start, end)

        if abs(left + right - whole) < 15*tol:
            return left + right + (left + right - whole)/15
        return self.integral(start, midpoint, tol) + self.integral(midpoint, end, tol)

    def _simpsons_rule(self, start, end):
        """Return the calculation of simpson's 3/8 rule on the interval from start
        to end with this function.

        Keyword arguments:
        start -- A real number being the startingpoint of the integral.
        end -- A real number being the endpoint of the integral.
        """
        return ((end - start)/8
                * (self.eval(start)
                + 3*self.eval((2*start + end)/3)
                + 3*self.eval((start  + 2*end)/3)
                + self.eval(end)))

    def plot(self, start, end, step=0.01):
        """Start a new process that shows the plot of the function from start to end.

        Keyword arguments:
        start -- The real number at which the x-axis starts
        end -- The real number at which the x-axis ends
        step -- A real number for the fineness of the plot (defaults to 0.01)
        """
        Process(target=self._plot, args=(start, end, step)).start()

    def _plot(self, start, end, step):
        """Plot this function from "start" to "end" with step size "step".

        Keyword arguments:
        start -- The real number at which the x-axis starts
        end -- The real number at which the x-axis ends
        step -- A real number for the fineness of the plot (defaults to 0.01)
        """
        domain = []
        curr = start
        while curr < end:
            domain.append(curr)
            curr += step
        domain.append(end)
        f_evals = [self.eval(x) for x in domain if not math.isnan(self.eval(x))]
        plt.plot(domain, f_evals)
        plt.show()


# Constants in this module
exp = Function(math.exp)
def _log(num):
    """Return ln(num) if num > 0 otherwise return nan.

    Keyword arguments:
    num -- A real number
    """
    if num <= 0:
        return float("nan")
    return math.log(num)
log = Function(_log)
sin = Function(math.sin)
arcsin = Function(math.asin)
cos = Function(math.cos)
arccos = Function(math.acos)
tan = Function(math.tan)
arctan = Function(math.atan)
sqrt = Function(math.sqrt)
x = Function(lambda num: num) # Identity function
