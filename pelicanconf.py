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

THEME = "elegant"

DISQUS_SITENAME = 'szuckerman-github-io-1'

LANDING_PAGE_TITLE = 'I am full stack developer focusing on data-driven applications'

PROJECTS = [{
    'name': 'Bookscouter Linear Optimizer',
    'url': 'https://github.com/szuckerman/Bookscouter_LP',
    'description':
        'A program which scrapes bookscouter.com for given ISBN numbers and determines to which stores they should be sent '
        'to maximize profit.'},
    {'name': 'PyJanitor',
     'url': 'https://github.com/ericmjl/pyjanitor',
     'description': '(Core Contributor) A Python implementation of the R package <a href="https://github.com/sfirke/janitor" target="_blank"'
                    '>janitor</a>, and more. It includes tools for examining and cleaning dirty data.'}]

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
GOOGLE_ANALYTICS = "UA-128575468-1"

ARTICLE_EXCLUDES = [
    'inprogress',
    'python_scripts'
]

STATIC_PATHS = ['images']
