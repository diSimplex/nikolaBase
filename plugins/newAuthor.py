# -*- coding: utf-8 -*-

"""Create a new reference author."""

from pathlib import Path
import re
import sys
import yaml

from blinker import signal
from nikola.plugin_categories import Command
from nikola.utils import ask, ask_yesno
from plugins.utils import author2urlBase, openEditorOn

removeMultipleSpaces    = re.compile(r"\s+")
removeSpacesBeforeComma = re.compile(r"\s+\,")

def checkForAuthorSurname(surname) :
  possibleAuthors = list(Path('author').glob(f'*/*{surname}*'))
  if len(possibleAuthors) < 1 :
    return "new"

  possibleAuthors.sort()
  print("\nDo you want to use one of these existing authors?")
  anIndex = 1
  for anAuthor in possibleAuthors :
    print(f"{anIndex}: {anAuthor}")
    anIndex = anIndex + 1
  chosenIndex = ask("index (or return to add new author): ")
  try :
    chosenIndex = int(chosenIndex)
  except :
    chosenIndex = 0
  if 0 < chosenIndex and chosenIndex <= len(possibleAuthors) :
    return possibleAuthors[chosenIndex-1]
  return "new"

def askForAuthorDetails(surname) :
  firstName = ask("first name")
  vonPart   = ask("von part")
  jrPart    = ask("jr part")
  cleanName = [
    vonPart,
    surname,
    jrPart
  ]
  cleanName = " ".join(cleanName) + ', ' + firstName
  cleanName = removeMultipleSpaces.sub(" ", cleanName)
  cleanName = removeSpacesBeforeComma.sub(",", cleanName)

  authorPath = Path(author2urlBase(cleanName) + '.md')

  if not authorPath.exists() :
    authorPath.parent.mkdir(parents=True, exist_ok=True)
    with open(authorPath, 'w') as authorFile :
      authorFile.write(f"""---
title: {cleanName}
biblatex:
  cleanname: {cleanName}
  von:
  surname: {surname}
  jr: {jrPart}
  firstname: {firstName}
  email:
  institute:
  synonymOf: []
  url: []
---

""")
  return authorPath

def getAnAuthor() :
  surname = ask("Last name")

  if len(surname) < 1 :
    return None

  chosenAuthor = checkForAuthorSurname(surname)
  if chosenAuthor == "new" or not chosenAuthor.exists() :
    chosenAuthor = askForAuthorDetails(surname)
  return chosenAuthor

def authorPath2name(anAuthorPath) :
  if not anAuthorPath.exists() :
    print(f"Could not load the author file: {anAuthorPath}")
    sys.exit(-1)
  contents = ""
  with open(anAuthorPath) as authorFile :
    contents = authorFile.read()
  yamlFence = contents.find('---', 4)
  if yamlFence < 0 :
    print(f"Could not find yaml meta-data in author file: {anAuthorPath}")
    sys.exit(-1)
  yamlStr = contents[:yamlFence]
  try :
    metaData = yaml.safe_load(yamlStr)
  except Exception as err :
    print(f"Cound not parse yaml meta-data in author file: {anAuthorPath}")
    print(repr(err))
    sys.exit(-1)
  return metaData['title']

class CommandNewAuthor(Command) :
  """Create a new reference author."""

  name = "new_author"
  doc_usage = ""
  doc_purpose = "create a new reference author"

  def _execute(self, options, args) :
    """Create a new reference author."""
    chosenAuthor = getAnAuthor()
    if chosenAuthor is not None :
      openEditorOn(chosenAuthor)






