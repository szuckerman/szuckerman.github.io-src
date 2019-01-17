Title: Integer Division in Redshift: Gotcha!
Date: 2019-01-17 15:30
Modified: 2019-01-17 15:30
Category: Redshift
Tags: redshift, sql
Slug: integer_division_in_redshift
Authors: Sam Zuckerman
Summary: Data types can always be tricky in SQL. Here's an interesting quirk I noticed with regard to integer division in Redshift.

# What's the problem?

## Background to Integer Division

Usually when someone divides two numbers, which don't divide evenly, with a calculator or another software program, he expects there to be a decimal. 

For example, if I divide 3 by 2, I would expect to see 1.5.

It's well known with some programming situations (like Python 2) that the answer to the above would be "1" since nothing after the decimal is preserved.

The following Redshift code would also return 1.

```sql
SELECT 3/2
```

## What's the solution to get a decimal then?

If you cast the values to a `float`, then everything works nicely.

For example, in Python 2 the following would both return 1.5:

```python
3.0/2.0
>>> 1.5

float(3)/float(2)
>>> 1.5
```

# How to solve this in Redshift:

In Redshift, the answer is basically the same, you merely cast to a `float`, or `decimal`, but there's a big caveat.

Let's say you try the following:

```sql
SELECT NUMERATOR::DECIMAL/DENOMINATOR::DECIMAL
```

You might still have integer division! Why? Because toward the bottom of [this AWS documentation on numeric computations in Redshift](https://docs.aws.amazon.com/redshift/latest/dg/r_numeric_computations201.html) it mentions that:

> When one of the operands in a calculation has an INTEGER data type and the other operand is DECIMAL, the INTEGER operand is implicitly cast as a DECIMAL:
> 
> - INT2 (SMALLINT) is cast as DECIMAL(5,0)
> - INT4 (INTEGER) is cast as DECIMAL(10,0)
> - INT8 (BIGINT) is cast as DECIMAL(19,0)

Basically, instead of the above, you might want to cast as:

```sql
SELECT NUMERATOR::DECIMAL(10,2)/DENOMINATOR::DECIMAL(10,2)
```

Or, rather, something that keeps the precision in the number. The first number after the word `DECIMAL` is the `precision`, loosely meaning, "how many numbers total in the number (including after the decimal point)" and `scale` is "how many numbers after the decimal point".

The above have a `scale` of 0, which essentially makes them look like an `INTEGER`; just add `scale` to the mix and you should be good to go!

> __Note:__ I've seen inconsistent results with this truncation behavior, especially when I have queries containing aggregations upon aggregations. For example, even `SELECT NUMERATOR::DECIMAL/DENOMINATOR::DECIMAL` returns as a `DECIMAL`. The main point of this post is to be able to troubleshoot what the issue might be if you think you've casted data types properly and don't want to spend too much time pulling your hair out.