# -*- coding: utf-8 -*-

"""Add the Reveal.js specific short codes"""

import yaml

from nikola.plugin_categories import ShortcodePlugin
from nikola.utils import LOGGER

revealCodes = {
  "start"     : "<div class=\"reveal\" style=\"width:100%;height:75vh\"><div class=\"slides\"><section>",
  "startSub"  : "<section>",
  "new"       : "</section> <section>",
  "finishSub" : "</section>",
  "finish"    : "</section></div></div>"
}

class RevealShortCodes(ShortcodePlugin) :
  """Add the Reveal.js specific short codes"""

  name = "reveal"

  def handler(self, rCode, **_options) :
    if rCode in revealCodes :
      return revealCodes[rCode]

    LOGGER.warning('Unknown reveal code: [{}]'.format(rCode))
    return ""
