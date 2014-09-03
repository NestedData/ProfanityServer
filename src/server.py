import tornado
from tornado import autoreload, ioloop, web, options, escape, websocket
import json
import unicodedata
import datetime

from .profanity import Filter

ProfanityFilters = {}

def getFilter(client_id):
  # creates the filter if it doesn't exist
  if client_id not in ProfanityFilters
    ProfanityFilters[client_id] = Filter(client_id)
  return ProfanityFilters[client_id]

class WSHandler(websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
        self.write_message("Python Profanity Tester")
      
    def on_message(self, message):
      message = json.loads(message)
      client_id = message['client_id']
      text = message['text']

      filter = getFilter(client_id)

      response = { 
        'client_id': client_id,
        'profane_code': filter.code_regex(text)
      }

      self.write_message(json.dumps(response))
 
    def on_close(self):
      print 'connection closed'


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class CodifyProfane(tornado.web.RequestHandler):
  def post(self):
    # require the vars. raise 400 if not present
    client_id = self.get_argument('client_id')
    text = self.get_argument('text')

    filter = getFilter(client_id)

    response = {
      'client_id': client_id,
      'profane_code': filter.code_regex(text)
    }

    self.write(response)
  get = post


class ProfaneList(tornado.web.RequestHandler):
  def get(self):
    # require client_id or raise 400
    client_id = self.get_argument('client_id')
    filter = getFilter(client_id)
    response = { 
      'client_id': client_id,
      'black_list': filter.black_list
    }
    self.write(response)


class ProfaneListInit(tornado.web.RequestHandler):
  def post(self):
    # require client_id and black_list or 400
    client_id = self.get_argument('client_id')
    black_list = self.get_argument('black_list')

    # load the black_list from json
    black_list = json.loads(black_list)

    filter = getFilter(client_id)
    filter.set_blacklist(black_list)

class ProfaneListUpdate(tornado.web.RequestHandler):
  def post(self):
    # require client_id or 400
    client_id = self.get_argument('client_id')

    u_type = self.get_argument('u_type', '')
    term = self.get_argument('term', '')

    if client_id in profane_dict:
      if u_type == 'add':
        if term not in profane_dict[client_id]['profane_list']:
          profane_dict[client_id]['profane_list'][term] = []
          r_str = "Term %s added" % term
          self.write(r_str)
        else:
          r_str = "Term %s exists" % term
          self.write(r_str)
      if u_type == 'remove':
        if term in profane_dict[client_id]['profane_list']:
          profane_dict[client_id]['profane_list'].pop(term, None)
          r_str = "Term %s removed" % term
          self.write(r_str)
        else:
          r_str = "Term %s not found" % term
          self.write(r_str)

      word_list = []
      for key,value in profane_dict[client_id]['profane_list'].iteritems():
        word_list.append(key)


      re_obj = re_compile(word_list)
      #re_obj = pattern_compile(word_list)
      re_dict[client_id] = re_obj

    else:
      self.write("Client does not exist")
  get = post



application = web.Application([
    (r"/", MainHandler),
    (r"/profanity/", ProfaneList),
    (r"/profanity/update/", ProfaneListUpdate),
    (r"/profanity/initialize/", ProfaneListInit),
    (r"/profanity/codify/", CodifyProfane),
    (r'/ws', WSHandler),
])

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = application
    app.listen(8888)
    ioloop = tornado.ioloop.IOLoop().instance()
    autoreload.start(ioloop)
    ioloop.start()
