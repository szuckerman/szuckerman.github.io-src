Title: What's this in functools? partial and partialmethod
Date: 2018-12-13 15:30
Modified: 2018-12-13 15:30
Category: Python
Tags: python, functools, functions, code snippet
Slug: functools_partial_and_partialmethod
Authors: Sam Zuckerman
Summary: There's a lot of cool stuff in the functools module. Some small additions to your functions will greatly increase your productivity and your code quality. The `partial` and `partialmethod` functions are easy ways to create new functions when you need to "freeze" an argument from an existing one.

# Why do I need functools.partial?

According to [Clean Code](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882) by Bob Martin, functions should "do one thing", but sometimes we try to pack so many arguments in a function to generalize it, that the "one thing" aspect gets muddled or lost. 

`functools.partial` helps by making functions from other functions but give default values for certain attributes. `functools.partialmethod` is the same idea, but within a `class`. Examples should make this idea more concrete.


# Example 1

A simple example ([taken from Raymond Hettinger](https://twitter.com/raymondh/status/1072592988268834816)) is to create a custom function for a certain base when using the `pow` function.

The following are equivalent:

```python
2**3
>>> 8

pow(2,3)
>>> 8
```

If for some reason I would be using `pow(2, x)` a lot, it might make sense to make a new function:

```python
from functools import partial
power_of_2 = partial(pow, 2)

power_of_2(3)
>>> 8
```

The way this works is `partial` takes a function for the first argument then takes the values for the arguments you want to freeze, left to right. It also takes keyward arguments, but we'll discuss that in the next section whether that's a good idea.

# Freezing other arguments

If you want to freeze other arguments rather than the left one first, you have a few options.

## Using Keyword Arguments

Here's a toy function that gets an employee's job level based on their position and location.

```python

def get_employee_job_level(position=None, location=None):
    level = position[0]
    if location == 'CA':
        return ord(level)
    else:
        return ord(level)//2
    
get_employee_job_level('CEO', 'CA')
>>> 67
```

If we were only interested in employees from California, we could use `partial` to create a new function, like so:


```python
from functools import partial
  
get_CA_employee_job_level = partial(get_employee_job_level,  location='CA')

get_CA_employee_job_level('CEO')
>>> 67
```

The above isn't recommended, however, as discussed in the aforementioned [tweet by Raymond Hettinger](https://twitter.com/raymondh/status/1072592988268834816).

For example, this won't work if we want to use keyword arguments to make a `square` function:

```python
from functools import partial
square = partial(pow, y=2)

square(3)
>>> TypeError: pow() takes no keyword arguments
```

## Using a lambda instead of keyword arguments

If one needs to freeze other arguments in a function, it's recommended to use a `lambda`:

```python
square = lambda x: pow(x, 2)

square(3)
>>> 9
```

# Most useful case for partial

The above examples for `partial` are nice, in terms of writing more clean and verbose code, but it just appears as something that's "nice" and not 100% necessary.

I think the most important use case is using it as a key for other functions, since these keys only allow one-argument functions to be passed.

For example:

```python

def sort_func(x, y):
    if x == 'forward':
        return ord(y)
    else:
        return -ord(y)
        
backward_sort = partial(sort_func, 'backward')

letters = ['A', 'B', 'C', 'D', 'E']

sorted(letters, key=backward_sort)
>>> ['E', 'D', 'C', 'B', 'A']
```

## Using in a Pandas DataFrame

This is especially useful in the Pandas `apply` function for columns. If you have a function with important business logic, but has more than one argument, you can cut it down using `partial` and pass it to the `apply` function. 

# Using partialmethod

`partialmethod` works in a similar fashion to `partial`, but is used within a `class`.

Take the following `class` for example, which implements similar functionality to the functions we've made above.

```python
from functools import partialmethod

class Compute:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.power = self.my_pow(self.x, self.y)
    
    def my_pow(self, x, y):
        return x ** y
    
    def __repr__(self):
        return '<Compute {x},{y}>'.format(x=self.x, y=self.y)
        
    power_of_2 = partialmethod(my_pow, 2)
        
        
num=Compute(2,3)
num
>>> <Compute 2,3>
num.power
>>> 8
num.power_of_2(2)
>>> 4
```

Basically we want to add another method for the `class` that's based on a previous method.

# Why not just use partial in the class?

If you run the above code, with `partial` instead of `partialmethod` you'll get an error. The reason is since, as we mentioned above, `partial` freezes arguments from left to right. The first argument of a method is `self` which, you can imagine, will make for many problems if you try to freeze that with something other than the object instance.

# Summary

The `partial` and `partialmethod` functions are easy ways to create new functions when you need to "freeze" an argument from an existing one. The there are various applications, with the most useful being, in my experience, when you need to pass a one-argument function as an argument to another function, like Pandas' `apply` or a `key` parameter. 