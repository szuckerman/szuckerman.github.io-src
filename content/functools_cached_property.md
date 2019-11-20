Title: What's this in functools? cached_property
Date: 2019-11-20 15:30
Modified: 2019-11-20 15:30
Category: Python
Tags: python, functools, functions, code snippet
Slug: functools_cached_property
Authors: Sam Zuckerman
Summary: There's a lot of cool stuff in the functools module. Some small additions to your functions will greatly increase your productivity and your code quality. `cached_property` is an easy way to add caching to methods in a Python object originally decorated with the `property` decorator. 

# Why do I need cached_property?

A big addition to Python classes was the inclusion of the `property` decorator for class methods.[^1] What's great about the `property` decorator is that it allows a method to be called as an instance variable, essentially allowing a new calculated variable to be used that has some underlying calculation being performed under the hood. Even though this is really good for writing clean, concise code, if there's a long-running function behind the variable, such as a database query, then it can take some time to return what appears to be a small variable. `cached_property` ensures that once the function is run once, the results are cached and can be resused quickly later.

[^1]: Raymond Hettinger in [this Python talk](https://www.youtube.com/watch?v=HTLu2DFOdTg).

**Note**: `cached_property` is new in functools for 3.8! You can't use this in previous versions unless you install the [cached-property](https://pypi.org/project/cached-property/) package.

# Examples

The following example is taken from the [`functools` documentation for `cached_propery`](https://docs.python.org/3/library/functools.html#functools.cached_property).

## Using property

```python
import statistics

class DataSet:
    def __init__(self, sequence_of_numbers):
        self._data = sequence_of_numbers
    
    @property
    def stdev(self):
        return statistics.stdev(self._data)
        
    @property
    def variance(self):
        return statistics.variance(self._data)
```

```
>>> data = DataSet(range(20))
>>> data.stdev
5.916079783099616
>>> data.variance
35.0
```

## Using cached_property
```python
from functools import cached_property
import statistics

class DataSet:
    def __init__(self, sequence_of_numbers):
        self._data = sequence_of_numbers
    
    @cached_property
    def stdev(self):
        return statistics.stdev(self._data)
    
    @cached_property
    def variance(self):
        return statistics.variance(self._data)
```

```
>>> data = DataSet(range(20))
>>> data.stdev
5.916079783099616
>>> data.variance
35.0
```

Ok, they return the same information. What's the big deal? The above example is trivial, but if there was a long running process to caculate variance or standard deviation you wouldn't want to wait a few seconds just to return `data.stdev` or `data.variance`.

# Pitfalls of cached_property

## Defining __slots__
Since `cached_property` "requires that the `__dict__` attribute on each instance be a mutable mapping"[^2] (i.e. there's a `__dict__` attribute for the instance) `cached_property` won't work in some cases. 

[^2]: https://docs.python.org/3/library/functools.html#functools.cached_property

For example, if one defines `__slots__` in an object then there's no `__dict__` attribute and you'll raise a `ValueError`.

```python
class DataSet:
    __slots__ = ['stdev']
    
    def __init__(self, sequence_of_numbers):
        self._data = sequence_of_numbers
    
    @cached_property
    def stdev(self):
        return statistics.stdev(self._data)
    
    @cached_property
    def variance(self):
        return statistics.variance(self._data)
```

```python
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: 'stdev' in __slots__ conflicts with class variable
```

As you can see, this code won't even be executed due to the `ValueError`. This exception isn't special for `cached_property` though; the same error is raised if one merely uses a `property` decorator as well.

## Changing the Data

If I go back to using just the `property` decorator like so:

```python

class DataSet:
    def __init__(self, sequence_of_numbers):
        self._data = sequence_of_numbers
    
    @property
    def stdev(self):
        return statistics.stdev(self._data)
    
    @property
    def variance(self):
        return statistics.variance(self._data)
```

```python
>>> data = DataSet(range(20))
>>> data.stdev
5.916079783099616
>>> data.variance
35.0
```

If I decide to change the data, the other variables update accordingly.

```python
>>> data._data = range(30)
>>> data.stdev
8.803408430829505
>>> data.variance
77.5
```

Comparing this to the `cached_property` version:

```python
class DataSet:
    
    def __init__(self, sequence_of_numbers):
        self._data = sequence_of_numbers
    @cached_property
    
    def stdev(self):
        return statistics.stdev(self._data)
    
    @cached_property
    def variance(self):
        return statistics.variance(self._data)
```

```python
>>> data = DataSet(range(20))
>>> data.stdev
5.916079783099616
>>> data.variance
35.0
```

```python
>>> data._data = range(30)
>>> data.stdev
5.916079783099616
>>> data.variance
35.0
```

`data.stddev` and `data.variance` didn't update because they're cached! What do we do now if the underlying data changes? The solution is to invalidate the cache.

As you can see, from `data__dict__`, the cached data is in a dictionary. However, it only gets there once the `data.stdev` property method is run. Now, it looks like this:

```python
>>> data.__dict__
{'_data': range(0, 30), 'stdev': 5.916079783099616, 'variance': 35.0}
```

But before running `data.stdev` and `data.variance` it looks like this:

```python
>>> data = DataSet(range(20))
>>> data.__dict__
{'_data': range(0, 20)}
```

Therefore to invalidate (i.e. "fix") the cache, you merely need to delete the values from the dictionary.

```python
>>> data.stdev
5.916079783099616
>>> data.variance
35.0
>>> data.__dict__
{'_data': range(0, 20), 'stdev': 5.916079783099616, 'variance': 35.0}
>>> data._data = range(30)
>>> data.__dict__
{'_data': range(0, 30), 'stdev': 5.916079783099616, 'variance': 35.0}
>>> del data.__dict__['stdev']
>>> data.__dict__
{'_data': range(0, 30), 'variance': 35.0}
>>> data.stdev
8.803408430829505
>>> del data.__dict__['variance']
>>> data.__dict__
{'_data': range(0, 30), 'stdev': 8.803408430829505}
>>> data.variance
77.5
>>> data.__dict__
{'_data': range(0, 30), 'stdev': 8.803408430829505, 'variance': 77.5}
```

After deleting the values from `data.__dict__` we were able to regenerate the correct values.

# Conclusion

`property` is a very useful decorator for Python objects. `cached_property` is useful as well, but one should understand the tradeoffs when using this decorator. It might save some time on the backend, but could introduce some bugs due to caching. 