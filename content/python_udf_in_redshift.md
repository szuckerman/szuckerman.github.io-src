Title: Creating a Python UDF in Redshift
Date: 2018-11-01 15:30
Modified: 2018-11-01 15:30
Category: Python
Tags: python, redshift, code snippet
Slug: python_udf_in_redshift
Authors: Sam Zuckerman
Summary: Here's some basic code on how to directly insert a Python function into your Redshift instance.

# What's a UDF?
Databases are central to effective programming and there are more and more offerings to handle people's workloads.  

One that should greatly increase ones' productivity is in the database arena is moving beyond basic SQL and using additional programming structures such as stored procedures or UDFs.

This post will focus on UDFs in Redshift and how we can leverage Python to write them.

So, it sounds interesting, but at this point you might be wondering, _what exactly is a UDF_?

> A UDF is a User-Defined Function that gets stored in the database. Instead of using standard functions like `sum()` one can make a custom one like `my_crazy_function()`.

I feel that this isn't 100% necessary if you're only writing SQL anyway (you can put your logic in a subquery and join to your new table), but if you like to write Python (like me), this can make some of the logic easier depending on the use case.

# How does Python interact with Redshift?

There's much more information contained in [the official Redshift documentation on Python UDFs](https://docs.aws.amazon.com/redshift/latest/dg/udf-python-language-support.html), but the main points I took from it are:

- It runs Python 2.7
- It contains the following packages by default:
      - numpy: 1.8.2
      - pandas: 0.14.1
      - python-dateutil: 2.2
      - pytz: 2014.7
      - scipy: 0.12.1
      - six: 1.3.0
      - wsgiref: 0.1.2
- [You can add your own custom packages](https://docs.aws.amazon.com/redshift/latest/dg/udf-python-language-support.html#udf-importing-custom-python-library-modules)

Basically, Python 2.7 is already "there" with the packages I listed above.

# How do permissions work?

In Redshift, Python is referred to as `plpythonu`. To allow users (besides the superuser) to use the language, the following command must be run:

```sql
GRANT USAGE ON LANGUAGE plpythonu TO USERNAME;
```

# Making the Function

After the permissions are added, you can add a function like so:

```sql
create function add_three_numbers(num1 float, num2 float, num3 float)
RETURNS float
STABLE 
AS $$
return num1 + num2 + num3
$$ LANGUAGE plpythonu;

```

This function adds three numbers and returns their result. In the definition, all the data types (parameters and return value) must be specified. Remember, these are Redshift datatypes, but it just so happens that `float` exists in both languages.

Everything between the `$$`'s is the Python code. If you wanted to use `pandas` at this point you would `import pandas as pd` at the beginning of the function definition.

`STABLE` in this case deals with the query optimizer and how it should evaluate the function. [The Redshift documentation goes into more detail on this for its different values](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_FUNCTION.html), but for the time being you should be OK keeping it with `STABLE`.

__Note:__ This doesn't currently work for aggregation. I.e. you can't use `group by` and your Python function like you would `sum` or `avg`. We're going to discuss a workaround in a later post.

# Output

```sql
SELECT add_three_numbers(1,2,3)
```

Would output 6. Remember, Redshift doesn't require a `FROM` clause.

Now you should have a basic understanding of how to add a Python function to your Redshift database.