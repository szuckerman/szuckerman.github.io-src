Title: What's this in functools? wraps and update_wrapper
Date: 2018-12-06 15:30
Modified: 2018-12-06 15:30
Category: Python
Tags: python, functools, functions, code snippet
Slug: functools_wraps_and_update_wrapper
Authors: Sam Zuckerman
Summary: There's a lot of cool stuff in the functools module. Some small additions to your functions will greatly increase your productivity and your code quality. The `wraps` decorator is an easy way to retain attributes for a wrapped function instead of inheriting from the wrapper function definition.

# Why do I need functools.wraps?

Decorators are a useful part of Python. They allow one to adjust functions in a similar, predictable manner and can be especially powerful due to their concise expressiveness when utilized by certain frameworks, especially web frameworks like Flask.

That being said, one issue with decorators is that they copy the attributes of the functions they wrap. An example will make this more clear.

# Example without functools.wraps
The following is [taken from the Python3 `functools` documentation](https://docs.python.org/3/library/functools.html#functools.wraps), but has the `@wraps(f)` section removed.

```python
def my_decorator(f):
    def wrapper(*args, **kwds):
        print('Calling decorated function')
        return f(*args, **kwds)
    return wrapper

@my_decorator
def example():
    """Docstring"""
    print('Called example function')

example()
>>> Calling decorated function
>>> Called example function
```

As you can see, the above works as expected. However, if we inspect some of the attributes from the function, we see that some attributes have been overwritten.

```python 
example.__name__
>>> 'wrapper'

example.__doc__
>>> 
```

The function has lost its name of 'example' and has been replaced by `wrapper`. Similarly, the non-existent docstring from `wrapper` has overwritten the docstring in `example`.

# Example with functools.wraps

Now let's run the same code above, use the `wraps` decorator:

```python
from functools import wraps

def my_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        print('Calling decorated function')
        return f(*args, **kwds)
    return wrapper

@my_decorator
def example():
    """Docstring"""
    print('Called example function')

example()
>>> Calling decorated function
>>> Called example function
```

The attributes we inspected above now return what would be expected for the `example` function.

```python 
example.__name__
>>> 'example'

example.__doc__
>>> 'Docstring'
```

The following are the attributes that are 'retained' (more correctly, 'copied over' to `wrapper`, but this makes more sense colloquially):

```python
functools.WRAPPER_ASSIGNMENTS
>>> ('__module__', '__name__', '__qualname__', '__doc__', '__annotations__')
```

# Why does this matter?

The above situation might not seem like a big deal, and in most cases it probably isn't. However, I'm sure people can think of situations where a program's logic could depend on what's available in the `__name__` attribute. If various functions are wrapped with the same decorator, they would all get the name of the internal wrapper function, which would definitely not be desired if logic is based on `__name__`.

# Access to the original function

Another nice aspect of `wraps` is that it adds a `__wrapped__()` attribute to the wrapped function that allows access to the original function if introspection is necessary. The `example` function that is called is technically calling `wrapper` (which also happens to call `example` in its definition). If we wanted to work with `example` like it was never wrapped, we would work with `example.__wrapped__()`.

# Now what about functools.update_wrapper?

`update_wrapper` is what actually performs the work, but `wraps` is cleaner to invoke as a wrapper. They're equivalent in that `wraps` is merely a `partial` function of `update_wrapper` that has its parameters frozen. Long story short, you should be fine just using `wraps`, but should be aware of `update_wrapper` in case you need more control over the wrapped function.

# Summary

The `wraps` decorator is an easy way to retain attributes for a wrapped function instead of inheriting from the wrapper function definition. By using this decorator you can ensure reliability and consistency of your function attributes. 
