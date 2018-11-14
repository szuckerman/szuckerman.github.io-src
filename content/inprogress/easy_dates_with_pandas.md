Title: Easy dates with Pandas
Date: 2018-11-12 15:30
Modified: 2018-11-12 15:30
Category: Python
Tags: python, pandas
Slug: easy_dates_with_pandas
Authors: Sam Zuckerman
Summary: Dates can be difficult to work with in any language. Fortunately there's many built-in tools for Pandas that make this less painful.


dat = pd.read_csv('something.csv', parse_dates=['date_col'])

dat['date_col'].dt.month

`dt` access the 

unstack and cumsum

Matplotlib themes

plt.style.use('ggplot')