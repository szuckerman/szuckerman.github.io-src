Title: What's this in itertools? batched
Date: 2024-03-05 14:30
Modified: 2024-03-05 14:30
Category: Python
Tags: python, itertools, functions, code snippet
Slug: itertools_batched
Authors: Sam Zuckerman
Summary: The itertools module offers a lot of useful tools for iterators. One such function, batched, makes it easy to divide large datasets or iterables into smaller, more manageable chunks for efficient processing.

# Why do I need batched?

Sometimes, you have large datasets or iterables that you want to process in smaller chunks rather than as a single long
sequence. Instead of manually slicing or grouping elements, the `batched` function lets you quickly split an iterable
into batches of a specified size. This is especially useful for tasks like data processing, batch processing, or when
interacting with APIs that require paginated responses.

# What does batched do?

The `batched` function takes two main arguments:

- `iterable`: The sequence of elements you want to chunk.
- `n`: The size of each batch (i.e., how many items you want per batch).

The function returns an iterator that yields tuples containing the elements of each batch. If the iterable doesn’t
divide evenly, the last batch might contain fewer elements.

# Example 1: Basic Usage

Let's say you have a list of items, and you want to process them in batches of 3. You can use `batched` like so:

```python
import itertools

data = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
result = list(itertools.batched(data, 3))

print(result)
```

**Output:**

```python
[('A', 'B', 'C'), ('D', 'E', 'F'), ('G',)]
```

In this example, the input list is chunked into three groups. The last group contains only one element since the list
isn’t evenly divisible by 3.

# Example 2: Handling Incomplete Batches

If you're working with a strict batch size and don’t want the final batch to be smaller than `n`, you can set
the `strict` parameter to `True`. This will raise a `ValueError` if the final batch is incomplete.

```python
import itertools

data = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
result = list(itertools.batched(data, 3, strict=True))

print(result)
```

**Output:**

```python
ValueError: batched() would create an incomplete batch
```

This error occurs because the last batch would be incomplete (containing just 'G'), and the `strict=True` flag enforces
that all batches must be full.

# Example 3: Working with Larger Data

The `batched` function is also useful when working with large datasets. Instead of iterating over every element
individually, you can process it in smaller chunks. This can be especially beneficial in scenarios where you’re working
with memory-intensive operations.

```python
import itertools

data = range(10)
result = list(itertools.batched(data, 4))

print(result)
```

**Output:**

```python
[(0, 1, 2, 3), (4, 5, 6, 7), (8, 9)]
```

Here, we have a range of numbers from 0 to 9, and we divide them into batches of 4.

# Conclusion

`batched` from the `itertools` module is a simple but powerful function for dividing iterables into smaller chunks.
Whether you're processing data in smaller pieces or preparing paginated API requests, `batched` streamlines the process,
making your code cleaner and more efficient. If you're working with large datasets or need to process items in groups,
this is a tool you’ll want in your toolkit.