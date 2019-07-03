Title: What's this in functools? singledispatch
Date: 2019-07-03 15:30
Modified: 2019-07-03 15:30
Category: Python
Tags: python, functools, functions, code snippet
Slug: functools_singledispatch
Authors: Sam Zuckerman
Summary: There's a lot of cool stuff in the functools module. Some small additions to your functions will greatly increase your productivity and your code quality. `singledispatch` is an easy way to apply 

# Why do I need singledispatch?

Other programming languages have native method or function overloading. For example, in Java one can make a class with methods that run different code depending on the datatype of the input.

With `singledispatch` one can run a different function when running `my_func(<int>)` vs `my_func(<str>)`.

The following example should help explain.

**Note**: `singledispatch` was only added in Python 3.4. Another reason to migrate!

# Example without singledispatch

One common example I run into where data types matter is number formatting. Usually product unit sales are represented as integers and with revenue as a float.   

If I want to print currency figures on only the float values I would need to do something like this:

```python
def print_currency(val):
    if isinstance(val, float):
        return '$' + str(val)
    else:
        return str(val)

units = 10
revenue = 100.0
output = f'We sold {print_currency(units)} units for {print_currency(revenue)}.'

>>> 'We sold 10 units for $100.0.'
```

# Example with singledispatch

**Note**: The "dispatch" only happens [on the first argument](https://docs.python.org/3.7/library/functools.html) (hence, "single" dispatch, applying to more arguments would be "multiple" dispatch [*Fluent Python* by Luciano Ramalho]), 
 
```python

from functools import singledispatch

@singledispatch
def print_currency(arg):
    pass
    
    
@print_currency.register(float)
def _(val):
    return '$' + str(val)
    
    
@print_currency.register(int)
def _(val):
    return str(val)

units = 10
revenue = 100.0
output = f'We sold {print_currency(units)} units for {print_currency(revenue)}.'

>>> 'We sold 10 units for $100.0.'
```

# Newer example

In Python 3.7 `singledispatch` was updated to allow for type annotations in function arguments. Therefore you don't need to use a "type" in the `register` function. 

```python

from functools import singledispatch

@singledispatch
def print_currency(arg):
    pass
    

@print_currency.register
def _(val:: float):
    return '$' + str(val)
    
    
@print_currency.register
def _(val:: int):
    return str(val)

units = 10
revenue = 100.0
output = f'We sold {print_currency(units)} units for {print_currency(revenue)}.'

>>> 'We sold 10 units for $100.0.'
```

# Conclusion

While the above examples don't seem so necessary, since the original if/else may be sufficient, I feel the code looks a lot more clear when having different functions for different types as opposed to many chains of if/else which can easily get unweildy. I think Ramalho puts it well in *Fluent Python*:

> @singledispatch is not designed to bring Java-style method overloading to Python. A single class with many overloaded variations of a method is better than a single function with a lengthy stretch of if/elif/elif/elif blocks. But both solutions are flawed because they concentrate too much responsibility in a single code unit the class or the function. The advantage of @singledispath is supporting modular extension: each module can register a specialized function for each type it supports.  *Ramalho, Luciano. Fluent Python: Clear, Concise, and Effective Programming (p. 211)*

By using `singledispatch` in your code you can make your code more readable and modular if you require a concept similar to function overloading.