Title: What's this in functools? cmp_to_key
Date: 2018-11-14 15:30
Modified: 2018-11-14 15:30
Category: Python
Tags: python, functools, functions, code snippet
Slug: functools_cmp_to_key
Authors: Sam Zuckerman
Summary: There's a lot of cool stuff in the functools module. Some small additions to your functions will greatly increase your productivity and your code quality. `cmp_to_key` is a slick way to make a custom sorting order for your functions.

# Why do I need cmp_to_key?

Sorting is generally straightfoward; items can be sorted in number order or alphabetically. However, sometimes you need to sort items in a different order and the `cmp_to_key` function in the `functools` module is an easy way to implement custom sorting functions.

# What is a comparison function?

According to the [`functools` documentation](https://docs.python.org/3/library/functools.html):
> A comparison function is any callable that accept two arguments, compares them, and returns a negative number for less-than, zero for equality, or a positive number for greater-than. 

Generally comparison functions are used as keys to other functions (like `sorted` or `min` or any function that takes a `key` argument).

# Let's see this in action

The following code block uses `cmp_to_key` to make a standard sorting function. It actually doesn't do anything differently than just using `sorted` by itself.

```python
from functools import cmp_to_key


def standard_comparison(x,y):
	if x > y:
		return 1
	elif x < y:
		return -1
	else:
		return 0


my_list = [4,2,3,1,5,3]


sorted(my_list, key=cmp_to_key(standard_comparison))
```

### Output:
```python
>>> [1, 2, 3, 3, 4, 5]
```

## Looking into standard_comparison

Let's take a look at the `standard_comparison` function above. It takes two numbers, compares them, and returns "1", "-1", or "0" depending on whether the numbers are bigger, smaller or the same as each other.

 
## But what does this actually mean?

Basically, while the `sorted` function is looking through the list, it's getting responses of "1", "-1", or "0" telling it where to put certain values. For our purposes "1" can be understood as "put to the right side of the list", "-1" as "put to the left side of the list" and "0" as "do nothing".

# Customizing the comparison function

I can change the above `standard_comparison` to be "only consider a number to be 'bigger' if it's more than two than the next one," which leads to some interesting results as you can see above.

```python
from functools import cmp_to_key


def weird_comparison(x,y):
	if x + 2 > y:
		return 1
	elif x < y:
		return -1
	else:
		return 0


my_list = [4,2,3,1,5,3]


sorted(my_list, key=cmp_to_key(weird_comparison))
```

### Output:
```python
>>> [2, 1, 4, 3, 3, 5]
```

# Realistic Example

The above was a cute example of messing with the comparison function, but the real question is "when would someone actually use this?"

I think the most common example would be "almost" alphabetical sorting.

I've needed to sort metrics into certain periods and usually there's no natural ordering on which to sort. This is especially helpful when the data is output in a web application. 

The following example sorts a list of dictionaries by their respective time periods. The order is 'Lifetime', 'Trailing 7 Days', 'Trailing 30 Days', 'First Day'. Without our sorting function it would be difficult to get to this order since "First Day" would always be first in the list. 


```python
from functools import cmp_to_key

def my_time_comparison(x,y):
	time_list = [
		'Lifetime',
		'Trailing 7 Days',
		'Trailing 30 Days',
		'First Day'
		]
	first_time = x['SALES_TIME_PERIOD']
	second_time = y['SALES_TIME_PERIOD']
	first_time_idx = time_list.index(first_time)
	second_time_idx = time_list.index(second_time)
	if first_time_idx > second_time_idx:
		return 1
	elif first_time_idx < second_time_idx:
		return -1
	else:
		return 0


sales_list = [
    {'PRODUCT_ID': 1, 'SALES_TIME_PERIOD': 'Trailing 7 Days', 'UNITS': 20 },
    {'PRODUCT_ID': 1, 'SALES_TIME_PERIOD': 'First Day', 'UNITS': 2 },
    {'PRODUCT_ID': 1, 'SALES_TIME_PERIOD': 'Trailing 30 Days', 'UNITS': 40 },
    {'PRODUCT_ID': 1, 'SALES_TIME_PERIOD': 'Lifetime', 'UNITS': 50 },
    {'PRODUCT_ID': 2, 'SALES_TIME_PERIOD': 'Trailing 7 Days', 'UNITS': 30 },
    {'PRODUCT_ID': 2, 'SALES_TIME_PERIOD': 'First Day', 'UNITS': 3 },
    {'PRODUCT_ID': 2, 'SALES_TIME_PERIOD': 'Trailing 30 Days', 'UNITS': 50 },
    {'PRODUCT_ID': 2, 'SALES_TIME_PERIOD': 'Lifetime', 'UNITS': 60 },
    {'PRODUCT_ID': 3, 'SALES_TIME_PERIOD': 'Trailing 7 Days', 'UNITS': 41 },
    {'PRODUCT_ID': 3, 'SALES_TIME_PERIOD': 'First Day', 'UNITS': 4 },
    {'PRODUCT_ID': 3, 'SALES_TIME_PERIOD': 'Trailing 30 Days', 'UNITS': 61 },
    {'PRODUCT_ID': 3, 'SALES_TIME_PERIOD': 'Lifetime', 'UNITS': 71 }]

sorted(sales_list, key=cmp_to_key(my_time_comparison))
```

### Output:

```python
>>> [{'PRODUCT_ID': 1, 'SALES_TIME_PERIOD': 'Lifetime', 'UNITS': 50},
     {'PRODUCT_ID': 2, 'SALES_TIME_PERIOD': 'Lifetime', 'UNITS': 60},
     {'PRODUCT_ID': 3, 'SALES_TIME_PERIOD': 'Lifetime', 'UNITS': 71},
     {'PRODUCT_ID': 1, 'SALES_TIME_PERIOD': 'Trailing 7 Days', 'UNITS': 20},
     {'PRODUCT_ID': 2, 'SALES_TIME_PERIOD': 'Trailing 7 Days', 'UNITS': 30},
     {'PRODUCT_ID': 3, 'SALES_TIME_PERIOD': 'Trailing 7 Days', 'UNITS': 41},
     {'PRODUCT_ID': 1, 'SALES_TIME_PERIOD': 'Trailing 30 Days', 'UNITS': 40},
     {'PRODUCT_ID': 2, 'SALES_TIME_PERIOD': 'Trailing 30 Days', 'UNITS': 50},
     {'PRODUCT_ID': 3, 'SALES_TIME_PERIOD': 'Trailing 30 Days', 'UNITS': 61},
     {'PRODUCT_ID': 1, 'SALES_TIME_PERIOD': 'First Day', 'UNITS': 2},
     {'PRODUCT_ID': 2, 'SALES_TIME_PERIOD': 'First Day', 'UNITS': 3},
     {'PRODUCT_ID': 3, 'SALES_TIME_PERIOD': 'First Day', 'UNITS': 4}]

```

## How did the above work?

1. First we put the order we wanted to use in `time_list`.
2. As we step through the list, we access the value of `SALES_TIME_PERIOD` in each dictionary.
3. We compare the value in our dictionary to the order that value falls in the list. For example, "Lifetime" would return an index of 0 and "First Day" would return an index of 3.
4. We compare the indices to determine which is the "smaller value" which should be at the top and the "larger value" that should be toward the bottom. Since 0 < 3, "Lifetime" gets placed above "First Day".

# Conclusion

 `cmp_to_key` is an easy and effective way to implement your custom sorting heuristics. With a minimum amount of set-up you can retain a sort order that can be used in multiple applications and only needs to be passed as a `key` argument to functions.