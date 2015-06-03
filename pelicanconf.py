#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
#######################################################################
#                               GENERAL                               #
#######################################################################

AUTHOR = 'Michael Medin'
SITENAME = 'Michael Medin'
SITESUBTITLE = 'Random thoughts on development, monitoring and family life…'
STARTING_YEAR = 2011
SITEURL = ''
DEBUG = True

THEME = "themes/mickem-bootstrap"
PLUGIN_PATHS = ["plugins", 'plugins/pelican-plugins', 'plugins/pelican_youtube']
PLUGINS = [
    "pelican-bootstrapify", 
    "liquid_tags", 
    "liquid_tags.youtube", 
    "pelican_youtube", 
    "sitemap", 
    "pelican-page-hierarchy", 
    "assets", 
    "summary", 
    "neighbors",
    #"clean_summary", 
    "related_posts",
    #"autostatic", 
    "pelican-advthumbnailer",
    "tipue_search"
    ]

PATH = "content"


DEFAULT_DATE_FORMAT = '%Y-%m-%d'
TIMEZONE = 'Europe/Stockholm'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DISPLAY_PAGES_ON_MENU = True
DISPLAY_ARCHIVES_ON_MENU = False
YEAR_ARCHIVE_SAVE_AS = 'archive/{date:%Y}/index.html'
ARCHIVES_URL = 'archive'
ARCHIVES_SAVE_AS = 'archive/index.html'
CATEGORIES_URL = 'category'
CATEGORIES_SAVE_AS = 'category/index.html'
AUTHORS_URL = 'authors'
AUTHORS_SAVE_AS = 'authors/index.html'
AUTHOR_URL = 'author/{slug}'
AUTHOR_SAVE_AS = 'author/{slug}/index.html'
TAGS_URL = 'tag'
TAGS_SAVE_AS = 'tag/index.html'
TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'

#PAGINATION_PATTERNS = (
#    (1, '{base_name}/', '{base_name}/index.html'),
#    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
#)


# Social widget
SOCIAL = (("Github", "https://github.com/mickem"),
          ("Facebook", "https://www.facebook.com/medinmichael"),
          ("Twitter", "https://twitter.com/mickem"),
          ("Google+", "https://plus.google.com/u/0/+MichaelMedin/"),
          ("LinkedIn", "https://se.linkedin.com/in/mickem"),)

TWITTER_USERNAME = "mickem"
TWITTER_CARD = True
OPEN_GRAPH = True
OPEN_GRAPH_ARTICLE_AUTHOR = "Michael Medin"
DEFAULT_METADESC = 'Random thoughts on development, monitoring and family life…'
DEFAULT_SOCIAL_IMAGE = 'images/michael-medin.jpg'
DEFAULT_PAGINATION = 10
FAVICON = 'images/michael-medin.jpg'
#######################################################################
#                             Contents                                #
#######################################################################

ARTICLE_PATHS = ['blog']
PAGE_PATHS = ['pages']

GOOGLE_SEARCH = "009388823403057951110:jwq9vehc3_q"

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
SLUGIFY_SOURCE = 'basename'

ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

CATEGORY_URL = 'category/{slug}'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'

TAG_URL = 'tag/{slug}'
TAG_SAVE_AS = 'tag/{slug}/index.html'

STYLESHEET_FILES = ("pygment.css",)

THEME_DEVELOPMENT = True

#######################################################################
#                             Extensions                              #
#######################################################################

MD_EXTENSIONS = ['codehilite(css_class=highlight)','extra']

SKIP_COLOPHON= True

RELATED_POSTS_MAX = 5

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}