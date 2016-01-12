import os, sqlite3, csv

members_db = "memberData.db"

def go():
    if (not os.path.exists(members_db)):
        conn = sqlite3.connect(members_db)
        c = conn.cursor()

        q = """create table members (fname text, lname text, uname text, email text, pwrd text, base text);"""
        c.execute(q)

        #sample member Bob Ross
        
        q = """insert into members values ("Bob", "Ross", "BobTheRoss", "bobross@bobross.com", "happylittletrees", "bob.db");"""
        c.execute(q)

        conn.commit()

        #Sample database for Bob Ross

        conn2 = sqlite3.connect("BobBobTheRoss.db")
        c2 = conn2.cursor()

        q2 = """create table places (lat real, long real, title text, address text);"""
        
#add new member
def newMember(first, last, user, email, passwd):
    conn = sqlite3.connect(members_db)
    c = conn.cursor()

    q = """select uname from members"""
    
    #check for username doubles
    for a in c.execute(q):
        if a.lower() == user.lower():
            return false
        else:
            firstname = first.lower()
            database = "" + firstname + "" + user  + ".db"
            #Add new user
            q = """insert into members values (%s, %s, %s, %s, %s, %s);"""
            q = q%(first, last, user, email, passwd, database)
            c.execute(q)
            conn.commit()

            return true


def verify(name, passwd):
    conn = sqlite3.connect(members_db)
    c = conn.cursor()

    q = """ select pwrd from members where uname = "%s" """
    q = q%(name)

    a = c.execute(q)
    
    if a[0] == pwrd:
        return true
    else:
        return false


def addPlace(uname, lat, lon, titled, address):
    conn = sqlite3.connect(members_db)
    c = conn.cursor()

    q = """select base from members where uname = "%s" """
    q = q%(uname)

    db = c.execute(q)

    database = ""
    
    for a in db:
        database = a[0]
 #       print a[0]
    
    conn2 = sqlite3.connect(database)
    c2 = conn2.cursor()

    q2 = """create table if not exists places (lat real, long real, title text, address text);"""

    c2.execute(q2)
    conn2.commit()
    
    q2 = """insert into places values(%r, %r, "%s", "%s");"""
    q2 = q2%(lat, lon, titled, address)

    c2.execute(q2)
    conn2.commit()


def getPlaces(uname):
    conn = sqlite3.connect(members_db)
    c = conn.cursor()

    q = """select base from members where uname = "%s" """
    q = q%(uname)

    db = c.execute(q)

    database = ""
    
    for a in db:
        database = a[0]
#        print a[0]
    
    conn2 = sqlite3.connect(database)
    c2 = conn2.cursor()

    q2 = """select * from places"""

    thing = c2.execute(q2)

#    for a in thing:
#        print a

    return thing
    
go()
addPlace("BobTheRoss", 17.0836, 22.5700, "here", "wherever")

