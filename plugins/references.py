# -*- coding: utf-8 -*-

"""Render the author/citeations from a simple reference database."""

import os
import msgpack
from pathlib import Path
import re
import sys
import yaml

from nikola.plugin_categories import Task
from nikola.utils import \
  LocaleBorg, get_theme_path_real, config_changed, LOGGER
from plugins.utils import \
  author2urlBase, md2html, md2bib, md2lua, convertIndex2sortedList, \
  author2url, citation2urlBase, citation2refUrl

class RenderReferences(Task) :
  """Render the author/citeations from a simple reference database."""

  #humanReadableDB = True
  humanReadableDB = False

  name = "render_references"

  def author2path(self, authorName) :
    authorPath = author2urlBase(authorName)+'.md'
    if authorPath not in self.filesDB :
      if authorPath in self.authorAliases :
        authorPath = self.authorAliases[authorPath]
    return authorPath

  def loadDatabase(self) :
    self.showProgress = False
    print("Loading refs database")
    refsDB = { }
    authorAliases = { }
    try :
      with open('authorAliases.yaml') as aliasesFile :
        authorAliases = yaml.safe_load(aliasesFile)

      if self.humanReadableDB :
        refsDBPath = os.path.join(self.site.config['CACHE_FOLDER'], "refsDB.yaml")
        with open(refsDBPath, 'r') as refsDBFile :
          refsDB = yaml.safe_load(refsDBFile)
      else :
        refsDBPath = os.path.join(self.site.config['CACHE_FOLDER'], "refsDB.msgpack")
        with open(refsDBPath, 'rb') as refsDBFile :
          refsDB = msgpack.unpackb(refsDBFile.read())
    except FileNotFoundError :
      LOGGER.warning("No cached version of the references database found")
      LOGGER.warning("Rebuilding from scratch...")
      self.showProgress = True
    except Exception as err :
      LOGGER.error("Could not load cached version of the references database")
      LOGGER.error(repr(err))

    if refsDB is None : refsDB = { }
    self.refsDB = refsDB

    if authorAliases is None : authorAliases = { }
    self.authorAliases = authorAliases

    if 'files' not in self.refsDB : self.refsDB['files'] = { }
    self.filesDB = self.refsDB['files']
    self.missingAuthors = { }
    self.changedFiles   = { }
    print("Loaded  refs database")

  def saveDatabase(self) :
    print("Saving refs database")

    try :
      if self.humanReadableDB :
        refsDBPath = os.path.join(self.site.config['CACHE_FOLDER'], "refsDB.yaml")
        with open(refsDBPath, 'w') as refsDBFile :
          refsDBFile.write(yaml.dump(self.refsDB))
      else :
        refsDBPath = os.path.join(self.site.config['CACHE_FOLDER'], "refsDB.msgpack")
        with open(refsDBPath, 'wb') as refsDBFile :
          refsDBFile.write(msgpack.packb(self.refsDB))
    except Exception as err :
      LOGGER.error("Could not save references database in cache")
      LOGGER.error(repr(err))
      # Something went wrong... so try and find out which file contains
      # the offending field...
      for aPath, aValue in self.filesDB.items() :
        print("serializing: {}".format(aPath))
        try :
          msgpack.packb(aValue)
        except Exception as err :
          print(repr(err))
          print(yaml.dump(aValue))
          for aKey, aVal in aValue['biblatex'].items() :
            print("{}: {} ({})".format(aKey, type(aVal), aVal))
    print("Saved  refs database")

  def addFile(self, aPath) :
    self.filesDB[str(aPath)] = {
      'mtime'      : 0,
      'size'       : 0,
      'meta'       : { },
      'biblatex'   : { },
      'papersDict' : { },
      'body'       : "",
      'indexDict'  : { }
    }

  def fileHasChanged(self, aPath) :
    aPathStr = str(aPath)
    aPathStat = aPath.stat()

    outputPath = os.path.join(
        self.site.config['OUTPUT_FOLDER'],
        str(aPath).removesuffix('md') + 'html'
      )
    if not os.path.exists(outputPath) :
      print(outputPath)
      self.changedFiles[aPathStr] = True

    if aPathStr not in self.filesDB :
      self.addFile(aPathStr)
      self.changedFiles[aPathStr] = True

    aRef = self.filesDB[aPathStr]
    if aRef['size'] != aPathStat.st_size :
      aRef['size'] = aPathStat.st_size
      self.changedFiles[aPathStr] = True

    if aRef['mtime'] != aPathStat.st_mtime :
      aRef['mtime'] = aPathStat.st_mtime
      self.changedFiles[aPathStr] = True

    return aPathStr in self.changedFiles

  def updateMetaData(self, aPath) :
    aPathStr = str(aPath)
    contents = aPath.read_text()
    yamlFence = contents.find('---', 4)
    body = ""
    meta = { 'biblatex' : { } }
    if -1 < yamlFence :
      bodyText = contents[yamlFence+3:]
      metaYaml = contents[:yamlFence]
      try :
        meta = yaml.safe_load(metaYaml)
      except Exception as err :
        LOGGER.error("Could not load the yaml metadata for [{}]".format(aPath))
        LOGGER.error(repr(err))
    biblatex = meta['biblatex']
    del meta['biblatex']
    if 'urldate' in biblatex and biblatex['urldate'] is not None :
      biblatex['urldate'] = str(biblatex['urldate'])
    if 'date' in biblatex and biblatex['date'] is not None :
      biblatex['date'] = str(biblatex['date'])
    if 'year' in biblatex and biblatex['year'] is not None :
      biblatex['year'] = str(biblatex['year'])
    if 'url' in biblatex and isinstance(biblatex['url'], str) :
      biblatex['url'] = [ biblatex['url'] ]

    aRef             = self.filesDB[aPathStr]
    aRef['bodyText'] = bodyText
    refMeta          = aRef['meta']
    refBiblatex      = aRef['biblatex']
    for key, value in meta.items() :
      if key not in refMeta :
        self.changedFiles[aPathStr] = True
        refMeta[key] = value
      elif value != refMeta[key] :
        self.changedFiles[aPathStr] = True
        refMeta[key] = value

    for key, value in biblatex.items() :
      if key not in refBiblatex :
        self.changedFiles[aPathStr] = True
        refBiblatex[key] = value
      elif value != refBiblatex[key] :
        self.changedFiles[aPathStr] = True
        refBiblatex[key] = value

  def addCitationCrossRefs(self, aCitation) :
    citationStr = str(aCitation)
    cBiblatex   = self.filesDB[citationStr]['biblatex']
    biblatexPeople = ['author', 'bookauthor', 'commentator',
      'editor', 'editora', 'editorb', 'editorc', 'author-editor',
      'holder', 'translator']
    for aPersonKey in  biblatexPeople :
      if aPersonKey in cBiblatex :
        if isinstance(cBiblatex[aPersonKey], str) :
          cBiblatex[aPersonKey] = [ cBiblatex[aPersonKey] ]
        for aPerson in cBiblatex[aPersonKey] :
          anAuthorStr = self.author2path(aPerson)
          if anAuthorStr not in self.filesDB :
            self.missingAuthors[anAuthorStr] = True
            self.addFile(anAuthorStr)
          anAuthorPapers = self.filesDB[anAuthorStr]['papersDict']
          aCitationStr = str(aCitation)
          if aCitationStr not in anAuthorPapers :
            self.changedFiles[anAuthorStr] = True
            anAuthorPapers[aCitationStr] = [
              md2html(aCitationStr),
              "{} {}".format(
                cBiblatex['year'],
                aCitation.name.removesuffix('md')
              ),
              cBiblatex['title']
            ]

  def updateIndex(self, aPath) :

    filesDB = self.filesDB
    changedFiles = self.changedFiles

    pathSegments = str(aPath).split(os.path.sep)
    indexType  = pathSegments[0]
    minorIndex = pathSegments[1]
    majorIndex = minorIndex[0]

    typeIndexPath   = os.path.join(indexType, 'index.html')
    typeIndexCache  = os.path.join('cache', typeIndexPath)
    minorIndexPath  = os.path.join(indexType, minorIndex, 'index.html')
    minorIndexCache = os.path.join('cache', minorIndexPath)
    majorIndexPath  = os.path.join(indexType, f"{majorIndex}-index.html")
    majorIndexCache = os.path.join('cache', majorIndexPath)

    if typeIndexCache not in filesDB :
      self.addFile(typeIndexCache)
      changedFiles[typeIndexCache] = True
    if majorIndexPath not in filesDB[typeIndexCache] :
      filesDB[typeIndexCache]['indexDict'][majorIndexPath] = [
        majorIndexPath,
        majorIndex
      ]
      filesDB[typeIndexCache]['meta']['title'] = indexType
      changedFiles[typeIndexCache] = True

    if majorIndexCache not in filesDB :
      self.addFile(majorIndexCache)
      changedFiles[majorIndexCache] = True
    filesDB[majorIndexCache]['rootIndexPath'] = typeIndexPath
    if minorIndexPath not in filesDB[majorIndexCache] :
      filesDB[majorIndexCache]['indexDict'][minorIndexPath] = [
        minorIndexPath,
        minorIndex
      ]
      filesDB[majorIndexCache]['meta']['title'] = majorIndex
      changedFiles[majorIndexCache] = True

    if minorIndexCache not in filesDB :
      self.addFile(minorIndexCache)
      changedFiles[minorIndexCache] = True
    filesDB[minorIndexCache]['rootIndexPath'] = typeIndexPath
    filesDB[minorIndexCache]['subIndexPath'] = majorIndexPath
    aPathStr = str(aPath)
    if aPathStr not in filesDB[minorIndexCache] :
      links = [ filesDB[aPathStr]['meta']['title'] ]
      if aPathStr.startswith('cite') :
        citeLink = "{} {}".format(
          filesDB[aPathStr]['biblatex']['year'],
          aPath.name.removesuffix('.md')
        )
        links.insert(0, citeLink)
      links.insert(0, aPathStr)
      filesDB[minorIndexCache]['indexDict'][aPathStr] = links
      filesDB[minorIndexCache]['meta']['title'] = minorIndex
      changedFiles[minorIndexCache] = True

  def reBuildDatabase(self) :
    self.loadDatabase()
    self.authors   = []
    self.citations = []

    authorsDir   = Path('author')
    citationsDir = Path('cite')

    print("Checking authors")
    authorsList = list(authorsDir.glob("**/*.md"))
    authorsList.sort()
    for anAuthor in authorsList :
      if self.showProgress : print("  {}".format(anAuthor))
      if self.fileHasChanged(anAuthor) :
        self.updateMetaData(anAuthor)
        self.updateIndex(anAuthor)

    print("Checking citations")
    citationsList = list(citationsDir.glob("**/*.md"))
    citationsList.sort()
    for aCitation in citationsList :
      if self.showProgress : print("  {}".format(aCitation))
      if self.fileHasChanged(aCitation) :
        self.updateMetaData(aCitation)
        self.addCitationCrossRefs(aCitation)
        self.changedFiles[md2bib(aCitation)] = True
        self.changedFiles[md2lua(aCitation)] = True
        self.updateIndex(aCitation)

    #print("----------------------------------------------------")
    #print("CHANGED: ")
    #changedFiles = list(self.changedFiles.keys())
    #if changedFiles is None : changedFiles = []
    #changedFiles.sort()
    #for aPath in changedFiles :
    #  print(aPath)
    missingAuthors = list(self.missingAuthors.keys())
    if missingAuthors is not None and 0 < len(missingAuthors) :
      print("----------------------------------------------------")
      print("MISSING AUTHORS: ")
      missingAuthors.sort()
      for aPath in missingAuthors :
        print(aPath)
      print("PLEASE FIX THESE Authors!")
      print("----------------------------------------------------")
      sys.exit(-1)

    self.saveDatabase()


  def renderARefsTemplate(self, templateName, context, outputName, isAFragment) :
    # Adapted from Nikola.generic_renderer and Nikola.render_template

    print("------------------------------------------")
    print("rendering: {} to {}".format(templateName, outputName))
    #print("------------------------------------------")
    #print(yaml.dump(context))
    #print("------------------------------------------")
    context['lang']           = LocaleBorg().current_lang
    context['permalink']      =  '/'
    context['has_custom_css'] = True
    context['description']    = "silly description"
    context['title']          = context['meta']['title']
    #print(yaml.dump(context))

    # Add our filters
    context['md2html']          = md2html
    context['author2url']       = author2url
    context['citation2refUrl']  = citation2refUrl
    context['citation2urlBase'] = citation2urlBase
    context['yamlDump']         = yaml.dump

    if os.path.exists(outputName) : os.unlink(outputName)

    fileDeps = self.site.template_system.template_deps(templateName)
    #print(yaml.dump(fileDeps))

    return {
      'name'     : os.path.normpath(outputName),
      'basename' : self.name,
      'targets'  : [ outputName ],
      'file_dep' : fileDeps,
      'actions'  : [ (self.site.render_template, [
          templateName, outputName, context, None, isAFragment
      ]) ],
      'clean'    : True,
      'uptodate' : [
        config_changed(self.refsDepsDict, 'render_references.gen_tasks')
      ]
    }

  def renderAnAuthor(self, aPath) :
    context = self.filesDB[aPath]
    context['papers'] = convertIndex2sortedList(context['papersDict'])
    return self.renderARefsTemplate(
      'refsAuthor.tmpl',
      context,
      os.path.join(
        self.site.config['OUTPUT_FOLDER'],
        aPath.removesuffix('md') + 'html'
      ),
      False
    )

  def renderAnIndex(self, aPath) :
    context = self.filesDB[aPath]
    if 'rootIndexPath' not in context :
      context['rootIndex'] = [ ]
    else :
      rootIndex = os.path.join('cache', context['rootIndexPath'])
      if  rootIndex in self.filesDB :
        context['rootIndex'] = convertIndex2sortedList(
          self.filesDB[rootIndex]['indexDict']
        )
    if 'subIndexPath' not in context :
      context['subIndex'] = [ ]
    else:
      subIndex = os.path.join('cache', context['subIndexPath'])
      if  subIndex in self.filesDB :
        context['subIndex'] = convertIndex2sortedList(
          self.filesDB[subIndex]['indexDict']
        )
    if 'indexDict' not in context :
      context['index'] = [ ]
    else :
      context['index'] = convertIndex2sortedList(
        context['indexDict']
      )
    return self.renderARefsTemplate(
      'refsIndex.tmpl',
      context,
      os.path.join(
        self.site.config['OUTPUT_FOLDER'],
        aPath.removeprefix('cache/')
      ),
      False
    )

  def renderABiblatex(self, aPath) :
    basePath = aPath.removesuffix('bib')
    context  = self.filesDB[basePath+'md']
    return self.renderARefsTemplate(
      'refsBiblatex.tmpl',
      context,
      os.path.join(self.site.config['OUTPUT_FOLDER'], aPath),
      True
    )

  def renderABibContext(self, aPath) :
    basePath = aPath.removesuffix('lua')
    context  = self.filesDB[basePath+'md']
    return self.renderARefsTemplate(
      'refsBibContext.tmpl',
      context,
      os.path.join(self.site.config['OUTPUT_FOLDER'], aPath),
      True
    )

  def renderACitation(self, aPath) :
    basePath = aPath.removesuffix('md')
    context  = self.filesDB[aPath]
    context['biblatexUrl']   = basePath + 'bib'
    context['bibcontextUrl'] = basePath + 'lua'
    biblatex = context['biblatex']
    if 'docType' not in biblatex : biblatex['docType'] = None
    return self.renderARefsTemplate(
      'refsCitation.tmpl',
      context,
      os.path.join(self.site.config['OUTPUT_FOLDER'], basePath + 'html'),
      False
    )

  def gen_tasks(self) :
    """Build html server side include partials from metadata and HTML
    fragments."""

    # We implement our own scan of the reference database (authors and
    # citations) this means that we do *not* want to follow the
    # instructions in:
    #
    #  https://getnikola.com/internals.html#posts-and-pages
    #
    #self.site.scan_posts()

    yield {
      'name'     : 'DoNothing',
      'basename' : self.name,
      'targets'  : [ ],
      'actions'  : [ ]
    }

    if 'THIS_IS_A_REFERENCES_SITE' in self.site.config :

      print("Hello from render_references!")
      self.reBuildDatabase()

      # Adapted from Nikola:generic_renderer
      #
      lang = LocaleBorg().current_lang
      refsDepsDict = {}
      refsDepsDict['OUTPUT_FOLDER'] = self.site.config['OUTPUT_FOLDER']
      refsDepsDict['TRANSLATIONS'] = self.site.config['TRANSLATIONS']
      refsDepsDict['global'] = self.site.GLOBAL_CONTEXT
      refsDepsDict['all_page_deps'] = self.site.ALL_PAGE_DEPS
      for k, v in self.site.GLOBAL_CONTEXT['template_hooks'].items():
        refsDepsDict['||template_hooks|{0}||'.format(k)] = v.calculate_deps()
      for k in self.site._GLOBAL_CONTEXT_TRANSLATABLE:
        refsDepsDict[k] = refsDepsDict['global'][k](lang)
      for k in self.site._ALL_PAGE_DEPS_TRANSLATABLE:
        refsDepsDict[k] = refsDepsDict['all_page_deps'][k](lang)
      refsDepsDict['navigation_links'] = refsDepsDict['global']['navigation_links'](lang)
      refsDepsDict['navigation_alt_links'] = refsDepsDict['global']['navigation_alt_links'](lang)
      self.refsDepsDict = refsDepsDict

      changedFiles = list(self.changedFiles.keys())
      if changedFiles is None : changedFiles = [ ]
      changedFiles.sort()
      for aPath in changedFiles :
        if aPath.startswith('author') :
          aTask = self.renderAnAuthor(aPath)
        elif aPath.startswith('cache') :
          aTask = self.renderAnIndex(aPath)
        elif aPath.startswith('cite') :
          if aPath.endswith('bib') :
            aTask = self.renderABiblatex(aPath)
          elif aPath.endswith('lua') :
            aTask = self.renderABibContext(aPath)
          else :
            aTask = self.renderACitation(aPath)
        else :
          LOGGER.error("An unknown type of changed path:")
          LOGGER.error(aPath)
          aTask = {
            'name'     : 'DoNothing',
            'basename' : self.name,
            'targets'  : [ ],
            'actions'  : [ ]
          }
        yield aTask

    print("=====================================================")
