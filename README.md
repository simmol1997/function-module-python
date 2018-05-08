# Basic manipulation of mathematical functions
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
f.integral(0,100)
```
### *class* functions.**Function**(function: f)
Here f is a pure function defined as usual by **def** that takes one number as input and outputs another number (or NaN if undefined in a point) according to some rule.

The Function class is the base of all mathematical functions. All instances can be conjugated with numbers and or other Function instances by the common operators +, -, \*, / and \*\* to produce new instances of the Function class. Every instance of this class is also considered to be callable and f(2) for some instance f of Function would produce the same result as f.eval(2) (see the eval method documentation below).

#### *method* **eval**(Number: x)
Return the evaluation of this function instance is the point x.

#### *method* **derivative**(*dx*=0.0001)
Return a new instance of the class Function that evaluates to the derivative of this function in each point (an optional argument for the step size in the calculation of the derivative is provided).

#### *method* **integral**(Number: start, Number: end, *init_step*=0.0001)
Return the evaluation of the definite integral from start to end of this function (the optional argument is provided as a means to provide more correct results at a loss of time).

#### *method* **plot**(Number: start, Number: end, *step*=0.01)
Start a new process that shows the plot of the function from start to end with the step size of step (defaults to 0.01). This does not in any way disrupt the flow of the program, instead it starts a new process that runs independently of the program it is started from.

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
