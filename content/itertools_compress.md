Title: What's this in itertools? compress
Date: 2024-04-09 15:30
Modified: 2024-04-09 15:30
Category: Python
Tags: python, itertools, functions, code snippet
Slug: itertools_compress
Authors: Sam Zuckerman
Summary: Python's itertools module is a powerhouse of tools designed for efficient looping and iteration. Among its many useful functions, `compress` stands out as an elegant way to selectively filter elements from a sequence based on a selector sequence of booleans.

# Why do I need compress?

When working with sequences or iterables, you often encounter situations where you want to select certain elements based on conditions or flags. Rather than manually looping through sequences and conditions, `compress` lets you neatly extract the desired elements using another iterable as a filter.

Let's see it in action.

# Example without compress

Suppose we have a list of products, and another list indicating whether each product is in stock. To generate a list of available products, you might do something like this:

```python
products = ['apple', 'banana', 'cherry', 'date']
in_stock = [True, False, True, False]

available_products = []
for product, stock in zip(products, in_stock):
    if stock:
        available_products.append(product)

print(available_products)

>>> ['apple', 'cherry']
```

This method works fine but can become cumbersome and less readable with larger datasets.

# Example with compress

Using `itertools.compress` simplifies this task significantly:

```python
from itertools import compress

products = ['apple', 'banana', 'cherry', 'date']
in_stock = [True, False, True, False]

available_products = list(compress(products, in_stock))
print(available_products)

>>> ['apple', 'cherry']
```

`compress` pairs each element of the first iterable (`products`) with the corresponding boolean value in the second iterable (`in_stock`). If the selector value is `True`, the corresponding element from the first iterable is yielded.

# Advanced example with compress

What makes `compress` especially powerful is its seamless integration with generators and conditions evaluated on-the-fly:

```python
from itertools import compress

products = ['apple', 'banana', 'cherry', 'date']
stocks = [5, 0, 3, 0]

# Generate availability dynamically
available_products = list(compress(products, (stock > 0 for stock in stocks)))
print(available_products)

>>> ['apple', 'cherry']
```

This method enhances readability and eliminates unnecessary intermediate data structures.

# Conclusion

While you could use traditional loops or list comprehensions for filtering, `itertools.compress` makes the operation clearer, more concise, and efficient—especially when dealing with large sequences or complex conditions. Like many tools in the itertools module, mastering `compress` helps you write Python code that's both elegant and performant.

