Title: Finding Local Python Packages
Date: 2017-12-21 12:45
Modified: 2017-12-21 12:45
Category: Python
Tags: python, packages
Slug: finding-local-python-packages
Authors: Sam Zuckerman
Summary: Finding Local Python Packages

##Problem
I had a problem where I couldn't get Python to notice a package I just made.

What's great about Python is that you can work on a module, say `my_file.py`, and in another script write 'import my_file' to include that script in the current one. To include this module in a package, you merely add a blank `__init__.py` file to the folder the script is in. If the script is in a folder called 'my_folder', adding a `__init__.py` file to that folder will allow you to run:

```python
from my_folder import my_script
```

However, Python only knows about this package if it's in the same directory. I was trying to run some tests recently by having a separate 'tests' folder and I kept on getting an error of `ModuleNotFoundError: No module named my_folder`.

The reason it can't find the package is because Python only knows about packages loaded into the site-packages section of your Python installation.

For example, I use a virtual environment on my mac which loads all my packages (such as pandas, scipy, etc) here:

`/Users/my_username/.virtualenvs/virtualenv_name/lib/python3.6/site-packages`

When you install with pip, the packages get loaded there.

If I decided to build the package, then it would go there too, but I don't really want to do that while I'm just doing some brief testing.

##Solution
Add a .pth file to the site-packages/ directory.

It's fairly simple. Let's say my `my_folder` package is in the following `my_folder` directory (it's a common design to have a package in a folder of the same name).

`/Users/my_username/Documents/my_folder/my_folder/`

I would take this line and put it in a file called `my_folder.pth` (it can be named anything, though) and put that pth file in the site-packages/ directory. It might seem odd to just have a text file with that one line of a directory, but it works.

The file's location would be `/Users/my_username/.virtualenvs/virtualenv_name/lib/python3.6/site-packages/my_folder.pth`.

Now you can run `from my_folder import my_script` without any errors!