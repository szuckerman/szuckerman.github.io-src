Title: The easiest way to get data into Redshift
Date: 2018-10-23 11:30
Modified: 2018-10-23 11:30
Category: Python, Redshift, AWS
Tags: python, s3, redshift, aws, data transfer
Slug: get_data_into_redshift
Authors: Sam Zuckerman
Summary: There are many ways to load data into Redshift, this method, using the `COPY` command, should be the most efficient and reliable.

When using AWS and working in an analytical environment, you most likely have encountered Redshift at some point. Now, Redshift is awesome since it can contain a lot of data and query that data quickly. Due to its columnar storage, it's more effiecient to run a query such as:

```sql
select 
  customer_id,
  sum(amount) total_amount
 
from customer_table
 
group by 
  customer_id
``` 

since it only needs to look at those two columns, versus a system like Oracle that needs to read the entire row up to the necessary column, basically wasting time reading unnecessary data.

# Problem - How do we get the data to Redshift?
However, this presents us with a bit of a problem. We like a lot of data being stored in Redshift, but how can we 'get' it there? If I'm performing a transform and load from another table, the answer is trivial, but let's say I have a lot of data sitting on my computer I want in Redshift.

For example, I could have:
- Created a model in Python or R and want to add a table of the predictions to Redshift. This is especially true if you're manually tagging millions of customers. 
- Data not created from a standard format, such as disparate Excel files or even an Access DB (yes, I've had to do that...)

If the data is in the "few Gbs" of size, it won't take very long to upload, but for data integrity it's not the best idea to be loading row by row across a network for a huge table, but for Redshift row-by-row inserts aren't the best idea anyway, since, as mentioned above with the columnar storage, the columns are optimized based on the data types and Redshift doesn't like these individual row inserts as much as other relational databases do.

That's assuming you even have proper database credentials and connections. If you can't even connect directly, this is pretty much impossible.  

# Solution - S3 to the rescue!

Since Redshift and S3 are both part of AWS, they have baked in functionality together.

Here's the workflow:

1. Do your work in Python/R and save to a CSV or TXT file
2. Upload that file to S3
3. Create the table in Redshift (or truncate a previous one, depending on your use-case)
4. Use the Redshift COPY command to move the file from S3 to Redshift

Let's look at these in turn:

## Saving a CSV file

First, you need to make sure that your data is in a friendly format to save to a Redshift table. That means: try to stay UTF-8 and also try to avoid any quoting characters if possible. One single quote without another to close the quote will give you a lot of headaches later. Similarly, make sure that you have all the columns that you need for this insert.

## Uploading that file to S3

### Using boto3

There's various ways to upload a file to S3. The first, using [AWS's Boto3 library](https://boto3.readthedocs.io/) goes a bit like this:

_The first example from the [S3 section](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3.html) on boto3_
```python
import boto3
 
# Get the service client
s3 = boto3.client('s3')
 
# Upload tmp.txt to bucket-name at key-name
s3.upload_file("tmp.txt", "bucket-name", "key-name")
```

There are also other upload methods depending on what you're doing; see the S3 section for more examples.

This obviously assumes you already have a bucket to upload to. That's easy enough to do from the S3 UI console or the other methods in the boto3 library.

### Using AWS CLI

I personally prefer to use the AWS CLI to upload to S3 since I like the separation between 'modeling work' in Python/R and I/O to S3.

The S3 command works very much like the `cp` and `mv` commands in Unix systems, so it's easy to get get used to and also easy to use if you're used to moving files around your system anyway.

You can see all the commands available at their [S3 documentation for the CLI](https://docs.aws.amazon.com/cli/latest/reference/s3/index.html).

This is as easy as:
```bash
aws s3 cp filename s3://bucket-name/
```

You can do `cp` or `mv` to get the file to S3, but I usually prefer `cp` since I'll have a backup of the file in case something goes wrong with the flow to Redshift. I can then delete the file later after I'm done with the whole process.

## Create the table in Redshift

I'm not going to go into the specifics on creating a table in this section, as table creation is an entirely different beast by itself, but there are two important ideas to keep in mind:

1. Make sure that you have your sort keys set up properly when making the table, or else you'll need to `drop` the table and start again. According to the [AWS Redshift documentation](https://docs.aws.amazon.com/redshift/latest/dg/r_ALTER_TABLE.html): 

    > You can't add a column that is the distribution key (DISTKEY) or a sort key (SORTKEY) of the table.

2. The columns don't have to be in the same order as the CSV, but we'll discuss that more in the next section.

## Using the Redshift COPY command

### Access Rights

Before being able to move the file from S3 to Redshift, you need a role with the correct permissions. The role should (at least) have S3 read access and Redshift insert/write access. In the IAM console, you can create a new Redshift role and attach the `RedshiftAdminAccess` policy and `S3` policy. You use the ARN reference in the command. In this example, I'm using `'arn:aws:iam::<account_number>:role/<your_redshift_role>'` as the ARN.

### Syntax

The basic syntax to move a file from S3 to Redshift is the following:

```sql
copy schema.tablename(column1, column2) from 's3://bucket-name/filename.txt' iam_role 'arn:aws:iam::<account_number>:role/<your_redshift_role>';
```

If the columns in the file in S3 are in the exact order you need them for the table, you can just do:

```sql
copy schema.tablename from 's3://bucket-name/filename.txt' iam_role 'arn:aws:iam::<account_number>:role/<your_redshift_role>';
```

But I think it's more clear when the columns are explicit. Also, you can change the order of the columns, or even skip some columns like so:

```sql
copy schema.tablename(column3, column1) from 's3://bucket-name/filename.txt' iam_role 'arn:aws:iam::<account_number>:role/<your_redshift_role>';
```

I also like to have a `default` value on the table of `DATE_CREATED TIMESTAMP DEFAULT SYSDATE`, therefore if you're explicit with the column names when loading from Redshift, and don't include a column name of `DATE_CREATED`, that column will automatically populate to the load date.

### Other Useful COPY Commands

There's additional commands to add (full list [can be found here](https://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html)).

I find that I use the following most often:

- [CSV](https://docs.aws.amazon.com/redshift/latest/dg/copy-parameters-data-format.html#copy-csv)
  - This takes care of the fact that the file is a CSV and has defaults for the format.
- [QUOTE [AS] 'quote_character'](https://docs.aws.amazon.com/redshift/latest/dg/copy-parameters-data-format.html#copy-csv)
  - This can only be used with the `CSV` command and is useful if there's user input where there might be hanging apostrophes or something like that. If you change the quote character to something random it will ignore the single apostrophes. 
- [DELIMITER](https://docs.aws.amazon.com/redshift/latest/dg/copy-parameters-data-format.html#copy-delimiter)
  - You can change `DELIMITER` to `\t` if you have a txt file. You don't need the `CSV` command in this case.
- [IGNOREHEADER](https://docs.aws.amazon.com/redshift/latest/dg/copy-parameters-data-conversion.html#copy-ignoreheader) 
  - If your file has column headers you'll get an error when loading. Use `IGNOREHEADER 1` to skip the first line.

With some of these commands added, your `COPY` command might look more like this:

```sql
copy schema.tablename(column3, column1) from 's3://bucket-name/filename.txt' iam_role 'arn:aws:iam::<account_number>:role/<your_redshift_role>' DELIMITER '\t' QUOTE '^' IGNOREHEADER 1;
```

There you have it! Your data is now safely, and securely, in Redshift to be able to be joined with other tables for efficient data processing.

After this is all done, you might want to go back and delete the local file from your computer and the file from S3 (if it's not needed anymore).

# Summary

In this post we looked at how to save data as a `CSV` or `TXT` file, upload to S3 and then use the `COPY` command in Redshift to quickly and efficiently move said data to the Redshift cluster, streamlining an often painful process of moving large amounts of data through various systems. 

