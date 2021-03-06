# Basic manipulation of mathematical functions, version 1.0.0
This module provides mathematical like syntax for working with mathematical functions. Sounds obvious right? However as of this writing it is fairly complex and time consuming to work with mathematical functions in Python. Things quickly become unreadable and don't look at all like the math we're used to. For example, say you want to evaluate the following function and its derivative at the points 3, 5 and 6: <br/>
f(x) = sin(log(x))\*exp(arccos(x^2)) <br/>
How would you go about this? Well with this module its easy and also looks surprisingly mathlike:
```python
from functions import *
f = sin(log(x))*exp(arccos(x**2))
fd = f.derivative()
f(3), fd(3)
f(5), fd(5)
f.eval(6), fd.eval(6)
```
The first two evaluations show how you can evaluate each function just like you would in normal mathematics and the last evaluation show how you can be more explicit in your evaluations.

## Documentation
The functions module provides easy manipulation of mathematical functions.

It does this by providing a macro that creates new mathematical functions by conjugating past functions with the common operators.

All functions can be evaluated, derivated, integrated and plotted as well as modified. The module can even calculate generalized integrals. It provides the user with all elementary functions that can then be used to construct more complex functions of interest. Furthermore the user can define his/her own function objects that can be used in compliance with the other functions.

### Example
Evaluate the generalized integral of 1/(sqrt(x)) from 0 to 100.
```python
from functions import *
f = 1/(sqrt(x))
f.integrate(0,100) # --> 20.00009
```
### *class* functions.**Function**(function: f)

Here f is a pure function defined as usual by **def** that takes one number as input and outputs another number (or NaN if undefined in a point) according to some rule.

The Function class is the base of all mathematical functions. All instances can be conjugated with numbers and/or other Function instances by the common operators +, -, \*, / and \*\* to produce new instances of the Function class.

Every instance of this class is also considered to be callable and f(2) for some instance f of Function would produce the same result as f.eval(2) (see the eval method documentation below). Also f(g) would evaluate as f(g(x)) for each value x and for all Function instances f and g.

Furthermore each Function instance, f, returns a new Function instance that evaluates as abs(f.eval) or |f(x)| when acted on by the "abs" builtin function.

#### *method* **eval**(Number: x)
Return the evaluation of this function instance at the point x (where x is a real number).

#### *method* **derivative**(*dx*=0.0001)
Return a new instance of the class Function that evaluates to the derivative of this function in each point (an optional argument for the step size in the calculation of the derivative is provided but defaults to 0.0001).

#### *method* **integrate**(Number: start, Number: end, *tol*=1e-5, *MAX*=1e10)
Return the evaluation of the definite integral from start to end of this function with a tolerance of tol in the error (defaults to 1e-5) if the integral exists, otherwise return NaN. For possible divergent integrals the MAX input value is provided (defaults to 1e10), if the algorithm determines the integral to be greater than MAX it views this integral as a divergent one and returns NaN.

#### *method* **plot**(Number: start, Number: end, *step*=0.01)
Start a new process that shows the plot of the function from start to end with the step size of step (defaults to 0.01). This does not in any way disrupt the flow of the program, instead it starts a new process that runs independently of the program it is started from.

### *function* functions.**norm**(Function: func, *norm_type*="L2", *tol*=1e-5)
Return the norm of the provided Function instance if such a norm exists, otherwise return NaN. The norm_type argument refers to a norm type. Supported norm types include: "L1", "L2", "L3", ..., "Lp" for all integers p. These being the standard norms in L_p spaces. This argument defaults to the "L2" norm. The tol argument is the accepted tolerance of the evaltuation (defaults to 1e-5). <br/>
For information about norm types see: https://en.wikipedia.org/wiki/Lp_space#Lp_spaces

### Exported constants
The following constants are exported for working with the elementary functions.

#### functions.**exp**
A Function instance relating to the exponential function.

#### functions.**sin**
A Function instance relating to the sine function.

#### functions.**arcsin**
A Function instance relating to the inverse sine function.

#### functions.**cos**
A Function instance relating to the cosine function.

#### functions.**arccos**
A Function instance relating to the inverse cosine function.

#### functions.**tan**
A Function instance relating to the tan function.

#### functions.**arctan**
A Function instance relating to the inverse tan function.

#### functions.**log**
A Function instance relating to the logarithmic function.

#### functions.**x**
A Function instance relating to the identity function (can also be used for clarity as the variable x, see examples above).

#### functions.**sqrt**
A Function instance relating to the square root of x function.

## Compatibility Policy

* The API of this module is frozen.
* Version numbers adhere to semantic versioning.

The only accepted reason to modify the API of this module
is to handle issues that cannot be resolved in any other
reasonable way.
