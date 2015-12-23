from pymongo import MongoClient

conn = MongoClient()

db = conn['thing']

users = conn['users']
places = conn['places']

bobross = {'first':"Bob", 'last':"Ross", 'uname':"bobtheross", 'email':"bobtheross@bobross.com", 'pass':"happylittletrees"}
stuy = {'lat':"", 'long':"", 'address':"", 'name':"school", 'description':"hell"}

db.users.insert(bobross)
db.places.insert(stuy)
