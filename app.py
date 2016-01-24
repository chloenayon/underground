from flask import *
import urllib2
import json
from models import *

app = Flask(__name__)


@app.route('/', methods=["GET"])
def home():
    if 'user' in session:
        return render_template('home.html', user=session['user'])
    else:
        return render_template('home.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if 'user' in session:
        return render_template('home.html', user=session['user'])

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
                return render_template('home.html', user=user)
            else:
                return render_template('login.html', error='Password incorrect')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if 'user' in session:
        return redirect(url_for('home'))

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
    user = session['user']
    if user is None:
        return redirect(url_for('home'))

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
        return redirect(url_for('home'))

    if request.method == 'GET':
        if username != session['user'].username:
            return redirect(url_for('user_profile', username=username))
        else:
            return render_template('edit_user.html')

    if request.method = 'POST':

        user = session['user']
        if user == None:
            abort(404)
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
@app.route('/places/<string:place_id>/edit', methods=["GET", "POST"])
@app.route('/places/<string:place_id>/delete', methods=["POST"])
@app.route('/places/<string:place_id>/comments', methods=["POST"])
@app.route('/search', methods=["GET"])

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.debug = True
    app.secret_key = "HappyLittleTrees"
    app.run('0.0.0.0', port=8000)
