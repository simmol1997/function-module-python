"""This module provides basic manipulation of mathematical functions."""

__all__ = []
__version__ = "1.0"
__author__ = "simmol"

import math
from numbers import Number #Used only for checking isinstance(n, Number)

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
        """Returns itself."""
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
        """Returns an instance of this class whose eval method returns self.eval - func_or_num.

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
        f = -self
        return f.__add__(func_or_num)

    def __mul__(self, func_or_num):
        """Returns an instance of this class whose eval method is self.eval * func_or_num.

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
        """Returns an instance of this class whose eval method is self.eval / func_or_num.

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
        f = Function(inverse)
        return f.__mul__(func_or_num)


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
