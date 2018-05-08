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
f.integral(0,100) # --> 1.98
```
### class Function
