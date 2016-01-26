from mongoengine import *
import bcrypt, datetime

connect('heroku_1p1fq4fq', host='mongodb://heroku_1p1fq4fq:n28s1p9g2mtingmu9ideuk9j04@ds049935.mongolab.com:49935/heroku_1p1fq4fq')

class User(DynamicDocument):

    def __init__(self, *args, **kwargs):
            db.Document.__init__(self, *args, **kwargs)

            if 'password' in kwargs:
                self.password = kwargs['password']


    first_name = StringField(required=True)
    last_name = StringField(required=True)
    username = StringField(required=True, max_length=20, unique=True)
    email = EmailField(required=True, unique=True)
    _password = StringField(max_length=255, required=True)
    favorites = ListField(ReferenceField('Place'))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class Place(DynamicDocument):
    name = StringField(required=True)
    description = StringField(required=True)
    location = PointField(required=True)
    address = StringField()
    user = ReferenceField('User', required=True)

class Comment(DynamicDocument):
    user = ReferenceField('User', required=True)
    place = ReferenceField('Place', required=True)
    text = StringField(required=True)
    date = DateTimeField(required=True)

    def pre_save(cls, sender, document, **kwargs):
        document.date = datetime.utcnow()
