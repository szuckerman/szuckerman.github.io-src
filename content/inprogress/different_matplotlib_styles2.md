Title: Using different styles with matplotlib2
Date: 2018-11-19 15:30
Modified: 2018-11-19 15:30
Category: Python
Tags: python, pandas, matplotlib, visualization
Slug: different_styles_with_matplotlib
Authors: Sam Zuckerman
Summary: The default style for matplotlib charts looks nice, but sometimes you might want a change. It's not difficult to use a plethora of predefined alternate styles.


Pandas won't plot points with NA values. That means that the lines won't show up in a line chart. However, you can't just 'drop' the NA values since that might remove values in columsn that are not NA (since the row gets removed). In this case you need to plot each column individually as to ensure that no data is accidentally dropped.  