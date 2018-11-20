Title: Finding duplicate rows to not break a primary key
Date: 2018-11-20 15:30
Modified: 2018-11-20 15:30
Category: SQL
Tags: sql, redshift, postgresql, code snippet
Slug: finding_duplicate_rows_in_sql
Authors: Sam Zuckerman
Summary: Primary keys are essential to relational databases. They ensure that rows in a database conform to a unique identifier. The following code snippet shows how to identify problematic rows.

Primary keys are essential to relational databases. They ensure that rows in a database conform to a unique identifier. The following code snippet shows how to identify problematic rows.

Sometimes when loading into a different table there can be issues with duplicates on distinct columns when you thought there should be none.

# Finding duplicates in a table

You might have a table in your database that doesn't contain any unique constraints. Let's assume the table is called `TABLE1` and we want to check duplicates on `COL1` and `COL2`. The following code will check to see what rows are duplicated, based on certain columns.

```sql
SELECT *
  FROM (
      SELECT 
        T1.*, 
        COUNT(*) OVER (PARTITION BY COL1, COL2) ROW_COUNT
      FROM TABLE1 T1
  )
 WHERE ROW_COUNT > 1
```

# How this works

This query uses `COUNT` as a window function to count what's given in the `PARTITION BY` section. That gets appended to our `TABLE` and from there we only keep the `TABLE1.ROW_COUNT`s that are greater than `1`, leaving the duplicate rows behind from `TABLE1`.

# Using on a query rather than table

It's a more common occurrence, however, to determine whether a query you're running may contain duplicate records and will fail when loading to a table with primary key constraints.

In that case you can wrap the query in a `WITH` clause (aka [subquery factoring clause](https://www.red-gate.com/simple-talk/sql/oracle/anatomy-of-a-select-statement-part-1-the-with-clause/)) and then reference that table in the snippet above:


```sql
WITH MY_TABLE AS (
    SELECT COL1, COL2, COL3
    FROM TABLE1
    WHERE COL3 != 'SOMETHING'
)

SELECT *
  FROM (
      SELECT 
        T1.*, 
        COUNT(*) OVER (PARTITION BY COL1, COL2) ROW_COUNT
      FROM MY_TABLE T1
  )
 WHERE ROW_COUNT > 1
```