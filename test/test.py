import requests
import json
import datetime
from websocket import create_connection

BASE_HTTP_URL = "http://localhost:8888"
FILTER_ID = "testdata"
# don't time the inflation from the file
json_data = open('../src/en_US.json')
profane_list = json.load(json_data)

#Initialization - create a filter and set it's blacklist
print "\n Initialization API"
s = datetime.datetime.now()
post_data = { 'filter_id': FILTER_ID, 'black_list' : json.dumps(profane_list)} #A dictionary of your post data
r = requests.post('{0}/filters'.format(BASE_HTTP_URL), post_data)
# print r.text
e = datetime.datetime.now()
d = e - s
print "Total time taken: ", d.total_seconds() * 1000

#Doc profane test
print "\n Test codification on : 'This is shit!'"
s = datetime.datetime.now()
post_data = { 'filter_id': FILTER_ID, 'text' : "This is shit!"} #A dictionary of your post data
r = requests.post('{0}/filters/{1}/codify/'.format(BASE_HTTP_URL, FILTER_ID), post_data)
# print r.text
resp = json.loads(r.text)
print "Profane code: ", resp['profane_code']
e = datetime.datetime.now()
d = e - s
print "Total time taken: ", d.total_seconds() * 1000


#Add term
print "\n Add term : 'apple, ole'"
s = datetime.datetime.now()
post_data = { 
  'filter_id': FILTER_ID,
  'black_list': {
    'add': ["apple", "ole"]
  }
}
r = requests.put('{0}/filters/{1}'.format(BASE_HTTP_URL, FILTER_ID), data=json.dumps(post_data))
# print r.text
e = datetime.datetime.now()
d = e - s
print "Total time taken: ", d.total_seconds() * 1000

#Doc profane test
print "\n Test codification on : 'This is ole miss!!!'"
s = datetime.datetime.now()
post_data = { 'filter_id': FILTER_ID, 'text' : "This is ole!!!"} #A dictionary of your post data
r = requests.post('{0}/filters/{1}/codify/'.format(BASE_HTTP_URL, FILTER_ID), post_data)
# print r.text
resp = json.loads(r.text)
print "Profane code: ", resp['profane_code']
e = datetime.datetime.now()
d = e - s
print "Total time taken: ", d.total_seconds() * 1000


#Remove term
print "\n Remove term : 'Ole'"
s = datetime.datetime.now()
post_data = { 
  'filter_id': FILTER_ID,
  'black_list': {
    'remove': ["ole"]
  }
}
r = requests.put('{0}/filters/{1}'.format(BASE_HTTP_URL, FILTER_ID), data=json.dumps(post_data))
# print r.text
e = datetime.datetime.now()
d = e - s
print "Total time taken: ", d.total_seconds() * 1000

#Doc profane test
print "\n Test codification on : 'This is ole!!!'"
s = datetime.datetime.now()
post_data = { 'filter_id': FILTER_ID, 'text' : "This is ole!!!"} #A dictionary of your post data
r = requests.post('{0}/filters/{1}/codify/'.format(BASE_HTTP_URL, FILTER_ID), post_data)
print r.text
resp = json.loads(r.text)
print "Profane code: ", resp['profane_code']
e = datetime.datetime.now()
d = e - s
print "Total time taken: ", d.total_seconds() * 1000

#Doc profane test
print "\n Test codification on : 'Happy'"
s = datetime.datetime.now()
post_data = { 'filter_id': FILTER_ID, 'text' : "Happy"} #A dictionary of your post data
r = requests.post('{0}/filters/{1}/codify/'.format(BASE_HTTP_URL, FILTER_ID), post_data)
print r.text
resp = json.loads(r.text)
print "Profane code: ", resp['profane_code']
e = datetime.datetime.now()
d = e - s
print "Total time taken: ", d.total_seconds() * 1000



# #websocket testing
# print "\n Websocket test"
# ws = create_connection("ws://localhost:8888/ws")
# resp =  ws.recv()
# print "Received '%s'" % resp

# test_doc = { 'filter_id': FILTER_ID, 'text' : "This is ole"} 
# print "\n Test codification on : 'This is ole'"
# s = datetime.datetime.now()
# ws.send(json.dumps(test_doc))
# resp =  ws.recv()
# print "Received '%s'" % resp
# e = datetime.datetime.now()
# d = e - s
# print "Total time taken: ", d.total_seconds() * 1000

# s = datetime.datetime.now()
# test_doc = { 'filter_id': FILTER_ID, 'text' : "This is shit!"}
# print "\n Test codification on : 'This is shit!'"
# ws.send(json.dumps(test_doc))
# resp =  ws.recv()
# print "Received '%s'" % resp
# e = datetime.datetime.now()
# d = e - s
# print "Total time taken: ", d.total_seconds() * 1000

# ws.close()

