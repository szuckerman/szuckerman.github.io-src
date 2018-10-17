#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'sam zuckerman'
SITENAME = 'programming notes'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10



THEME = "pelican-elegant-1.3"

DISQUS_SITENAME = 'szuckerman-github-io-1'


LANDING_PAGE_ABOUT = {'title': 'I am full stack developer focusing on data-driven applications', 'details': 'I work as a full stack developer analyst using various database and web technologies to make data analysis more efficient. I work with the whole pipeline, from data engineering and database design to front end UX.'}

PROJECTS = [{
    'name': 'Bookscouter Linear Optimizer',
    'url': 'https://github.com/szuckerman/Bookscouter_LP',
    'description':
    'A program which scrapes bookscouter.com for given ISBN numbers and determines to which stores they should be sent to maximize profit.'},
    {'name': 'Elegant Theme for Pelican',
    'url': 'http://oncrashreboot.com/pelican-elegant',
    'description': 'A clean and distraction free theme, with search and a'
    ' lot more unique features, using Jinja2 and Bootstrap'}]



# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
