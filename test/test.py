import requests
import json
import datetime

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
print "\n Test codification on : 'This is shitsdfdsf'"
s = datetime.datetime.now()
post_data = { 'client_id': 'testdata', 'doc' : "This is shitsdfdsf"} #A dictionary of your post data
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


