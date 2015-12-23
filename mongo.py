from pymongo import MongoClient

conn = MongoClient()

users = conn['users']
places = conn['places']

bobross = {'first':"Bob", 'last':"Ross", 'uname':"bobtheross", 'email':"bobtheross@bobross.com", 'pass':"happylittletrees"}
#first name
#last name
#username
#email
#password

stuy = {'lat':"-70", 'long':"43", 'address':"here", 'name':"school", 'description':"hell"}
#latitude
#longitude
#address
#name/title
#description

#db.users.insert(bobross)
#db.places.insert(stuy)

def addPlace(lat, lon, add, title, desc):
    conn = MongoClient()
    db = conn['places']
    db.places.insert({'lat': lat, 'long':lon, 'address': add, 'name':title, 'description':desc})


