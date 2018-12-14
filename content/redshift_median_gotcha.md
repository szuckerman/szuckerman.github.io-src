Title: Getting tripped up with "MEDIAN" in Redshift and PostgreSQL
Date: 2018-12-14 15:30
Modified: 2018-12-14 15:30
Category: Redshift
Tags: sql, redshift, postgres
Authors: Sam Zuckerman
Summary: Analytical functions are essential to working effectively with relational databases. There's a quirk with MEDIAN, however.

# MEDIAN in Redshift

Redshift has an interesting quirk in that when a `MEDIAN` function is called within a query, it implicitly give an `ORDER BY` for that column. 

## Window Functions in 5 seconds

Taking a step back, when working with window functions there's usually  `OVER` and  `ORDER BY` arguments and optionally, but often, a `PARTITION BY` argument as well.

If I wanted to order customer purchases by customer, I could do the following:

```sql
SELECT 
    CUSTOMER_ID,
    PRODUCT_NAME,
    ORDER_DATE,
    ROW_NUMBER() OVER (PARTITION BY CUSTOMER_ID ORDER BY ORDER_DATE) ORDER_NUMBER
FROM CUSTOMER_ORDERS
```

The `MEDIAN` function also uses an `ORDER BY` internally to determine the middle value, but doesn't use the same syntax as the above.

## Ok, fine... But why does this matter?

The above is important to keep in mind since multiple `MEDIAN` functions in a query will mess up. You'll get the following error:

```sql
ERROR: within group ORDER BY clauses for aggregate functions must be the same
```

You'll get this error if you have any combination of `LISTAGG`, `PERCENTILE_CONT`, or `MEDIAN` in a query that do not share the same `ORDER BY` column.

The [AWS Redshift Documentation](https://docs.aws.amazon.com/redshift/latest/dg/r_MEDIAN.html) shows the following example that will execute correctly when mixing these various window functions in a query:

```sql
select top 10 salesid, sum(pricepaid), 
percentile_cont(0.6) within group (order by salesid),
median (salesid)
from sales group by salesid, pricepaid;
```

## Solutions if you need multiple MEDIANs

If you absolutely need to have various medians in a result set, most likely the easiest option is to make multiple subqueries and then join them together at the end.

For example:

```sql
WITH MED_ITEMS_BOUGHT AS (
SELECT 
    CUSTOMER_ID,
    MEDIAN(ITEMS_BOUGHT) MED_ITEMS_BOUGHT
FROM 
  CUSTOMER_ORDERS
GROUP BY 
  CUSTOMER_ID
),
 
MED_PAYMENT AS (
SELECT 
  CUSTOMER_ID,
  MEDIAN(PAYMENT) MED_PAYMENT
FROM 
  CUSTOMER_ORDERS
GROUP BY 
  CUSTOMER_ID
)

SELECT 
    MIB.CUSTOMER_ID,
    MIB.MED_ITEMS_BOUGHT,
    MP.MED_PAYMENT
FROM 
    MED_ITEMS_BOUGHT MIB,
    MED_PAYMENT MP
WHERE MIB.CUSTOMER_ID = MP.CUSTOMER_ID
```

# MEDIAN in PostgreSQL

Unfortunately PostgreSQL doesn't have a native median function, but this doesn't really matter so much, as there is a `percentile_cont` function. `percentile_cont(0.5)` is equivalent to `median`.

You can see the description of `percentile_cont` in [the official PostgreSQL documentation](https://www.postgresql.org/docs/9.6/functions-aggregate.html#FUNCTIONS-ORDEREDSET-TABLE).

However, if you _must_ have a `median` function (i.e you're using SQLAlchemy and want to seamlessly switch backends) there's a user-defined `PL/pgSQL` function that can mimic this functionality.

The code for `median` is available [at this link](https://wiki.postgresql.org/wiki/Aggregate_Median).

# Summary

When using `MEDIAN` in Redshift, you cannot use more than one in a query at a time. A workaround is to make subqueries and join later. 

PostgreSQL does not have a native `MEDIAN` function, but this may be mimicked with the `percentile_cont(0.5)` function or [an additional PL/pgSQL function](https://wiki.postgresql.org/wiki/Aggregate_Median).