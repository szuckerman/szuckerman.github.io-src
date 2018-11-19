Title: Using different styles with matplotlib
Date: 2018-11-19 15:30
Modified: 2018-11-19 15:30
Category: Python
Tags: python, pandas, matplotlib, visualization
Slug: different_styles_with_matplotlib
Authors: Sam Zuckerman
Summary: The default style for matplotlib charts looks nice, but sometimes you might want a change. It's not difficult to use a plethora of predefined alternate styles.


# Getting the styles
To see what alternate styles are available for matplotlib charts, you would first run `plt.style.available` to get the list of available styles.

This is assuming you've already run the following:

```python
import matplotlib.pyplot as plt
```



    >>> [u'seaborn-darkgrid',
         u'Solarize_Light2',
         u'seaborn-notebook',
         u'classic',
         u'seaborn-ticks',
         u'grayscale',
         u'bmh',
         u'seaborn-talk',
         u'dark_background',
         u'ggplot',
         u'fivethirtyeight',
         u'_classic_test',
         u'seaborn-colorblind',
         u'seaborn-deep',
         u'seaborn-whitegrid',
         u'seaborn-bright',
         u'seaborn-poster',
         u'seaborn-muted',
         u'seaborn-paper',
         u'seaborn-white',
         u'fast',
         u'seaborn-pastel',
         u'seaborn-dark',
         u'seaborn',
         u'seaborn-dark-palette']
         
There's various reasons why you might want a different theme; maybe depending on the content of your report you want a darker or lighter theme. If you're planning on printing the graphs and only have access to a B&W printer, grayscale charts might be preferred. Being mindful of users who may be colorblind is also a thoughtful consideration.

# Applying the style

The style must be applied before the charts are made, therefore it's a good idea to run the command right after importing the `matplotlab` module like so:

```python
import matplotlib.pyplot as plt
plt.style.use('ggplot')
```

__Note:__ If you change styles in the middle, you might get a mix of styles which is not consistent behavior and most likely not what you want. You should always restart your Jupyter kernal or Python instance when changing to a new style.

With this one line, you can easily customize your graphs and charts to your content making for a more polished reporting template.