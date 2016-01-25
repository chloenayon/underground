from flask import *
import urllib2
import json
from models import *

app = Flask(__name__)


@app.route('/', methods=["GET"])
def home():
    user = session['user']
    if user is None:
        return render_template('home.html')
    else:
        return render_template('home.html', user=user)


@app.route('/login', methods=["GET", "POST"])
def login():
    user = session['user']
    if user is not None:
        return redirct(url_for('home'))

    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.objects(username=username).first()

        if user == None:
            return render_template('login.html', error='User doesn\'t exist')
        else:
            if user.verify_password(password=password):
                session['user'] = user
                return redirct(url_for('home'))
            else:
                return render_template('login.html', error='Password incorrect')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    user = session['user']
    if user is not None:
        return redirct(url_for('home'))

    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':

        user = User(
            username=request.form['username'],
            first_name=request.form['firstName'],
            last_name=request.form['lastName'],
            email=request.form['email'],
            password=request.form['password']
        )

        try:
            user.save()
        except ValidationError as error:
            return render_template('signup.html', errors=error.to_dict())
        else:
            session['user'] = user
            return redirect(url_for('home'))


@app.route('/users/<string:username>', methods=["GET"])
def user_profile(username):

    user = User.objects(username=username).first()
    if user == None:
        abort(404)
    else:
        places = Place.objects(user=user).all()
        lists = List.objects(user=user).all()
        return render_template('user_profile.html', user=user, places=places, lists=lists)


@app.route('/users/<string:username>/edit', methods=["GET", "POST"])
def edit_user(username):
    user = session['user']
    if user is None:
        return abort(404)

    if request.method == 'GET':
        if username != user.username:
            return redirect(url_for('user_profile', username=username))
        else:
            return render_template('edit_user.html', user=user)

    if request.method = 'POST':

        if user.username != username:
            return redirect(url_for('user_profile', username=username))
        else:
            if request.form['firstName'] is not None:
                user.first_name = request.form['firstName']

            if request.form['lastName'] is not None:
                user.last_name = request.form['lastName']

            if request.form['username'] is not None:
                user.username = request.form['username']

            if request.form['password'] is not None:
                user.password = request.form['password']

            if request.form['email'] is not None:
                user.email = request.form['email']

            try:
                user.save()
            except ValidationError as error:
                return render_template('edit_user.html', errors=error.to_dict())
            else:
                session['user'] = user
                return redirect(url_for('user_profile', username=user.username))


@app.route('/places/create', methods=["GET", "POST"])
def create_place():
    user = session['user']
    if user is None:
        return redirect(url_for('home'))

    if request.method == 'GET':
        return render_template('create_place.html')

    if request.method == 'POST':
        place = Place(
            user=user,
            name=request.form['name'],
            description=request.form['description'],
            location=[request.form['latitude'],request.form['longitude']],
            address=request.form['address']
        )

        try:
            place.save()
        except ValidationError as error:
            return render_template('create_place.html', errors=error.to_dict())
        else:
            return redirect(url_for('view_place', place_id=place.id))



@app.route('/places/<string:place_id>', methods=["GET"])
def view_place(place_id):
    user = session['user']
    place = Place.objects(id=place_id).first()
    if place == None:
        abort(404)
    else:
        comments = Comment.objects(place=place).all()
        return render_template('view_place.html', user=user, place=place, comments=comments)

@app.route('/places/<string:place_id>/edit', methods=['GET', 'PUT', 'DELETE'])
def edit_place(place_id):
    user = session['user']
    if user is None:
        return redirect(url_for('view_place', place_id=place_id))

    place = Place.objects(id=place_id).first()
    if place == None:
        abort(404)

    if place.user!= user:
        return redirect(url_for('view_place', place_id=place.id))

    if request.method == 'GET':
        return render_template('edit_place.html', user=user, place=place)

    if request.method == 'PUT':
        if request.form['name'] is not None:
            place.name = request.form['name']

        if request.form['description'] is not None:
            place.description = request.form['description']

        if request.form['latitude'] is not None and request.form['longitude'] is not None:
            place.location = [
                request.form['latitude'],
                request.form['longitude']
            ]

        if request.form['address'] is not None:
            user.address = request.form['address']

        try:
            place.save()
        except ValidationError as error:
            return render_template('edit_place.html', errors=error.to_dict())
        else:
            return redirect(url_for('view_place', place_id=place.id))

    if request.method == 'DELETE'
        try:
            place.delete()
        except Exception as error:
            return render_template('edit_place.html', user=user, errors=error.to_dict())
        else:
            return redirect(url_for('home'))

@app.route('/places/<string:place_id>/comments', methods=["POST"])
def add_comment(place_id):
    user = session['user']
    if user is None:
        return redirect(url_for('view_place', place_id=place_id))

    place = Place.objects(id=place_id).first()
    if place == None:
        abort(404)

    comment = Comment(
        place=place,
        user=user,
        text=request.form['text']
    )

    try:
        comment.save()
    except ValidationError as error:
        return render_template('view_place.html', user=user, errors=error.to_dict())
    else:
        return redirect(url_for('view_place', place_id=place_id))



@app.route('/search', methods=["GET"])
def search():
    user = session['user']
    q = request.args.get('q')
    if q is None:
        return render_template('search.html', user=user)
    else:
        places = Place.objects.search_text(q).all()
        return render_template('search.html', user=user, places=places)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.debug = True
    app.secret_key = "HappyLittleTrees"
    app.run('0.0.0.0', port=8000)
