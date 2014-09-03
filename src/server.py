import tornado
from tornado import autoreload, ioloop, web, options, escape, websocket
import json
import unicodedata
import datetime
from bson.objectid import ObjectId
from profanity import Filter

ProfanityFilters = {}

def getFilter(filter_id, create=True):
  # creates the filter if it doesn't exist
  if filter_id not in ProfanityFilters:
    if create:
      ProfanityFilters[filter_id] = Filter(filter_id)
    else:
      # if create is false and the filter doesn't exist, bail
      return None
  return ProfanityFilters[filter_id]

class WSHandler(websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
        self.write_message("Python Profanity Tester")
      
    def on_message(self, message):
      message = json.loads(message)
      filter_id = message['filter_id']
      text = message['text']

      filter = getFilter(filter_id)

      response = { 
        'filter_id': filter_id,
        'profane_code': filter.code_regex(text)
      }

      self.write_message(json.dumps(response))
 
    def on_close(self):
      print 'connection closed'


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class ClientFiltersInitHandler(tornado.web.RequestHandler):
  def post(self):
    # require filter_id and black_list or 400
    # we get filter_id from the request body because it doesn't exist yet.
    # this allows the client to specify it or it defaults to an ObjectId string.
    filter_id = self.get_argument('filter_id', str(ObjectId()))
    black_list = self.get_argument('black_list')

    # load the black_list from json
    black_list = json.loads(black_list)

    # creates the filter if it doesn't exist, returns None if it does
    filter = getFilter(filter_id, create=False)

    if filter:
      filter.set_blacklist(black_list)
      response = {
        "filter_id": filter_id 
      }
      self.write(response)
    else:
      response = {
        "error": "Filter already exists with this id."
      }
      self.write(response)


class ClientFiltersHandler(tornado.web.RequestHandler):
  # return the details of the filter
  def get(self, filter_id):
    filter = getFilter(filter_id)
    response = { 
      'filter_id': filter_id,
      'black_list': filter.black_list
    }
    self.write(response)

  # update the filter
  def put(self, filter_id):
    blacklist_changes = self.get_argument('black_list', json.dumps({}))
    blacklist_changes = json.loads(blacklist_changes)

    filter = getFilter(filter_id)

    # prevent hitting the db 3 times here
    editted = False
    if 'init' in blacklist_changes:
      filter.set_blacklist(blacklist_changes['init'], False)
      editted = True
    if 'remove' in blacklist_changes:
      filter.remove_from_blacklist(blacklist_changes['remove'])
      editted = True
    if 'add' in blacklist_changes:
      filter.add_to_blacklist(blacklist_changes['add'])
      editted = True

    if editted:
      filter.save()

    response = {
      'filter_id': filter_id,
      'black_list': filter.black_list
    }

    self.write(response)

  # remove the filter
  def delete(self, filter_id):
    filter = getFilter(filter_id)
    filter.destroy()

    response = {
      'filter_id': filter_id,
    }

    self.write(response)

class CodifyHandler(tornado.web.RequestHandler):
  def post(self, filter_id):
    # require the text. raise 400 if not present
    text = self.get_argument('text')

    filter = getFilter(filter_id)

    response = {
      'filter_id': filter_id,
      'profane_code': filter.code_regex(text)
    }

    self.write(response)
  get = post


application = web.Application([
    (r"/", MainHandler),
    (r"/filters", ClientFiltersInitHandler),
    (r"/filters/(TODO:ID_REGEX)", ClientFiltersHandler),
    (r"/filters/(TODO:ID_REGEX)/codify/", ClientFiltersCodifyHandler),
    (r'/ws', WSHandler),
])

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = application
    app.listen(8888)
    ioloop = tornado.ioloop.IOLoop().instance()
    autoreload.start(ioloop)
    ioloop.start()
