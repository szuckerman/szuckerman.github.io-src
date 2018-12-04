Title: Number of days between dates in Postgres
Date: 2018-12-04 15:30
Modified: 2018-12-04 15:30
Category: Postgres
Tags: sql, postgres
Slug: number_of_days_between_dates_in_postgres
Authors: Sam Zuckerman
Summary: Different database systems handle math for dates differently. Here's how you find the number of dates between dates in Postgres.

# Date math with dates and timestamps

In most relational databases getting the number of days between two dates is fairly straightforward. You merely subtract two date objects from eachother. This also works in PostgreSQL.

```sql
select TO_DATE('20180501', 'YYYYMMDD') - TO_DATE('20170101', 'YYYYMMDD') num_days
```

```sql
num_days
485
```

However, if even one of the objects is a `timestamp` and not a `date`, then the output is a bit messy:

```sql
select TO_DATE('20180501', 'YYYYMMDD') - TO_TIMESTAMP('20170101', 'YYYYMMDD') num_days
```

```sql
num_days
0 years 0 mons 485 days 0 hours 0 mins 0.00 secs
```

This situation happens often if you use one of the built-in date functions, such as `CURRENT_DATE`:

```sql
select CURRENT_DATE - TO_TIMESTAMP('20170101', 'YYYYMMDD') num_days
```

```sql
num_days
0 years 0 mons 702 days 0 hours 0 mins 0.00 secs
```

# Making the output cleaner

Here's how you make the output numeric, like the first example, instead of long and ugly like the others: You use the `DATE_PART` function.

Basically you just wrap `DATE_PART` around your output to grab the (wait for it...) date part.

You need to do this since, if you notice the above output, only days are returned. Even though one example is 485 days, it's not split into "1 year 125 days".

Here's the above example using `DATE_PART`:

```sql
select DATE_PART('day', CURRENT_DATE - TO_TIMESTAMP('20170101', 'YYYYMMDD')) num_days
```

```sql
num_days
702
```

# Further reading

I found [this page on Sqlines useful](http://www.sqlines.com/postgresql/how-to/datediff) if you need to perform a `DATE_DIFF` using units other than dates. 