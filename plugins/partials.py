# -*- coding: utf-8 -*-

"""Create html server side include partials in the output."""

import os
from pathlib import Path
import yaml

from nikola.plugin_categories import Task
from nikola.utils import \
  LocaleBorg, get_theme_path_real, config_changed, LOGGER

class RenderPartials(Task) :
  """Create html server side include partials in the output."""

  name = "render_partials"

  def gen_tasks(self) :
    """Build html server side include partials from metadata and HTML
    fragments."""

    if 'RENDER_DISIMPLEX_THEME_PARTIALS' not in self.site.config :
      yield {
        'name'     : 'DoNothing',
        'basename' : self.name,
        'targets'  : [ ],
        'actions'  : [ ]
      }

    else :

      diSimpThemeName = 'disimplex'
      diSimpThemeDir = Path(
        get_theme_path_real(diSimpThemeName, self.site.themes_dirs)
      )

      lang = LocaleBorg().current_lang

      # Adapted from Nikola:generic_renderer
      #
      depsDict = {}
      depsDict['OUTPUT_FOLDER'] = self.site.config['OUTPUT_FOLDER']
      depsDict['TRANSLATIONS'] = self.site.config['TRANSLATIONS']
      depsDict['global'] = self.site.GLOBAL_CONTEXT
      depsDict['all_page_deps'] = self.site.ALL_PAGE_DEPS
      for k, v in self.site.GLOBAL_CONTEXT['template_hooks'].items():
        depsDict['||template_hooks|{0}||'.format(k)] = v.calculate_deps()
      for k in self.site._GLOBAL_CONTEXT_TRANSLATABLE:
        depsDict[k] = depsDict['global'][k](lang)
      for k in self.site._ALL_PAGE_DEPS_TRANSLATABLE:
        depsDict[k] = depsDict['all_page_deps'][k](lang)
      depsDict['navigation_links'] = depsDict['global']['navigation_links'](lang)
      depsDict['navigation_alt_links'] = depsDict['global']['navigation_alt_links'](lang)

      for aPartial in diSimpThemeDir.glob('**/*.partial.tmpl') :
        print(f"Updating partial: {aPartial}")
        outputName = os.path.join(
          self.site.config['OUTPUT_FOLDER'],
          'partials',
          aPartial.name.replace('partial.tmpl', 'html')
        )
        templateName = aPartial.name
        fileDeps     = self.site.template_system.template_deps(templateName)
        #
        # Adapted from Nikola.generic_renderer and Nikola.render_template
        #
        yield {
          'name'     : os.path.normpath(outputName),
          'basename' : self.name,
          'targets'  : [ outputName ],
          'file_dep' : fileDeps,
          'actions'  : [ (self.site.render_template, [
              templateName, outputName,
              { 'lang': lang, 'permalink': '/', 'has_custom_css': True },
              None, True ]) ],
          'clean'    : True,
          'uptodate' : [config_changed(depsDict, 'render_partials.gen_tasks')]
        }
