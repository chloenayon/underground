from mongoengine import *
import datetime

def get_current_user(session):
    if 'user' in session:
        return User.objects(username=session['user']['username']).first()
    else:
        return None

class User(DynamicDocument):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    username = StringField(required=True, max_length=20, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(max_length=255, required=True)

    def to_dict(self):
        return {
            'id': str(self.id),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'username': self.username,
            'password': self.password,
        }


class Place(DynamicDocument):
    name = StringField(required=True)
    description = StringField(required=True)
    latitude = FloatField(required=True)
    longitude = FloatField(required=True)
    address = StringField()
    user = ReferenceField('User', required=True)
    category = StringField()

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'user': self.user.to_dict(),
            'category': self.category
        }

class Comment(DynamicDocument):
    user = ReferenceField('User', required=True)
    place = ReferenceField('Place', required=True)
    text = StringField(required=True)
    date = DateTimeField(required=True)

    def pre_save(cls, sender, document, **kwargs):
        document.date = datetime.utcnow()

    def to_dict(self):
        return {
            'id': str(self.id),
            'user': self.user.to_dict(),
            'place': self.place.to_dict(),
            'text': self.text,
            'date': self.date
        }
