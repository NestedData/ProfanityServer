import re
import os
import unicodedata
from nltk import stem

from pymongo import MongoClient

porter = stem.porter.PorterStemmer()

# TODO: WHY IS IT CONNECTING TO THE WRONG DATABASE?!?!?!?!?!?
class Filter(object):
  MONGO_URL = os.environ['MONGO_URL'] if ('MONGO_URL' in os.environ) else "mongodb://localhost:27017/profanity"
  def __init__(self, filter_id, black_list=[], create=True):
    # declare instance variables
    self.filter_id = filter_id

    # initialize from the database
    self._create_db_connection()

    # create the necessary record to get started
    # if one doesn't exist for the filter_id
    client_doc = self._get_client_from_db()
    if not client_doc:
      if create:
        self._create_filter()
      else:
        raise Exception("No filter exists for filter_id: %s", self.filter_id)

    self.set_blacklist(black_list)

    self._update_from_db()

  def _get_collection(self, collection_name="filters"):
    return self.mongoclient.get_default_database()[collection_name]

  def _create_db_connection(self):
    self.mongoclient = MongoClient(self.MONGO_URL)

  def _create_filter(self):
    FiltersCollection = self._get_collection('filters')
    return FiltersCollection.insert({
      "filter_id": self.filter_id
    })

  def _get_client_from_db(self):
    FiltersCollection = self._get_collection('filters')
    return FiltersCollection.find_one({
      "filter_id": self.filter_id
    })

  def _update_from_db(self):
    # grab the necessary state from the db
    client_doc = self._get_client_from_db()
    print client_doc
    if client_doc is None:
      # if there isn't a client, bail
      raise Exception("Client doesn't exist for filter_id: %s" % self.filter_id)

    # if there is a client, set the values from the doc
    if not self._is_valid_blacklist(client_doc['black_list']):
      raise Exception("Blacklist was invalid")

    self.black_list = client_doc['black_list']

    # update calculated state once the data is loaded
    self._compile_blacklist_regex()

  def _store_to_db(self):
    # take the state of the object and write it to the db
    FiltersCollection = self._get_collection('filters')
    selector = {
      "filter_id": self.filter_id
    }
    modifier = {
      "$set": {
        "black_list": self.black_list
      }
    }
    FiltersCollection.update(selector, modifier)

  def _is_valid_blacklist(self, black_list):
    return isinstance(black_list, list)

  def _compile_blacklist_regex(self):
    # Q: do we want to return it or assign it or both
    r = re.compile(r'\b(?:%s)\b' % '|'.join(self.black_list), re.IGNORECASE)
    # exp = r'\b%s' % r'\b|'.join(self.black_list)
    # exp += r'\b'
    # r = re.compile(exp, re.IGNORECASE)
    self.regex = r

  # check if text is profane using regex
  def code_regex(self, text):
    #cleanup of doc
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    text = text.encode('ascii', errors='ignore')
    #stemming
    text = " ".join([porter.stem(i) for i in text.split()])

    match = self.regex.search(text)
    print text, self.regex, match
    
    if match:
      return True
    else:
      return False

  # returns boolean indicating success of update
  # false value indicates that the black_list was invalid
  def set_blacklist(self, black_list, store=True):
    valid = self._is_valid_blacklist(black_list)
    if valid:
      self.black_list = black_list
      if store:
        self._store_to_db()
    return valid

  # returns boolean indicating success of update
  # false value indicates that the black_list was invalid
  def add_to_blacklist(self, add_terms, store=True):
    print "=="
    print add_terms
    valid = self._is_valid_blacklist(add_terms)
    if valid:
      self.black_list.extend(add_terms)
      self._compile_blacklist_regex()
      if store:
        self._store_to_db()
    return valid

  # returns boolean indicating success of update
  # false value indicates that the black_list was invalid
  def remove_from_blacklist(self, remove_terms, store=True):
    valid = self._is_valid_blacklist(remove_terms)
    if valid:
      # remove the terms in remove_terms from black_list
      self.black_list = [term for term in self.black_list if term not in remove_terms]
      self._compile_blacklist_regex()
      if store:
        self._store_to_db()
    return valid

  # method to remove the filter from the db
  def destroy(self):
    FiltersCollection = self._get_collection('filters')
    FiltersCollection.remove({
      "filter_id": self.filter_id
    })

  def save(self):
    self._store_to_db()
