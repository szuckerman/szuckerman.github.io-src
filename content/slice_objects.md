Title: Using slice objects in Python
Date: 2017-10-03 15:30
Modified: 2017-10-03 15:30
Category: Python
Tags: python
Slug: slice-objects
Authors: Sam Zuckerman
Summary: Slice objects in Python


# Using Slice Objects in Python

Here's a cool little helpful piece of code I found for Python, it's called a slice object.

You know when you write `my_list[:2]` and you get the first two values? Well, the ":2" section is actually a slice object which you can input directly.

The notation for the object is `slice(None, 2)` or `slice(None, 2, None)`, similar to when you subset a list using one or two colons.

Therefore, if we want to get the first two values of the list we can write:

```python
my_list[slice(None, 2)]
```

Now, this doesn't actually save us anything from the usual syntax, but we can now save the slice object as its own variable:

```python
first_two = slice(None,2)

my_list[first_two]
```

My most common use case for slice objects is with pandas dataframes.

In one case I was generating a report with many different subsets of a few tables. Sometimes I needed the last column, which was a 'total' column, and othertimes not.

Therefore, it was much easier to write:

```python
def subset_my_df(df, include_total=True)
	'''This function takes a pandas dataframe and includes the 'total' column at the end, or not.'''
	if include_total:
		df_slice = slice(None,5)
	else:
		df_slice = slice(None,4)

	cols=df.columns[df_slice]

	subset_df = df[cols]

	return subset_df
```


Than to try to hardcode the columns without the total, especially if you have dataframes with different column names.

You need the `cols=df.columns[df_slice]` line to subset the columns.  If you don't include that line you'll be subsetting by rows instead.