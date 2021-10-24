# NikolaBase Plugin utilities

import os
import re

removeStrangeChars   = re.compile(r"[\'\",\.\{\} \t\n\r]+")
removeMultipleDashes = re.compile(r"\-+")
removeLeadingDashes  = re.compile(r"^\-+")
removeTrailingDashes = re.compile(r"\-+$")

def author2urlBase(authorName) :
  authorFileName = authorName[:]
  authorFileName = removeStrangeChars.sub('-', authorFileName)
  authorFileName = removeMultipleDashes.sub('-', authorFileName)
  authorFileName = removeLeadingDashes.sub('', authorFileName)
  authorFileName = removeTrailingDashes.sub('', authorFileName)
  return f"author/{authorFileName[0:2]}/{authorFileName}"

def author2url(authorName) :
  return author2urlBase(authorName)+'.html'

removeLeadingDigitsWhiteSpace = re.compile(r"^[0-9]+[ \t]+")

def citation2refUrl(citeKey) :
  citeKeyLocal = removeLeadingDigitsWhiteSpace.sub('', citeKey)
  return f"{citeKeyLocal[0:2]}/{citeKeyLocal}"

def citation2urlBase(citeKey) :
  citeKeyLocal = removeLeadingDigitsWhiteSpace.sub('', citeKey)
  return "cite/" + citation2refUrl(citeKey)

def citation2url(citeKey) :
  return citation2urlBase(citeKey)+'.html'

def md2ext(aPath, ext) :
  aUrl = aPath
  pathStr = str(aPath)
  if pathStr.endswith('md') : aUrl = pathStr.removesuffix('md') + ext
  return aUrl

def md2html(aPath) :
  return md2ext(aPath, 'html')

def md2bib(aPath) :
  return md2ext(aPath, 'bib')

def md2lua(aPath) :
  return md2ext(aPath, 'lua')

def convertIndex2sortedList(anIndexDict) :
  indexList = list(anIndexDict.values())
  indexList.sort(key=lambda anIndexList : anIndexList[1])
  return indexList

def openEditorOn(aPath) :
  theEditor = 'nano'
  if 'EDITOR' in os.environ :
    theEditor = os.environ['EDITOR']
  os.system(f"{theEditor} {aPath}")
