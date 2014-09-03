import re
import json
from pattern.search import search, STRICT
from pattern.en import parsetree
import unicodedata
import datetime

profane_dict = dict()
re_dict = dict()

class Filter(object):
  def __init__(self):
    # declare instance variables
    self.regex = None

  def _compile_regex(self, word_list):
    # Q: do we want to return it or assign it or both
  	exp = r'\b%s' % r'\b|'.join(word_list)
  	exp += r'\b'
  	r = re.compile(exp, re.IGNORECASE)
    self.regex = r
  	return r

  def code_regex(self, doc, regex):
    match = re_obj.search(doc)
    if match:
      return True
    else:
      return False

  def _compile_pattern(self, word_list):
    exp = '|'.join(word_list)
    self.pattern = exp
    return exp

#Using Regular Expression
def re_compile(word_list):
  exp = r'\b%s' % r'\b|'.join(word_list)
  exp += r'\b'
  return re.compile(exp, re.IGNORECASE)

def codify_doc(doc, re_obj):
	match = re_obj.search(doc)
	if match:
		return True
	else:
		return False

#Using Parse Tree
def pattern_compile(word_list):
	exp = '|'.join(word_list)
	return exp

def codify_doc_pattern(doc, exp):
	doc = ''.join(c for c in unicodedata.normalize('NFD', doc) if unicodedata.category(c) != 'Mn')
	doc = doc.encode('ascii', errors='ignore')
	t = parsetree(doc, lemmata=True, tags=False, chunks=False)

	# For greedy matching
	# match = search(exp,t)
	# For strict order matching
	match = search(exp,t, STRICT) 

	if match != []:
		return True
	else:
		return False



