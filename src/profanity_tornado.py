import tornado
from tornado import autoreload, ioloop, web, options, escape, websocket
import re
import json
from pattern.search import search, STRICT, Pattern, Constraint, taxonomy
from pattern.en import parsetree
import unicodedata
import datetime

profane_dict = dict()
re_dict = dict()

#Using Regular Expression
def re_compile(word_list):
	r = re.compile(r'\b(?:%s)\b' % '|'.join(word_list), re.IGNORECASE)
	return r

def codify_doc(doc, re_obj):
	doc = ''.join(c for c in unicodedata.normalize('NFD', doc) if unicodedata.category(c) != 'Mn')
	doc = doc.encode('ascii', errors='ignore')
	match = re_obj.search(doc)
	if match:
		return True
	else:
		return False

#Using Parse Tree
def pattern_compile(word_list):
	exp = ' | '.join(word_list)
	return exp

def codify_doc_pattern(doc, exp):
	doc = ''.join(c for c in unicodedata.normalize('NFD', doc) if unicodedata.category(c) != 'Mn')
	doc = doc.encode('ascii', errors='ignore')
	t = parsetree(doc, lemmata=True)

	# For greedy matching
	# match = search(exp,t)
	# For strict order matching
	match  = search(exp,t,STRICT)

	# match = search(exp,t, STRICT) 

	if match != []:
		return True
	else:
		return False

class WSHandler(websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
        self.write_message("Python Profanity Tester")
      
    def on_message(self, message):
    	message = json.loads(message)
    	client_id = message['client_id']
    	doc = message['doc']
    	exp = re_dict[client_id]

    	response = { 'client_id': client_id,
					'profane_code': codify_doc(doc, exp)
					# 'profane_code': codify_doc_pattern(doc, exp)
					}

        self.write_message(json.dumps(response))
 
    def on_close(self):
      print 'connection closed'


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class CodifyProfane(tornado.web.RequestHandler):
	def post(self):
		client_id = self.get_argument('client_id', '')
		doc = self.get_argument('doc', '')

		exp = re_dict[client_id]

		if client_id in profane_dict:
			response = { 'client_id': client_id,
						'profane_code': codify_doc(doc, exp)
						# 'profane_code': codify_doc_pattern(doc, exp)
						}
		else:
			response = "client not found"
		self.write(response)
	get = post

class ProfaneList(tornado.web.RequestHandler):
	def get(self):
		client_id = self.get_argument('client_id', '')
		if client_id in profane_dict:
			response = { 'client_id': client_id,
						'swear_dict': profane_dict[client_id]
						}
		else:
			response = { 'client_id': client_id,
						'swear_dict': 'Client id not present'
						}
		self.write(response)


class ProfaneListInit(tornado.web.RequestHandler):
	global profane_dict
	global re_dict
	def post(self):
		client_id = self.get_argument('client_id', '')
		profane_list = json.loads(self.get_argument('profane_list', ''))

		if client_id in profane_dict:
			self.write("Client ID exists, use update")
		else:
			profane_dict[client_id] ={
				'profane_list': profane_list
			}

			word_list = []
			for key,value in profane_list.iteritems():
				word_list.append(key)

			exp = re_compile(word_list)

			# exp = pattern_compile(word_list)
			re_dict[client_id] = exp


class ProfaneListUpdate(tornado.web.RequestHandler):
	def post(self):
		global profane_dict
		global re_dict
		client_id = self.get_argument('client_id', '')
		u_type = self.get_argument('u_type', '')
		term = self.get_argument('term', '')
		term = term.strip()
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
			# re_obj = pattern_compile(word_list)
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
