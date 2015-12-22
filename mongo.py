from pymongo import MongoClient

conn = MongoClient()
users = conn['users']
places = conn['places']

db.users.insert({'first':"Bob", 'last':"Ross"})
db.places.insert({'name':"school", 'description':"hell"})
