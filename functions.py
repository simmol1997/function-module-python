"""This module provides basic manipulation of mathematical functions."""

import math
from numbers import Number #Used only for checking isinstance(n, Number)

__all__ = []
__version__ = "1.0"
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
        self.eval = func

    def __call__(self, func_or_num):
        """If func_or_num is a real number return self.eval(func_or_num).
        If func_or_num is an instance of Function return a new Function
        instance whose eval returns self.eval(func_or_num(x)) for any input x.

        Keyword arguments:
        func_or_num -- An instance of this class OR a real number.

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

    def __add__(self, func_or_num):
        """Return an instance of this class whose eval method returns self.eval + func_or_num.

        Keyword arguments:
        func_or_num -- An instance of this class OR a real number.

        Example: exp + sin, would return a new Function that evaluates according to e^x + sin(x).
        """
        if isinstance(func_or_num, Function):
            def added(arg):
                return self.eval(arg) + func_or_num.eval(arg)

        elif isinstance(func_or_num, Number):
            def added(arg):
                return self.eval(arg) + func_or_num

        else:
            raise TypeError("unsupported operand type for +.\
            Functions can only be added with real numbers or\
            other functions.")

        return Function(added)

    def __radd__(self, func_or_num):
        """Does self.__add__(func_or_num)"""
        return self.__add__(func_or_num)

    def __sub__(self, func_or_num):
        """Return an instance of this class whose eval method returns self.eval - func_or_num.

        Keyword arguments:
        func_or_num -- An instance of this class OR a real number.

        Example: exp - sin, would return a Function that evaluates to e^x - sin(x).
        """
        if isinstance(func_or_num, Function):
            def subtracted(arg):
                return self.eval(arg) - func_or_num.eval(arg)

        elif isinstance(func_or_num, Number):
            def subtracted(arg):
                return self.eval(arg) - func_or_num

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
        """Return an instance of this class whose eval method is self.eval * func_or_num.

        Keyword arguments:
        func_or_num -- An instance of this class OR a real number.

        Example: exp * sin, would return a Function that evaluates to e^x * sin(x).
        """
        if isinstance(func_or_num, Function):
            def multiplied(arg):
                return self.eval(arg) * func_or_num.eval(arg)

        elif isinstance(func_or_num, Number):
            def multiplied(arg):
                return self.eval(arg) * func_or_num

        else:
            raise TypeError("unsupported operand type for *.\
            Functions can only be multiplied with real numbers or\
            other functions.")

        return Function(multiplied)

    def __rmul__(self, func_or_num):
        """Does self.__mul__(func_or_num)"""
        return self.__mul__(func_or_num)

    def __truediv__(self, func_or_num):
        """Return an instance of this class whose eval method is self.eval / func_or_num.

        Keyword arguments:
        func_or_num -- An instance of this class OR a real number.

        Example: exp / sin, would return a Function that evaluates to e^x / sin(x).
        """
        # Here special consideration is needed in order to
        # handle cases where func_or_num evaluates to 0
        if isinstance(func_or_num, Function):
            def divided(arg):
                if func_or_num.eval(arg) == 0:
                    return float("nan")
                return self.eval(arg) / func_or_num.eval(arg)

        elif isinstance(func_or_num, Number):
            if func_or_num == 0:
                def divided(arg):
                    return float("nan")
            else:
                def divided(arg):
                    return self.eval(arg) / func_or_num

        else:
            raise TypeError("unsupported operand type for /.\
            Functions can only be divided with real numbers or\
            other functions.")

        return Function(divided)

    def __rtruediv__(self, func_or_num):
        """Does (1/self) * func_or_num instead"""
        def inverse(arg):
            val = self.eval(arg)
            if val == 0:
                return float("nan")
            return 1/val
        inversed = Function(inverse)
        return inversed.__mul__(func_or_num)

    def __pow__(self, func_or_num):
        """Return an instance of this class whose eval method is self.eval^func_or_num.

        Keyword arguments:
        func_or_num -- An instance of this class OR a real number.

        Example: exp^sin, would return a Function that evaluates to (e^x)^sin(x).
        """
        if isinstance(func_or_num, Function):
            def power(arg):
                return self.eval(arg) ** func_or_num.eval(arg)

        elif isinstance(func_or_num, Number):
            def power(arg):
                return self.eval(arg) ** func_or_num

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
        def deriv(arg, h):
            if math.isnan(self.eval(arg)):
                # Cannot calculate derivative in this point
                return float("nan")

            f_posh = self.eval(arg+h)
            f_negh = self.eval(arg-h)

            # Defaults to the one point difference method if either of the points is
            # nan. This means we happened to come across a singularity.
            if math.isnan(f_posh):
                f_posh = self.eval(arg)
                h = h/2
            elif math.isnan(f_negh):
                f_negh = self.eval(arg)
                h = h/2
            df = f_posh - f_negh
            return df/(2*h)

        return Function(lambda arg: deriv(arg, dx))

    def integral(self, start, end, init_step=0.0001):
        """Return the definite integral from start to end of this function.

        Keyword arguments:
        start -- A real number being the startingpoint of the integral.
        end -- A real number being the endpoint of the integral.
        init_step -- The initial value of the interval size.

        The algorithm uses a version of Simpson's 3/8 rule where the step size is
        decreased and increased based on the functions derivative.
        (https://en.wikipedia.org/wiki/Simpson%27s_rule#Simpson's_3/8_rule)
        """
        # The following ensures that the step size is at least 1/10 of the interval
        # and that if end is less than start we backtrack instead of moving forward.
        init_step = math.copysign(min(init_step, (end-start)/10), end-start)
        f = self # Makes it more readable later

        # The step size in the derivative must be smaller than in the integral
        # in case of the integral being generalized.
        deriv = f.derivative(dx=init_step/2)
        # h is the "local" step size and depends on the derivative and init_step
        h = init_step

        # If either endpoint is a singularity it is a generalized integral
        if math.isnan(self.eval(start)):
            start += init_step
        if math.isnan(self.eval(end)):
            end -= init_step

        x_i = start
        acc_int = 0 # Accumulates the value of the integral

        while x_i + init_step < end:
            # local_step is determined by the magnitude of the derivative
            h = min(abs(1/(10*deriv.eval(x_i))), abs(init_step))
            # Calculates the integral from x_i to x_i+h using Simpson's 3/8 rule
            acc_int += (h/8)*(f(x_i) + 3*f((3*x_i + h)/3) + 3*f((3*x_i + 2*h)/3) + f(x_i + h))
            x_i += h

        # There is one interval left from x_i to end
        h = end - x_i
        acc_int += (h/8)*(f(x_i) + 3*f((3*x_i + h)/3) + 3*f((3*x_i + 2*h)/3) + f(x_i + h))

        return acc_int


# Constants in this module
exp = Function(math.exp)
log = Function(math.log)
sin = Function(math.sin)
arcsin = Function(math.asin)
cos = Function(math.cos)
arccos = Function(math.acos)
tan = Function(math.tan)
arctan = Function(math.atan)
sqrt = Function(math.sqrt)
x = Function(lambda arg: arg) # Identity function
