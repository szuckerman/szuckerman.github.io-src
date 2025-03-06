Title: What's this in itertools? count
Date: 2024-07-06 10:30
Modified: 2024-07-06 10:30
Category: Python
Tags: python, itertools, iteration, code snippet
Slug: itertools_count
Authors: Sam Zuckerman
Summary: Python's itertools module provides powerful tools for efficient looping. The `count` function from itertools offers a clean way to create infinite iterators, useful for generating sequences effortlessly.

# Why do I need itertools.count?

Sometimes you need an endless stream of numbers or an infinite iterator. Writing loops or generator functions for such simple tasks can become cumbersome or unclear. Thankfully, Python's built-in `itertools` module provides a neat and readable solution with `count`.

Let's see an example.

# Example without itertools.count

A common example is when you need continuous incremental indices. Without `count`, you might write something like this:

```python
def index_generator(start=0, step=1):
    n = start
    while True:
        yield n
        n += step

counter = index_generator(5, 2)

for _ in range(5):
    print(next(counter))
```
**Output:**
```
5
7
9
11
13
```

This works, but Python gives us a better built-in way.

# Example with itertools.count

`itertools.count` makes this significantly simpler and cleaner.

```python
from itertools import count

counter = count(start=5, step=2)

for _ in range(5):
    print(next(counter))
```

**Output:**
```
5
7
9
11
13
```

# Practical use-case

`count` is also very handy when pairing with other tools like `zip()` to effortlessly create indexed lists:

```python
from itertools import count

fruits = ['apple', 'banana', 'orange']
indexed_fruits = list(zip(count(1), fruits))

print(indexed_fruits)
```
**Output:**
```
[(1, 'apple'), (2, 'banana'), (3, 'orange')]
```

Compared to manually managing counters, this approach is concise, readable, and reliable.

# Conclusion

While creating a manual counter is straightforward, using `itertools.count` makes your code more expressive and reduces potential bugs or inconsistencies in managing loop indices or incremental counts. As a general rule, whenever you find yourself creating a custom incremental generator or manually incrementing a variable repeatedly, consider using `count` from itertools instead.
