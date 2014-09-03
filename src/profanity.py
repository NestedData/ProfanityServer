import re
import os

from pymongo import MongoClient

class Filter(object):
  MONGO_URL = os.environ['MONGO_URL'] or "mongodb://localhost:27017/profanity"

  def __init__(self, client_id, create=True):
    # declare instance variables
    self.client_id = client_id

    # initialize from the database
    self._create_db_connection()

    # create the necessary record to get started
    # if one doesn't exist for the client_id
    client_doc = self._get_client_from_db()
    if not client_doc:
      if create
        self._create_filter()
      else
        raise Exception("No filter exists for client_id: %s", self.client_id)


    self._update_from_db()

  def _get_collection(self, collection_name="clients"):
    return self.MongoClient.db[collection_name]

  def _create_db_connection(self, client_id):
    self.mongoclient = MongoClient(self.MONGO_URL)

  def _create_filter(self):
    ClientsCollection = self._get_collection('clients')
    return ClientsCollection.insert({
      "client_id": self.client_id
    })

  def _get_client_from_db(self):
    ClientsCollection = self._get_collection('clients')
    return ClientsCollection.find_one({
      "client_id": self.client_id
    })

  def _update_from_db(self):
    # grab the necessary state from the db
    client_doc = self._get_client_from_db()
    
    if client_doc is None:
      # if there isn't a client, bail
      raise Exception("Client doesn't exist for client_id: %s" % self.client_id)

    # if there is a client, set the values from the doc
    if not self._is_valid_blacklist(client_doc.black_list):
      raise Exception("Blacklist was invalid")

    self.black_list = client_doc.black_list

    # update calculated state once the data is loaded
    self._compile_blacklist_regex()

  def _store_to_db(self):
    # take the state of the object and write it to the db
    ClientsCollection = self._get_collection('clients')
    selector = {
      "client_id": self.client_id
    }
    modifier = {
      "$set": {
        "black_list": self.black_list
      }
    }
    ClientsCollection.update(selector, modifier)

  def _is_valid_blacklist(self, black_list):
    return isinstance(black_list, list)

  def _compile_blacklist_regex(self):
    # Q: do we want to return it or assign it or both
  	exp = r'\b%s' % r'\b|'.join(self.black_list)
  	exp += r'\b'
  	r = re.compile(exp, re.IGNORECASE)
    self.regex = r

  # check if text is profane using regex
  def code_regex(self, text):
    match = self.regex.search(text)
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
      if store
        self._store_to_db()
    return valid

  # returns boolean indicating success of update
  # false value indicates that the black_list was invalid
  def add_to_blacklist(self, add_terms, store=True):
    valid = self._is_valid_blacklist(add_terms)
    if valid:
      self.black_list.extend(add_terms)
      if store
        self._store_to_db()
    return valid

  # returns boolean indicating success of update
  # false value indicates that the black_list was invalid
  def remove_from_blacklist(self, remove_terms, store=True):
    valid = self._is_valid_blacklist(remove_terms)
    if valid:
      # remove the terms in remove_terms from black_list
      self.black_list = [term for term in self.black_list if term not in remove_terms]
      if store
        self._store_to_db()
    return valid

  # method to remove the filter from the db
  def destroy(self):
    ClientsCollection = self._get_collection('clients')
    ClientsCollection.remove({
      "client_id": self.client_id
    })

  def save(self):
    self._store_to_db()
