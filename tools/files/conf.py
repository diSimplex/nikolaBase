# -*- coding: utf-8 -*-

# This Nikola conf.py file adds the "sister" nikolaBase directory to the
# collection of Python modules and then imports a "base" conf.py from the
# nikolaBase Python package.

# You can over-ride any of the nikolaBase configuration settings by simply
# changing their values in this file...

import os
import sys

sys.path.append(os.path.abspath("../nikolaBase"))

from nikolaBase.conf_base import *

EXTRA_PLUGINS_DIRS = [
  os.path.abspath("../nikolaBase/plugins")
]

EXTRA_THEMES_DIRS = [
  os.path.abspath("../nikolaBase/themes")
]

# Add any local changes here!

# Data about this site
#BLOG_AUTHOR = ""
#BLOG_TITLE = ""
#SITE_URL = ""
#BLOG_EMAIL = ""
#BLOG_DESCRIPTION = ""

# Uncomment the following line in any sub-sites which *are* blogs
#THIS_IS_A_BLOG_SITE = True
INDEX_DISPLAY_POST_COUNT = 15

# Uncomment the following line to make use of diSimplex's ServerSideIncludes
RENDER_DISIMPLEX_THEME_PARTIALS = True
