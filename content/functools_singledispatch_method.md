Title: What's this in functools? singledispatchmethod
Date: 2019-11-21 15:30
Modified: 2019-11-21 15:30
Category: Python
Tags: python, functools, functions, code snippet
Slug: functools_singledispatchmethod
Authors: Sam Zuckerman
Summary: There's a lot of cool stuff in the functools module. Some small additions to your functions will greatly increase your productivity and your code quality. `singledispatchmethod` is an easy way to apply overload methods based on an input argument's type.

# Why do I need singledispatchmethod?

As mentioned in [a previous post about `singledispatch`]({filename}/functools_singledispatch.md), other programming languages have native method or function overloading. For example, in Java one can make a class with methods that run different code depending on the datatype of the input.

With `singledispatch` one can run a different function when running `my_func(<int>)` vs `my_func(<str>)`.

That's the main idea; see [the other post about `singledispatch`]({filename}/functools_singledispatch.md) for more examples.

Regarding `singledispatchmethod`, it's the same idea as `singledispatch` except to be used as a class method decorator rather than a function decorator.

**Note**: `singledispatchmethod` was added in Python 3.8. It makes sense that `singledispatch` was difficult to implement as a method decorator prior to Python 3.8 in that `singledispatch` works on the first element of a function, and the first element of a method refers to `self` or the instance of the object (i.e. not the first method argument). There are some workarounds, but they're quite ugly[^1] and it would be recommended to merely upgrade to Python 3.8.

[^1]: See [the answer to this stackoverflow question](https://stackoverflow.com/questions/24063788/python3-singledispatch-in-class-how-to-dispatch-self-type).

# Example without singledispatchmethod

Building upon the example from the [the other post about `singledispatch`]({filename}/functools_singledispatch.md), we are now creating a class to print currency values.

```python
class Currency:
    
    def __init__(self, units, revenue):
        self.units = units
        self.revenue = revenue
    
    def print_currency(self, val):
        if isinstance(val, float):
            return '$' + str(val)
        else:
            return str(val)


units = 10
revenue = 100.0
amount = Currency(units, revenue)
output = f'We sold {amount.print_currency(amount.units)} units for {amount.print_currency(amount.revenue)}.'
print(output)

>>> 'We sold 10 units for $100.0.'
```

# Example with singledispatchmethod
 
```python

from functools import singledispatchmethod
class Currency:
    
    def __init__(self, units, revenue):
        self.units = units
        self.revenue = revenue
    
    @singledispatchmethod
    def print_currency(self, val):
        raise NotImplementedError("Incorrect type for print_currency")
    
    @print_currency.register
    def _(self, val:float):
        return '$' + str(val)
    
    @print_currency.register
    def _(self, val:int):
        return str(val)
        

units = 10
revenue = 100.0
amount = Currency(units, revenue)
output = f'We sold {amount.print_currency(amount.units)} units for {amount.print_currency(amount.revenue)}.'
print(output)


>>> 'We sold 10 units for $100.0.'
```


I feel that even though the example with `singledispatchmethod` adds many more lines to the code, it's much more readable and makes more sense quicker than the first example. Without using `singledispatchmethod` I need to look through a group of nested if/else statements and understand what is trying to be done. `singledispatchmethod` is specifically used to dispatch to different types, so the reasoning is clear.

# Conclusion

By using `singledispatchmethod` in your code you can make your code more readable and modular if you require a concept similar to function overloading within class definitions.