# -*- coding: utf-8 -*-

"""Apply any monkey patches to Nikola (HERE BE DRAGONS!)."""

import yaml

from blinker import signal

from nikola.plugin_categories import SignalHandler
from nikola.utils import LOGGER

class MonkeyPatches(SignalHandler) :
  """Apply any monkey patches to Nikola (HERE BE DRAGONS!)."""

  name = "monkey_patches"

  def doTheMonkeyPatches(self, site) :
    LOGGER.debug("Time to DO the monkey patches!")
    for plugin_info in site.plugin_manager.getPluginsOfCategory("Taxonomy") :
      if plugin_info.name == 'classify_indexes' :
        if 'THIS_IS_A_BLOG_SITE' not in site.config :
          plugin_info.plugin_object.apply_to_posts = False
          plugin_info.plugin_object.apply_to_pages = True
          plugin_info.plugin_object.template_for_single_list = 'pageIndex.tmpl'

  def preGenerateClassificationPage(self, context) :
    """We resort the list of posts in title order given the
     context = {
      'site': self.site,
      'taxonomy': taxonomy,
      'classification': classification,
      'lang': lang,
      'posts': filtered_posts,
      'context': context,
      'kw': kw,
    }"""
    if 'pagekind' in context['context'] :
      if 'main_index' in context['context']['pagekind'] :
        context['posts'].sort(key=lambda aPost: aPost.title())

  def set_site(self, site) :
    configured = signal('configured')
    configured.connect(self.doTheMonkeyPatches)

    genClassificationPage = signal('generate_classification_page')
    genClassificationPage.connect(self.preGenerateClassificationPage)

