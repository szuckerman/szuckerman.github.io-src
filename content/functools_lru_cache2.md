Title: Additional points on lru_cache
Date: 2018-11-09 15:30
Modified: 2018-11-09 15:30
Category: Python
Tags: python, functools, functions, code snippet
Slug: functools_lru_cache2
Authors: Sam Zuckerman
Summary: Here's a few additional points for using the `lru_cache` module.

In our previous post _[What's this in functools? lru_cache]({filename}/functools_lru_cache.md)_, we saw how we can use `lru_cache` effectively to speed up execution time of a function that grows exponentially.

Here's three more points to be aware of when using `lru_cache`.

# The function arguments must be hashable

Since the results are cached using a dictionary, the function arguments must be hashable. This is because the keys of a dictionary must be hashable.

Basically, hashable means that there is a lookup value (i.e. "hash") associated with the object. If something is immutable, and thus can't change, the item can be hashed.

Lists and other mutable objects that can be changed don't have a hash value. More specifically, they don't implement the \_\_hash\_\_ method, but one could be added in a custom class [as in this stackoverflow answer](https://stackoverflow.com/a/42203997).

Therefore, __the arguments to the functions you're decorating with `lru_cache` should only accept hashable objects__.

I.e: __Don't use lists or dictionaries as function arguments for functions you decorate with `lru_cache`__.

# Watch out for differing argument patterns

Different argument patterns might get cached differently. For example: `f(a=1, b=2)` might get cached differently from `f(b=2, a=1)`.

Ok, so, that's easy enough. Just always use the correct order, right?

Well, I sometimes like to do argument unpacking with my parameters using a `dict`.

So, instead of `f(a=1, b=2)`, I might run:

```python
my_params = {'a': 1, 'b': 2}

f(**my_params)
```

The problem here is that, depending on what version of Python3 you're using, dictionaries aren't necessarily ordered. If you're using Python 3.7, though, [you should be fine](https://stackoverflow.com/a/39980744).

If you're using a version that doesn't order they keys, then the function could be called sometimes as `f(a=1, b=2)` and sometimes `f(b=2, a=1)` depending on what gets unpacked first. In these cases you should look into using an `OrderedDict` found in the `collections` module.  

# Clearing the cache

You can clear out the cache with the `cache_clear()` method. 