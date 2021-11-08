# -*- coding: utf-8 -*-

"""Create a new reference citation."""

from pathlib import Path
import sys
import yaml

from blinker import signal

from nikola.plugin_categories import Command
from nikola.utils import ask, ask_yesno
from plugins.utils import citation2urlBase, openEditorOn
from plugins.newAuthor import getAnAuthor, authorPath2name

citationNameFields = [
  'author', 'bookauthor', 'commentator',
  'editor', 'editora', 'editorb', 'editorc',
  'holder', 'translator'
]

def selectDocType() :
  docTypes = [ "owned", "public", "purchased", "uncatalogued", "unknown", "workingCopies"]
  anIndex = 1
  for aDocType in docTypes :
    print(f"{anIndex}: {aDocType}")
    anIndex = anIndex + 1
  chosenIndex = ask("index (or return for unknown)")
  try :
    chosenIndex = int(chosenIndex)
  except :
    chosenIndex = 5
  if 0 < chosenIndex and chosenIndex <= len(docTypes) :
    return docTypes[chosenIndex - 1]
  return "unknown"

def gatherNamesFor(aNameField) :
  print(f"\nGathering names for {aNameField}")
  names = [ ]
  while True :
    aName = getAnAuthor()
    if aName is None : return names
    openEditorOn(aName)
    names.append(authorPath2name(aName))

def askForCitationDetails(citeType, citeKey, citeOptions) :
  citeFields = [ 'docType' ]
  requiredFields = [ ]
  for aCiteField in citeOptions['requiredFields']:
    if aCiteField.find('[]') < 0 :
      citeFields.append(aCiteField)
      requiredFields.append(aCiteField)
  for aCiteField in citeOptions['usefulFields'] :
    if aCiteField.find('[]') < 0 :
      citeFields.append(aCiteField)
  citeFields.sort()
  requiredFields.sort()

  citation = { }

  citation['citekey']   = citeKey
  citation['docType']   = selectDocType()
  citation['entrytype'] = citeType

  for aNameField in citationNameFields :
    if aNameField in citeFields :
      names = gatherNamesFor(aNameField)
      if len(names) < 1 :
        citation[aNameField] = "[]"
      else :
        nameStrs = [ "" ]
        for aName in names :
          nameStrs.append(f"  - {aName}")
        citation[aNameField] = "\n".join(nameStrs)

  for aField in requiredFields :
    if aField not in citation :
      citation[aField] = ask(aField)

  for aField in citeFields :
    if aField not in citation :
      citation[aField] = ""

  if 'year-date' in citation :
    yearDate = citation['year-date']
    del citation['year-date']
    citeFields.remove('year-date')
    if -1 < yearDate.find('-') :
      citeFields.append('date')
      citation['date'] = yearDate
      citation['year'] = yearDate.split('-')
    else :
      citation['year'] = yearDate
    citeFields.append('year')
    citeFields.sort()

  titleFields = [ 'title' ]
  for aTitleField in titleFields :
    if aTitleField in citation :
      citation[aTitleField] = f"\"{citation[aTitleField]}\""

  citationPath = Path(citation2urlBase(citeKey)+'.md')
  if not citationPath.exists() :
    with open(citationPath, 'w') as cFile :
      cFile.write("---\n")
      cFile.write("title: {}\n".format(citation['title']))
      cFile.write("biblatex:\n")
      for aField in citeFields :
        if aField in citation :
          cFile.write(" {}: {}\n".format(aField, citation[aField]))
      cFile.write("---\n\n")
  return citationPath

def checkForCitation(citeKey) :
  possibleCitations = list(Path("cite").glob(f"*/*{citeKey[0:5]}*"))
  if len(possibleCitations) < 1 :
    return "new"

  possibleCitations.sort()
  print("\nDo you want to use one of these existing citations?")
  anIndex = 1
  for aCitation in possibleCitations :
    print(f"{anIndex}: {aCitation}")
    anIndex = anIndex + 1
  chosenIndex = ask("index (or return to add new citation)")
  try :
    chosenIndex = int(chosenIndex)
  except :
    chosenIndex = 0
  if 0 < chosenIndex and chosenIndex <= len(possibleCitations) :
    return possibleCitations[chosenIndex - 1]
  return "new"

def getACitation(citeType, citeOptions) :
  citeKey = ask("citekey")
  chosenCitation = checkForCitation(citeKey)
  if chosenCitation == "new" or not chosenCitation.exists() :
    chosenCitation = askForCitationDetails(citeType, citeKey, citeOptions)
  return chosenCitation

def checkCiteType(args, biblatexTypes) :
  citeType = "unknown"
  if 0 < len(args) : citeType = args[0]
  if citeType not in biblatexTypes :
    citeTypes = list(biblatexTypes.keys())
    citeTypes.sort()
    print("\nPlease choose one of the following citation types;")
    for aCiteType in citeTypes :
      aliases = ""
      if 'aliases' in biblatexTypes[aCiteType] and \
        biblatexTypes[aCiteType]['aliases'] is not None :
        aliases = biblatexTypes[aCiteType]['aliases']
      print(f"  {aCiteType} {aliases}")
    sys.exit(-1)
  return citeType

class CommandNewCite(Command) :
  """Create a new reference citation."""

  name = "new_cite"
  doc_usage = "[options] citeType"
  doc_purpose = "create a new reference citation"

  def _execute(self, options, args) :
    """Create a new reference citation."""

    with open('data/biblatexTypes.yml') as biblatexFile :
      biblatexTypes = yaml.safe_load(biblatexFile.read())

    citeType = checkCiteType(args, biblatexTypes)

    chosenCitation = getACitation(citeType, biblatexTypes[citeType])
    if chosenCitation is not None :
      openEditorOn(chosenCitation)
