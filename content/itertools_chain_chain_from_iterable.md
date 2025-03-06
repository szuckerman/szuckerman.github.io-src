Title: What's this in itertools? chain and chain.from_iterable
Date: 2023-10-05 14:30
Modified: 2023-10-05 14:30
Category: Python
Tags: python, itertools, functions, code snippet
Slug: itertools_chain_chain_from_iterable
Authors: Sam Zuckerman
Summary: The itertools module provides powerful tools like chain and chain.from_iterable to combine multiple iterables into one. chain allows you to concatenate multiple sequences, while chain.from_iterable flattens an iterable of iterables. These functions make it easy to work with data from various sources efficiently.

# Why do I need chain and chain.from_iterable?

There are many situations where you need to combine or flatten multiple iterables into a single iterable. Instead of
manually concatenating lists or looping through sequences, you can use `chain` to combine iterables
and `chain.from_iterable` to flatten an iterable of iterables. These functions make your code cleaner, more readable,
and more memory efficient, as they process the input lazily.

# What does chain do?

The `chain` function takes multiple iterables as input and returns a single iterator that yields elements from the first
iterable until it's exhausted, then proceeds to the next iterable, and so on. It’s great for combining multiple
sequences of data into one without creating a new list.

## Example 1: Using chain

```python
import itertools

# Combine multiple lists into a single iterator
iterable = itertools.chain([1, 2, 3], ['a', 'b', 'c'], [True, False])

print(list(iterable))
```

**Output:**

```python
[1, 2, 3, 'a', 'b', 'c', True, False]
```

In this example, we combined three lists—one with integers, one with strings, and one with booleans—into a single
sequence. `chain` lets us seamlessly iterate through all of them one by one.

# What does chain.from_iterable do?

While `chain` works well for directly passing multiple iterables, `chain.from_iterable` is used when you have a single
iterable that contains other iterables, and you want to flatten them into one. This function is especially useful when
you have a list of lists (or any iterable of iterables) and you want to iterate through all the elements without
nesting.

## Example 2: Using chain.from_iterable

```python
import itertools

# A list of lists (an iterable of iterables)
data = [[1, 2, 3], ['a', 'b', 'c'], [True, False]]

# Flatten the list of lists
flat_data = itertools.chain.from_iterable(data)

print(list(flat_data))
```

**Output:**

```python
[1, 2, 3, 'a', 'b', 'c', True, False]
```

Here, we used `chain.from_iterable` to flatten a list of lists into a single iterator. This is a cleaner and more
memory-efficient way to flatten iterables compared to manually looping through them.

# Combining chain and chain.from_iterable

You can also combine `chain` and `chain.from_iterable` to process iterables in more complex ways. For example, you might
have a list of iterables and additional standalone elements to append to the sequence. `chain` handles both scenarios
smoothly.

## Example 3: Combining chain and chain.from_iterable

```python
import itertools

# A list of iterables and standalone elements
data = [[1, 2], [3, 4]]
additional_data = ['a', 'b', 'c']

# Flatten the data and add additional elements
combined_data = itertools.chain.from_iterable(data)
final_data = itertools.chain(combined_data, additional_data)

print(list(final_data))
```

**Output:**

```python
[1, 2, 3, 4, 'a', 'b', 'c']
```

Here, we first flattened a list of lists using `chain.from_iterable`, and then appended additional standalone elements
using `chain`.

# Conclusion

The `chain` and `chain.from_iterable` functions from the `itertools` module are incredibly helpful for combining
multiple iterables into one. Whether you’re dealing with separate iterables or a nested iterable, these functions
provide an elegant, memory-efficient solution for flattening and chaining sequences together. They’re great tools for
simplifying your code when you need to process data from multiple sources.