Title: What's this in functools? reduce
Date: 2019-01-11 15:30
Modified: 2019-01-11 15:30
Category: Python
Tags: python, functools, functions, code snippet
Slug: functools_reduce
Authors: Sam Zuckerman
Summary: There's a lot of cool stuff in the functools module. Some small additions to your functions will greatly increase your productivity and your code quality. `reduce` is an easy way "reduce" an array of elements to a single value.

# Why do I need reduce?

Honestly, you don't really. `reduce` was a built-in in Python 2 and was demoted to `functools` in Python 3. 

Most of the examples from `reduce` can be done in an easier fashion using other built-ins.

# What does reduce do?

`reduce` works the same way as most "reduce" functions in Computer Science. It "reduces" an array of numbers to one number, adding the first number to the second, and adding subsequent numbers to each intermittent total.

# Example 1: Implementing a "sum" function using reduce

```python
from functools import reduce
import operator as o

my_list = [1,2,3,4,5]

reduce(o.add, my_list)

>>> 15
```  

The above example works the same way as running `sum(my_list)`. 

What the above example is doing:

1. `o.add` is a functional approach to algebra; `o.add(1,2)` is the same as `1 + 2`.
2. `o.add` takes two arguments, `reduce` adds the next value to the current subtotal.

It works the same way as:

```python
total = 1
next_numbers = [2, 3, 4, 5]

for next_number in next_numbers:
    total = total + next_number
```

Basically, there's always a function with two parameters used, with one of the parameters being the next value and the other being the intermediate total value.


# Example 2: Implementing a "factorial" function using reduce


```python
from functools import reduce
import operator as o

my_list = [1,2,3,4,5]

reduce(o.mul, my_list)

>>> 120
```

As you can see, it's similar to the loop we mentioned before, except that the addition operator is replaced with a multiplication operator:

```python
total = 1
next_numbers = [2, 3, 4, 5]

for next_number in next_numbers:
    total = total * next_number
```

# Which is faster? reduce or the loops?

```python
import timeit
from functools import reduce
import operator as o

def factorial(values):
    total = values[0]
    next_numbers = values[1:]
    
    for next_number in next_numbers:
        total = total * next_number
    
    return total


timeit.timeit('factorial([1,2,3,4,5])', setup="from __main__ import factorial", number=1000)
>>> 0.0005066430021543056

timeit.timeit('reduce(o.mul, [1,2,3,4,5])', setup="from functools import reduce\nimport operator as o", number=1000)
>>> 0.000527281008544378
```

From the above, it appears that our own `factorial` implementation has similar performance to using `reduce`.

# Conclusion

There are many situations where it's useful to `reduce` numbers to a single value, however the implementation for those situations might be better suited for other functions than `reduce` from `functools.

Understanding how `reduce` works, by using an intermittent sum, is useful since this topic comes up often in Computer Science, and is actually how Apache Spark aggregates data. 

As we saw above, the time difference for a user defined function or a similar version with `reduce` yield similar results. In this case one should obviously opt for whatever appears to be more clean/verbose/understandable code.  