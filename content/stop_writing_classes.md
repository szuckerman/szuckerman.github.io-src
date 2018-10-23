Title: Thoughts on "Stop Writing Classes" PyCon 2012 talk
Date: 2018-10-17 17:30
Modified: 2018-10-17 17:30
Category: Python
Tags: python, youtube, videos
Slug: stop_writing_classes
Authors: Sam Zuckerman
Summary: There's a [famous talk by Jack Diederich](https://www.youtube.com/watch?v=o9pEzgHorH0) about clean and readable Python code from PyCon 2012. The main point of his talk (and the title) is called "Stop Writing Classes". 

# Writing Classes for Data Analysis

There's a [famous talk by Jack Diederich](https://www.youtube.com/watch?v=o9pEzgHorH0) about clean and readable Python code from PyCon 2012. The main point of his talk (and the title) is called "Stop Writing Classes".

As someone who works mainly in the data space, I thought this talk was interesting since I don't usually write classes at all.  Usually when working with a Jupyter notebook or some other interactive REPL scripting session, it doesn't make sense to have many custom objects floating around; usually the fanciest objects are relegated to Pandas Dataframes or SciKit-Learn models.

That being said, there have been some cases where I did make 'crazy' objects as containers for data (this is pre-Python 3.7 dataclasses, btw). In my specific use case I would have an object to represent the item my company is selling and then have various 'getters' that do some sort of math on the data and return specific metrics.

For example, the class might look something like this:

```python
class Product:
    def __init__(self, product_id):
        self.product_id = product_id
        self.sales = self.get_sales()
        self.last_week_sales = self.get_last_week_sales()
        
    def get_sales(self):
        return '''sql query for sales data'''
        
    def get_last_week_sales(self):
        return [item for item in self.sales where days_ago <= 7]
      
```

And it goes on and on. It was kinda fun to organize data like this in the first place and get code more 'organized' however, as you can see above, it gets unweildly fast.

Are all those initializers really necessary? How much space is this object taking up because we're storing all this info in the object?

I can imagine that were I to refactor the entire project I would just keep all the data in a big Pandas Dataframe and have various custom methods to slice the data as necessary.

# Diederich's Points

Now, the above class isn't 'horrible' according to Deiderich's talk. His main mantra is that "if you have a class that only has an \_\_init__ method, make it a function".

I like that point and I think that taking that into account with the above example, the above example class could be refactored to:

```python
def get_sales():
    return '''sql query for sales data'''
        
        
def get_last_week_sales():
    return [item for item in sales where days_ago <= 7]
    
    
def product_data(product_id, sales):
    sales_temp = get_sales(sales)
    return (product_id, sales_temp, get_last_week_sales(sales_temp))

      
```
I think this is cleaner in terms of its readability, but, more importantly. It's easier to test! You can put a unit test on each function and make sure everything's working correctly.

Overall, I really enjoyed the talk and think that it's another good example of how people sometimes forget to think Pythonically when coming from other languages.