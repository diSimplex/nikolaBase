# -*- coding: utf-8 -*-

import time

# !! This is the configuration of Nikola. !! #
# !!  You should edit it to your liking.  !! #

# Data about this site
BLOG_AUTHOR = "Nikola Tesla"  # (translatable)
BLOG_TITLE = "My Nikola Site"  # (translatable)
# This is the main URL for your site. It will be used
# in a prominent link. Don't forget the protocol (http/https)!
SITE_URL = "https://example.com/"
# This is the URL where Nikola's output will be deployed.
# If not set, defaults to SITE_URL
# BASE_URL = "https://example.com/"
BLOG_EMAIL = "n.tesla@example.com"
BLOG_DESCRIPTION = "This is a demo site for Nikola."  # (translatable)

# What is the default language?
DEFAULT_LANG = "en"

# What other languages do you have?
# The format is {"translationcode" : "path/to/translation" }
# the path will be used as a prefix for the generated pages location
TRANSLATIONS = {
    DEFAULT_LANG: "",
    # Example for another language:
    # "es": "./es",
}

# What will translated input files be named like?
TRANSLATIONS_PATTERN = '{path}.{lang}.{ext}'

# Links for the sidebar / navigation bar.  (translatable)
# This is a dict.  The keys are languages, and values are tuples.
NAVIGATION_LINKS = {
    DEFAULT_LANG: (
        ("/archive.html", "Archive"),
        ("/categories/", "Tags"),
        ("/rss.xml", "RSS feed"),
    ),
}

# Alternative navigation links. Works the same way NAVIGATION_LINKS does,
# although themes may not always support them. (translatable)
# (Bootstrap 4: right-side of navbar, Bootblog 4: right side of title)
NAVIGATION_ALT_LINKS = {
    DEFAULT_LANG: ()
}

# Name of the theme to use.
#THEME = "bootblog4"
THEME = "disimplex"

# A theme color. In default themes, it might be displayed by some browsers as
# the browser UI color (eg. Chrome on Android). Other themes might also use it
# as an accent color (the default ones don’t). Must be a HEX value.
THEME_COLOR = '#5670d4'

# Theme configuration. Fully theme-dependent. (translatable)
# Samples for bootblog4 (enabled) and bootstrap4 (commented) follow.
# bootblog4 supports: featured_large featured_small featured_on_mobile
#                     featured_large_image_on_mobile featured_strip_html sidebar
# bootstrap4 supports: navbar_light (defaults to False)
#                      navbar_custom_bg (defaults to '')

# Config for bootblog4:
THEME_CONFIG = {
    DEFAULT_LANG: {
        # Show the latest featured post in a large box, with the previewimage as its background.
        'featured_large': False,
        # Show the first (remaining) two featured posts in small boxes.
        'featured_small': False,
        # Show featured posts on mobile.
        'featured_on_mobile': True,
        # Show image in `featured_large` on mobile.
        # `featured_small` displays them only on desktop.
        'featured_large_image_on_mobile': True,
        # Strip HTML from featured post text.
        'featured_strip_html': False,
        # Contents of the sidebar, If empty, the sidebar is not displayed.
        'sidebar': ''
    }
}

# POSTS and PAGES contains (wildcard, destination, template) tuples.
# (translatable)
#
POSTS = (
    ("posts/*.rst", "posts", "post.tmpl"),
    ("posts/*.md", "posts", "post.tmpl"),
    ("posts/*.txt", "posts", "post.tmpl"),
    ("posts/*.html", "posts", "post.tmpl"),
)
PAGES = (
    ("pages/*.rst", "", "page.tmpl"),
    ("pages/*.md", "", "page.tmpl"),
    ("pages/*.txt", "", "page.tmpl"),
    ("pages/*.html", "", "page.tmpl"),
)


# Below this point, everything is optional

# Post's dates are considered in UTC by default, if you want to use
# another time zone, please set TIMEZONE to match. Check the available
# list from Wikipedia:
TIMEZONE = "Europe/London"

# Date format used to display post dates. (translatable)
# Used by babel.dates, CLDR style: http://cldr.unicode.org/translation/date-time-1/date-time
# You can also use 'full', 'long', 'medium', or 'short'
# DATE_FORMAT = 'yyyy-MM-dd HH:mm'

# Date format used to display post dates, if local dates are used. (translatable)
# Used by Luxon: https://moment.github.io/luxon/docs/manual/formatting
# Example for presets: {'preset': True, 'format': 'DATE_FULL'}
# LUXON_DATE_FORMAT = {
#     DEFAULT_LANG: {'preset': False, 'format': 'yyyy-MM-dd HH:mm'},
# }

# Date fanciness.
#
# 0 = using DATE_FORMAT and TIMEZONE (without JS)
# 1 = using LUXON_DATE_FORMAT and local user time (JS, using Luxon)
# 2 = using a string like “2 days ago” (JS, using Luxon)
#
# Your theme must support it, Bootstrap already does.
# DATE_FANCINESS = 0

# Customize the locale/region used for a language.
# For example, to use British instead of US English: LOCALES = {'en': 'en_GB'}
# LOCALES = {}

# One or more folders containing files to be copied as-is into the output.
# The format is a dictionary of {source: relative destination}.
# Default is:
# FILES_FOLDERS = {'files': ''}
# Which means copy 'files' into 'output'

# One or more folders containing code listings to be processed and published on
# the site. The format is a dictionary of {source: relative destination}.
# Default is:
# LISTINGS_FOLDERS = {'listings': 'listings'}
# Which means process listings from 'listings' into 'output/listings'

# A mapping of languages to file-extensions that represent that language.
# Feel free to add or delete extensions to any list, but don't add any new
# compilers unless you write the interface for it yourself.
#
# The default compiler for `new_post` is the first entry in the POSTS tuple.
#
# 'rest' is reStructuredText
# 'markdown' is Markdown
# 'html' assumes the file is HTML and just copies it
COMPILERS = {
    "rest": ['.rst', '.txt'],
    "markdown": ['.md', '.mdown', '.markdown'],
    "textile": ['.textile'],
    "txt2tags": ['.t2t'],
    "bbcode": ['.bb'],
    "wiki": ['.wiki'],
    "ipynb": ['.ipynb'],
    "html": ['.html', '.htm'],
    # PHP files are rendered the usual way (i.e. with the full templates).
    # The resulting files have .php extensions, making it possible to run
    # them without reconfiguring your server to recognize them.
    "php": ['.php'],
    # Pandoc detects the input from the source filename
    # but is disabled by default as it would conflict
    # with many of the others.
    # "pandoc": ['.rst', '.md', '.txt'],
}

# Preferred metadata format for new posts
# "YAML": YAML wrapped in "---"
METADATA_FORMAT = "YAML"

# If you do not want to display a tag publicly, you can mark it as hidden.
# The tag will not be displayed on the tag list page and posts.
# Tag pages will still be generated.
HIDDEN_TAGS = ['mathjax']


# If CATEGORY_ALLOW_HIERARCHIES is set to True, categories can be organized in
# hierarchies. For a post, the whole path in the hierarchy must be specified,
# using a forward slash ('/') to separate paths. Use a backslash ('\') to escape
# a forward slash or a backslash (i.e. '\//\\' is a path specifying the
# subcategory called '\' of the top-level category called '/').
CATEGORY_ALLOW_HIERARCHIES = False
# If CATEGORY_OUTPUT_FLAT_HIERARCHY is set to True, the output written to output
# contains only the name of the leaf category and not the whole path.
CATEGORY_OUTPUT_FLAT_HIERARCHY = False

# If you do not want to display a category publicly, you can mark it as hidden.
# The category will not be displayed on the category list page.
# Category pages will still be generated.
HIDDEN_CATEGORIES = []

# If ENABLE_AUTHOR_PAGES is set to True and there is more than one
# author, author pages are generated.
ENABLE_AUTHOR_PAGES = False

# If you do not want to display an author publicly, you can mark it as hidden.
# The author will not be displayed on the author list page and posts.
# Tag pages will still be generated.
HIDDEN_AUTHORS = ['Guest']

# Optional HTML that displayed on “main” blog index.html files.
# May be used for a greeting. (translatable)
FRONT_INDEX_HEADER = {
    DEFAULT_LANG: ''
}

# URLs to other posts/pages can take 3 forms:
# rel_path: a relative URL to the current page/post (default)
# full_path: a URL with the full path from the root
# absolute: a complete URL (that includes the SITE_URL)
# URL_TYPE = 'rel_path'
#
# Note that our use of "server side includes" / partials
# REQUIRES the use of 'full_path'
#
URL_TYPE = 'full_path'

# Extension for RSS feed files
# RSS_EXTENSION = ".xml"

# RSS filename base (without extension); used for indexes and galleries.
# (translatable)
# RSS_FILENAME_BASE = "rss"

# Atom filename base (without extension); used for indexes.
# (translatable)
ATOM_FILENAME_BASE = "feed"

# Extension for Atom feed files
# ATOM_EXTENSION = ".atom"

# A list of redirection tuples, [("foo/from.html", "/bar/to.html")].
#
# A HTML file will be created in output/foo/from.html that redirects
# to the "/bar/to.html" URL. notice that the "from" side MUST be a
# relative URL.
#
# If you don't need any of these, just set to []
REDIRECTIONS = []

# Presets of commands to execute to deploy. Can be anything, for
# example, you may use rsync:
# "rsync -rav --delete output/ joe@my.site:/srv/www/site"
# And then do a backup, or run `nikola ping` from the `ping`
# plugin (`nikola plugin -i ping`).  Or run `nikola check -l`.
# You may also want to use github_deploy (see below).
# You can define multiple presets and specify them as arguments
# to `nikola deploy`.  If no arguments are specified, a preset
# named `default` will be executed.  You can use as many presets
# in a `nikola deploy` command as you like.
# DEPLOY_COMMANDS = {
#     'default': [
#         "rsync -rav --delete output/ joe@my.site:/srv/www/site",
#     ]
# }

# github_deploy configuration
# For more details, read the manual:
# https://getnikola.com/handbook.html#deploying-to-github
# You will need to configure the deployment branch on GitHub.
GITHUB_SOURCE_BRANCH = 'src'
GITHUB_DEPLOY_BRANCH = 'master'

# The name of the remote where you wish to push to, using github_deploy.
GITHUB_REMOTE_NAME = 'origin'

# Whether or not github_deploy should commit to the source branch automatically
# before deploying.
GITHUB_COMMIT_SOURCE = True

# Where the output site should be located
# If you don't use an absolute path, it will be considered as relative
# to the location of conf.py
# OUTPUT_FOLDER = 'output'

# where the "cache" of partial generated content should be located
# default: 'cache'
# CACHE_FOLDER = 'cache'

# #############################################################################
# Image Gallery Options
# #############################################################################

# Use a thumbnail (defined by ".. previewimage:" in the gallery's index) in
# list of galleries for each gallery
GALLERIES_USE_THUMBNAIL = False

# Image to use as thumbnail for those galleries that don't have one
# None: show a grey square
# '/url/to/file': show the image in that url
GALLERIES_DEFAULT_THUMBNAIL = None

# Images will be scaled down according to IMAGE_THUMBNAIL_SIZE and MAX_IMAGE_SIZE
# options, but will have to be referenced manually to be visible on the site
# (the thumbnail has ``.thumbnail`` added before the file extension by default,
# but a different naming template can be configured with IMAGE_THUMBNAIL_FORMAT).

IMAGE_FOLDERS = {'images': 'images'}
# IMAGE_THUMBNAIL_SIZE = 400
# IMAGE_THUMBNAIL_FORMAT = '{name}.thumbnail{ext}'

# #############################################################################
# HTML fragments and diverse things that are used by the templates
# #############################################################################

# 'Read more...' for the index page, if INDEX_TEASERS is True (translatable)
INDEX_READ_MORE_LINK = '<p class="more"><a href="{link}">{read_more}…</a></p>'
# 'Read more...' for the feeds, if FEED_TEASERS is True (translatable)
FEED_READ_MORE_LINK = '<p><a href="{link}">{read_more}…</a> ({min_remaining_read})</p>'

# Append a URL query to the FEED_READ_MORE_LINK in Atom and RSS feeds. Advanced
# option used for traffic source tracking.
FEED_LINKS_APPEND_QUERY = False

# A HTML fragment describing the license, for the sidebar.
# (translatable)
LICENSE = ""
# I recommend using the Creative Commons' wizard:
# https://creativecommons.org/choose/
# LICENSE = """
# <a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
# <img alt="Creative Commons License BY-NC-SA"
# style="border-width:0; margin-bottom:12px;"
# src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png"></a>"""

# A small copyright notice for the page footer (in HTML).
# (translatable)
CONTENT_FOOTER = 'Contents &copy; {date}         <a href="mailto:{email}">{author}</a> - Powered by         <a href="https://getnikola.com" rel="nofollow">Nikola</a>         {license}'

# Things that will be passed to CONTENT_FOOTER.format().  This is done
CONTENT_FOOTER_FORMATS = {
    DEFAULT_LANG: (
        (),
        {
            "email": BLOG_EMAIL,
            "author": BLOG_AUTHOR,
            "date": time.gmtime().tm_year,
            "license": LICENSE
        }
    )
}

# A simple copyright tag for inclusion in RSS feeds that works just
# like CONTENT_FOOTER and CONTENT_FOOTER_FORMATS
RSS_COPYRIGHT = 'Contents © {date} <a href="mailto:{email}">{author}</a> {license}'
RSS_COPYRIGHT_PLAIN = 'Contents © {date} {author} {license}'
RSS_COPYRIGHT_FORMATS = CONTENT_FOOTER_FORMATS

# To use comments, you can choose between different third party comment
# systems.  The following comment systems are supported by Nikola:
#   disqus, facebook, intensedebate, isso, muut, commento, utterances
# You can leave this option blank to disable comments.
COMMENT_SYSTEM = ""
# And you also need to add your COMMENT_SYSTEM_ID which
# depends on what comment system you use. The default is
# "nikolademo" which is a test account for Disqus. More information
# is in the manual.
COMMENT_SYSTEM_ID = ""

# Create index.html for page folders?
# WARNING: if a page would conflict with the index file (usually
#          caused by setting slug to `index`), the PAGE_INDEX
#          will not be generated for that directory.
# PAGE_INDEX = False
# Enable comments on pages (i.e. not posts)?
# COMMENTS_IN_PAGES = False
# Enable comments on picture gallery pages?
# COMMENTS_IN_GALLERIES = False

# What file should be used for directory indexes?
# Defaults to index.html
# Common other alternatives: default.html for IIS, index.php
# INDEX_FILE = "index.html"

# If a link ends in /index.html,  drop the index.html part.
# http://mysite/foo/bar/index.html => http://mysite/foo/bar/
# (Uses the INDEX_FILE setting, so if that is, say, default.html,
# it will instead /foo/default.html => /foo)
STRIP_INDEXES = True

# List of files relative to the server root (!) that will be asked to be excluded
# from indexing and other robotic spidering. * is supported. Will only be effective
# if SITE_URL points to server root. The list is used to exclude resources from
# /robots.txt and /sitemap.xml, and to inform search engines about /sitemapindex.xml.
# ROBOTS_EXCLUSIONS = ["/archive.html", "/category/*.html"]

# Instead of putting files in <slug>.html, put them in <slug>/index.html.
# No web server configuration is required. Also enables STRIP_INDEXES.
# This can be disabled on a per-page/post basis by adding
#    .. pretty_url: False
# to the metadata.
PRETTY_URLS = True

# If True, publish future dated posts right away instead of scheduling them.
# Defaults to False.
# FUTURE_IS_NOW = False

# If True, future dated posts are allowed in deployed output
# Only the individual posts are published/deployed; not in indexes/sitemap
# Generally, you want FUTURE_IS_NOW and DEPLOY_FUTURE to be the same value.
# DEPLOY_FUTURE = False
# If False, draft posts will not be deployed
# DEPLOY_DRAFTS = True

# Allows scheduling of posts using the rule specified here (new_post -s)
# Specify an iCal Recurrence Rule: https://www.kanzaki.com/docs/ical/rrule.html
# SCHEDULE_RULE = ''
# If True, use the scheduling rule to all posts (not pages!) by default
# SCHEDULE_ALL = False

# Do you want to add a Mathjax config file?
# MATHJAX_CONFIG = ""

# If you want support for the $.$ syntax (which may conflict with running
# text!), just use this config:
# MATHJAX_CONFIG = """
# <script type="text/x-mathjax-config">
# MathJax.Hub.Config({
#     tex2jax: {
#         inlineMath: [ ['$','$'], ["\\\(","\\\)"] ],
#         displayMath: [ ['$$','$$'], ["\\\[","\\\]"] ],
#         processEscapes: true
#     },
#     displayAlign: 'center', // Change this to 'left' if you want left-aligned equations.
#     "HTML-CSS": {
#         styles: {'.MathJax_Display': {"margin": 0}}
#     }
# });
# </script>
# """

# Want to use KaTeX instead of MathJax? While KaTeX may not support every
# feature yet, it's faster and the output looks better.
# USE_KATEX = False

# KaTeX auto-render settings. If you want support for the $.$ syntax (which may
# conflict with running text!), just use this config:
# KATEX_AUTO_RENDER = """
# delimiters: [
#     {left: "$$", right: "$$", display: true},
#     {left: "\\\\[", right: "\\\\]", display: true},
#     {left: "\\\\begin{equation*}", right: "\\\\end{equation*}", display: true},
#     {left: "$", right: "$", display: false},
#     {left: "\\\\(", right: "\\\\)", display: false}
# ]
# """

# What Markdown extensions to enable?
# You will also get gist, nikola and podcast because those are
# done in the code, hope you don't mind ;-)
# Note: most Nikola-specific extensions are done via the Nikola plugin system,
#       with the MarkdownExtension class and should not be added here.
# Defaults are markdown.extensions.(fenced_code|codehilite|extra)
# markdown.extensions.meta is required for Markdown metadata.
MARKDOWN_EXTENSIONS = ['markdown.extensions.fenced_code', 'markdown.extensions.codehilite', 'markdown.extensions.extra']

# Options to be passed to markdown extensions (See https://python-markdown.github.io/reference/)
# Default is {} (no config at all)
# MARKDOWN_EXTENSION_CONFIGS = {}

# Social buttons. This is sample code for AddThis (which was the default for a
# long time). Insert anything you want here, or even make it empty (which is
# the default right now)
# (translatable)
# SOCIAL_BUTTONS_CODE = """
# <!-- Social buttons -->
# <div id="addthisbox" class="addthis_toolbox addthis_peekaboo_style addthis_default_style addthis_label_style addthis_32x32_style">
# <a class="addthis_button_more">Share</a>
# <ul><li><a class="addthis_button_facebook"></a>
# <li><a class="addthis_button_google_plusone_share"></a>
# <li><a class="addthis_button_linkedin"></a>
# <li><a class="addthis_button_twitter"></a>
# </ul>
# </div>
# <script src="https://s7.addthis.com/js/300/addthis_widget.js#pubid=ra-4f7088a56bb93798"></script>
# <!-- End of social buttons -->
# """

# Show link to source for the posts?
SHOW_SOURCELINK = False
# Copy the source files for your pages?
# Setting it to False implies SHOW_SOURCELINK = False
COPY_SOURCES = False

# Modify the number of Post per Index Page
# Defaults to 10
# INDEX_DISPLAY_POST_COUNT = 10

# Extra things you want in the pages HEAD tag. This will be added right
# before </head>
# (translatable)
# EXTRA_HEAD_DATA = ""
# Google Analytics or whatever else you use. Added to the bottom of <body>
# in the default template (base.tmpl).
# (translatable)
# BODY_END = ""

# Bundle JS and CSS into single files to make site loading faster in a HTTP/1.1
# environment but is not recommended for HTTP/2.0 when caching is used.
# Defaults to True.
# USE_BUNDLES = True
USE_BUNDLES = False

# Plugins you don't want to use. Be careful :-)
# DISABLED_PLUGINS = ["render_galleries"]

# Special settings to disable only parts of the indexes plugin.
# Use with care.
# DISABLE_INDEXES = False
# DISABLE_MAIN_ATOM_FEED = False
# DISABLE_MAIN_RSS_FEED = False

# Add the absolute paths to directories containing plugins to use them.
# For example, the `plugins` directory of your clone of the Nikola plugins
# repository.
# EXTRA_PLUGINS_DIRS = []

# Add the absolute paths to directories containing themes to use them.
# For example, the `v7` directory of your clone of the Nikola themes
# repository.
# EXTRA_THEMES_DIRS = []

# List of regular expressions, links matching them will always be considered
# valid by "nikola check -l"
# LINK_CHECK_WHITELIST = []

# The <hN> tags in HTML generated by certain compilers (reST/Markdown)
# will be demoted by that much (1 → h1 will become h2 and so on)
# This was a hidden feature of the Markdown and reST compilers in the
# past.  Useful especially if your post titles are in <h1> tags too, for
# example.
# (defaults to 1.)
# DEMOTE_HEADERS = 1

# If set to True, the tags 'draft', 'mathjax' and 'private' have special
# meaning. If set to False, these tags are handled like regular tags.
USE_TAG_METADATA = False

# If set to True, a warning is issued if one of the 'draft', 'mathjax'
# and 'private' tags are found in a post. Useful for checking that
# migration was successful.
WARN_ABOUT_TAG_METADATA = False

# Templates will use those filters, along with the defaults.
# Consult your engine's documentation on filters if you need help defining
# those.
# TEMPLATE_FILTERS = {}

# Put in global_context things you want available on all your templates.
# It can be anything, data, functions, modules, etc.
GLOBAL_CONTEXT = {}

# Add functions here and they will be called with template
# GLOBAL_CONTEXT as parameter when the template is about to be
# rendered
GLOBAL_CONTEXT_FILLER = []

# Settings for the (boot)Reveal theme must be added to the global context.
# subtheme selection:   beige/serif/simple/sky/night/default
# transition selection: cube/page/concave/linear/none/default
GLOBAL_CONTEXT.update({
    'subtheme': 'simple',
    'transition': 'none'
})
