import requests
import json
import datetime
from websocket import create_connection

#Initialization
print "\n Initialization API"
s = datetime.datetime.now()
json_data = open('../src/en_US.json')
profane_list = json.load(json_data)
post_data = { 'client_id': 'testdata', 'profane_list' : json.dumps(profane_list)} #A dictionary of your post data
r = requests.post('http://127.0.0.1:8888/profanity/initialize/', post_data)
print r.text
e = datetime.datetime.now()
d = e - s
print "Total time taken: ", d.total_seconds() * 1000

#Doc profane test
print "\n Test codification on : 'This is shit!'"
s = datetime.datetime.now()
post_data = { 'client_id': 'testdata', 'doc' : "This is shit!"} #A dictionary of your post data
r = requests.post('http://127.0.0.1:8888/profanity/codify/', post_data)
print r.text
resp = json.loads(r.text)
print "Profane code: ", resp['profane_code']
e = datetime.datetime.now()
d = e - s
print "Total time taken: ", d.total_seconds() * 1000


#Add term
print "\n Add term : 'Ole'"
s = datetime.datetime.now()
post_data = { 'client_id': 'testdata', 'u_type': 'add', 'term':'Ole'} #A dictionary of your post data
r = requests.post('http://127.0.0.1:8888/profanity/update/', post_data)
print r.text
e = datetime.datetime.now()
d = e - s
print "Total time taken: ", d.total_seconds() * 1000

#Doc profane test
print "\n Test codification on : 'This is ole!!!'"
s = datetime.datetime.now()
post_data = { 'client_id': 'testdata', 'doc' : "This is ole!!!"} #A dictionary of your post data
r = requests.post('http://127.0.0.1:8888/profanity/codify/', post_data)
print r.text
resp = json.loads(r.text)
print "Profane code: ", resp['profane_code']
e = datetime.datetime.now()
d = e - s
print "Total time taken: ", d.total_seconds() * 1000


#Remove term
print "\n Remove term : 'Ole'"
s = datetime.datetime.now()
post_data = { 'client_id': 'testdata', 'u_type': 'remove', 'term':'Ole'} #A dictionary of your post data
r = requests.post('http://127.0.0.1:8888/profanity/update/', post_data)
print r.text
e = datetime.datetime.now()
d = e - s
print "Total time taken: ", d.total_seconds() * 1000

#Doc profane test
print "\n Test codification on : 'This is ole!!!'"
s = datetime.datetime.now()
post_data = { 'client_id': 'testdata', 'doc' : "This is ole"} #A dictionary of your post data
r = requests.post('http://127.0.0.1:8888/profanity/codify/', post_data)
print r.text
resp = json.loads(r.text)
print "Profane code: ", resp['profane_code']
e = datetime.datetime.now()
d = e - s
print "Total time taken: ", d.total_seconds() * 1000

#websocket testing
print "\n Websocket test"
ws = create_connection("ws://localhost:8888/ws")
resp =  ws.recv()
print "Received '%s'" % resp

test_doc = { 'client_id': 'testdata', 'doc' : "This is ole"} 
print "\n Test codification on : 'This is ole'"
s = datetime.datetime.now()
ws.send(json.dumps(test_doc))
resp =  ws.recv()
print "Received '%s'" % resp
e = datetime.datetime.now()
d = e - s
print "Total time taken: ", d.total_seconds() * 1000

s = datetime.datetime.now()
test_doc = { 'client_id': 'testdata', 'doc' : "This is shit!"}
print "\n Test codification on : 'This is shit!'"
ws.send(json.dumps(test_doc))
resp =  ws.recv()
print "Received '%s'" % resp
e = datetime.datetime.now()
d = e - s
print "Total time taken: ", d.total_seconds() * 1000

ws.close()

