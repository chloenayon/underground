from mongoengine import *
import datetime

def get_current_user(session):
    if 'user' in session:
        return User.objects(username=session['user']['username']).first()
    else:
        return None

def mongo_to_dict(obj):

    return_data = []

    if isinstance(obj, Document):
        return_data.append(("id", str(obj.id)))

    for field_name in obj._fields:
        data = obj._data[field_name]

        if isinstance(obj._fields[field_name], DateTimeField):
            return_data.append((field_name, str(data.isoformat())))

        elif isinstance(obj._fields[field_name], StringField):
            return_data.append((field_name, str(data)))

        elif isinstance(obj._fields[field_name], FloatField):
            return_data.append((field_name, float(data)))

        elif isinstance(obj._fields[field_name], IntField):
            return_data.append((field_name, int(data)))

        elif isinstance(obj._fields[field_name], ListField):
            return_data.append((field_name, data))

        elif isinstance(obj._fields[field_name], EmbeddedDocumentField):
            return_data.append((field_name, to_dict(data)))

        elif isinstance(obj._fields[field_name], ObjectIdField):
            return_data.append((field_name, str(data)))

        else:
            print type(obj._fields[field_name])

    return dict(return_data)

class User(DynamicDocument):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    username = StringField(required=True, max_length=20, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(max_length=255, required=True)


class Place(DynamicDocument):
    name = StringField(required=True)
    description = StringField(required=True)
    latitude = FloatField(required=True)
    longitude = FloatField(required=True)
    address = StringField()
    user = ReferenceField('User', required=True)
    category = StringField()

class Comment(DynamicDocument):
    user = ReferenceField('User', required=True)
    place = ReferenceField('Place', required=True)
    text = StringField(required=True)
    date = DateTimeField(required=True)

    def pre_save(cls, sender, document, **kwargs):
        document.date = datetime.utcnow()
