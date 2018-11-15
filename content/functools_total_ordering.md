Title: What's this in functools? total_ordering
Date: 2018-11-15 07:00
Modified: 2018-11-15 07:00
Category: Python
Tags: python, functools, functions, code snippet
Slug: functools_total_ordering
Authors: Sam Zuckerman
Summary: There's a lot of cool stuff in the functools module. Some small additions to your functions will greatly increase your productivity and your code quality. `total_ordering` is an easy way to implement comparison methods in a class without duplicating your code.

# Why do I need total_ordering?

If you have a class and you need to compare objects to eachother, `total_ordering` will help save you from code duplication. If you supply an object with an `__eq__` method and one of the other comparison methods, `__le__`, `__lt__`, `__ge__`, or `__gt__`, the remaining comparison methods will be "magically" supplied as well.

# Example

Using the example from the [`functools` documentation](https://docs.python.org/3/library/functools.html#functools.total_ordering), let's see what happens if we don't use `total_ordering`: 

```python
class Student:
    def _is_valid_operand(self, other):
        return (hasattr(other, "lastname") and
                hasattr(other, "firstname"))
    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.lastname.lower(), self.firstname.lower()) ==
                (other.lastname.lower(), other.firstname.lower()))
    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.lastname.lower(), self.firstname.lower()) <
                (other.lastname.lower(), other.firstname.lower()))

sam = Student()
sam.firstname = 'Sam'
sam.lastname = 'Zuckerman'

john = Student()
john.firstname = 'John'
john.lastname = 'Smith'
```

The above class has only implemented equality and less-than methods.

```python
sam == john
 
>>> False
```

```python
sam < john
 
>>> False
```

Now, if I use any other comparison methods:

```python
sam <= john

>>> TypeError: '<=' not supported between instances of 'Student' and 'Student'
```

# Using the total_ordering decorator

If I decorate the above class with the `total_ordering` decorator, I won't throw a `TypeError` as above.

```python
from functools import total_ordering

@total_ordering
class Student:
    def _is_valid_operand(self, other):
        return (hasattr(other, "lastname") and
                hasattr(other, "firstname"))
    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.lastname.lower(), self.firstname.lower()) ==
                (other.lastname.lower(), other.firstname.lower()))
    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.lastname.lower(), self.firstname.lower()) <
                (other.lastname.lower(), other.firstname.lower()))
                
sam = Student()
sam.firstname = 'Sam'
sam.lastname = 'Zuckerman'

john = Student()
john.firstname = 'John'
john.lastname = 'Smith'

sam <= john
 
>>> False
```

To implement the `__le__` method I would have needed to copy and paste five lines of code and change one character. To implement all the methods, I would need about 15 additional lines of code. It's quite a waste of space which is saved by a simple decorator. In addition, it saves minor errors and typos that could come from manually needing to change small items in very similar looking methods.

# Performance

In the [`functools` documentation](https://docs.python.org/3/library/functools.html#functools.total_ordering) it mentions that if performance is a consideration for your application, you might want to just implement all the methods instead of using this decorator.

> __Note:__ While this decorator makes it easy to create well behaved totally ordered types, it does come at the cost of slower execution and more complex stack traces for the derived comparison methods. If performance benchmarking indicates this is a bottleneck for a given application, implementing all six rich comparison methods instead is likely to provide an easy speed boost.

# Conclusion

The `total_ordering` decorator is an easy way to save on code duplication when writing classes that utilize comparison metrics. By writing an `__eq__` method and another comparison method, all the work is done for you.