Title: Conditional decorators in Python
Date: 2018-10-25 15:30
Modified: 2018-10-25 15:30
Category: Python
Tags: python, decorators, functions, code snippet
Slug: conditional_decorators
Authors: Sam Zuckerman
Summary: The issue of conditional decorators came up recently.  Here's a code snippet.  


The issue of conditional decorators came up recently.  It was brought up in [reference to pytest on Twitter](https://twitter.com/samzuckerman/status/1055246076297560065). The following's a quick snippet to make the point.

# Basic Code

```python

def do_nothing_decorator(func):
    return func
 
def print_hi_decorator(func):
    def wrapper(*args, **kwargs):
        print("Hi!")
        return func(*args, **kwargs)
    return wrapper
 
num_check = 5
 
conditional_decorator = print_hi_decorator if num_check > 4 else do_nothing_decorator

@conditional_decorator
def my_function(x):
    return x+2
```

Now this example doesn't do much, it merely prints "Hi!" when the function is called.

The main idea is that there's some sort of check, in this case `num_check` that either applies the decorator and, if not, applies a `do_nothing_decorator`.


### Output

```python
>>> my_function(3)
Hi!
5
>>> my_function(4)
Hi!
6
```

# Changing the Parameters

If we run the following to fail the `if` portion, we can see the expected output below. Don't forget that the `conditional_decorator` needs to be run with `my_function` again to 'reinitialize'.
```python
num_check = 3
 
conditional_decorator = print_hi_decorator if num_check > 4 else do_nothing_decorator
 
@conditional_decorator
def my_function(x):
    return x+2
```
### Output
```python
>>> my_function(3)
5
>>> my_function(4)
6
```
