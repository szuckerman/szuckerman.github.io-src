Title: How to make a sequence of days in R
Date: 2018-10-10 17:30
Modified: 2018-10-10 17:30
Category: R
Tags: r, dates
Slug: make_date_range_r
Authors: Sam Zuckerman
Summary: Sometimes I need to make a sequence of dates to help with analysis. Here's a quick 1-liner in R.

I usually use the [lubridate](https://lubridate.tidyverse.org/) package for date manipulation, however, there's one item in that package that I haven't really gotten the hold of, which is making an array of dates. 

I usually have a situation where I'm missing data, such as with sales data. If a sale didn't take place on a certain day, then that date value won't show up. I want that date to have a value of zero.

I can make a sequence of dates with the following (base-R) command:

```r
date_sequence = seq(as.Date("2018/01/01"), as.Date("2018/12/31"), "days")
```

You can then put this in a `data.frame` which is easy to use with `dplyr`:

```r
all_dates = data.frame(date_sequence=date_sequence)

full_dataset = all_dates %>%
    left_join(sales_data)

full_dataset[is.na(full_dataset$product_sales), 'product_sales'] <- 0
```