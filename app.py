from flask import *
from models import *

app = Flask(__name__)

try:
    connect('heroku_1p1fq4fq',
            host='mongodb://heroku_1p1fq4fq:n28s1p9g2mtingmu9ideuk9j04@ds049935.mongolab.com:49935/heroku_1p1fq4fq')
except Exception as e:
    print e
else:
    print 'YOU WILL DO THIS'


@app.route('/', methods=["GET"])
def home():
    """
    description: Renders the home page

    authentication: none

    """

    current_user = get_current_user(session)
    if current_user is None:
        return render_template('home.html')
    else:
        return render_template('home.html', current_user=current_user.to_dict())


@app.route('/login', methods=["GET", "POST"])
def login():
    """
    description: Renders the login page and handles login process

    authentication: none

    if the user is logged in redirects to home
    if the user is not logged in renders the login page
    if the credentials are incorrect it redisplays the login page with errors
    """
    current_user = get_current_user(session)
    if current_user is not None:
        return redirect(url_for('home'))

    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.objects(username=username).first()

        if user == None:
            return render_template('login.html', error='User doesn\'t exist')
        else:
            if user.password == password:
                session['user'] = user.to_dict()
                return redirect(url_for('home'))
            else:
                return render_template('login.html', error='Password incorrect')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """
    description: Renders the signup page and handles sign up process

    authentication: none

    if the user is logged in redirects to home
    if the user is not logged in renders the sign up page
    if the data is incorrect it redisplays the sign up page with errors
    """
    current_user = get_current_user(session)
    if current_user is not None:
        return redirect(url_for('home'))

    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':

        user = User(
            username=request.form['username'],
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
            password=request.form['password']
        )

        try:
            user.save()
        except ValidationError as error:
            return render_template('signup.html', errors=error.to_dict())
        else:
            session['user'] = user.to_dict()
            return redirect(url_for('home'))


@app.route('/users/<string:username>', methods=["GET"])
def profile(username):
    """
    description: Renders the user profile, lists places, favorites

    authentication: none
    """
    current_user = get_current_user(session)
    user = User.objects(username=username).first()
    if user == None:
        abort(404)
    else:
        places = []

        for place in Place.objects(user=user).all():
            places.append(place.to_dict())

        return render_template('profile.html', current_user=current_user.to_dict(), user=user.to_dict(), places=places)


@app.route('/users/<string:username>/edit', methods=["GET", "POST"])
def edit_user(username):
    """
    description: Renders the edit user page, handles edit user logic

    authentication: required
    """
    current_user = get_current_user(session)
    if current_user is None:
        return abort(404)

    if request.method == 'GET':
        if username != user.username:
            return redirect(url_for('profile', username=username))
        else:
            return render_template('edit_user.html', user=user)

    if request.method == 'POST':

        if current_user.username != username:
            return redirect(url_for('profile', username=username))
        else:
            if request.form.get('firstName') is not None:
                current_user.first_name = request.form.get('first_name')

            if request.form.get('lastName') is not None:
                current_user.last_name = request.form.get('lastName')

            if request.form.get('username') is not None:
                current_user.username = request.form.get('username')

            if request.form.get('password') is not None:
                current_user.password = request.form.get('password')

            if request.form.get('email') is not None:
                current_user.email = request.form.get('email')

            try:
                current_user.save()
            except ValidationError as error:
                return render_template('profile.html', current_user=current_user.to_dict(), errors=error.to_dict())
            else:
                session['user'] = current_user.to_dict()
                return redirect(url_for('profile', username=current_user.username))


@app.route('/places', methods=["POST"])
def create_place():
    """
    description:  handles place creation logic

    authentication: required
    """
    current_user = get_current_user(session)
    if current_user is None:
        return redirect(url_for('home'))

    if request.method == 'POST':
        place = Place(
            user=current_user,
            name=request.form.get('name'),
            description=request.form.get('description'),
            latitude=request.form.get('latitude'),
            longitude=request.form.get('longitude'),
            address=request.form.get('address'),
            category=request.form.get('category')
        )

        try:
            place.save()
        except ValidationError as error:
            return render_template('profile.html', current_user=current_user, errors=error.to_dict())
        else:
            return redirect(url_for('view_place', place_id=place.id))


@app.route('/places/<string:place_id>', methods=["GET"])
def view_place(place_id):
    """
    description: Renders the place page

    authentication: none
    """
    current_user = get_current_user(session)
    place = Place.objects(id=place_id).first()
    if place == None:
        abort(404)
    else:
        comments = Comment.objects(place=place).all()
        return render_template('view_place.html', user=user, place=place, comments=comments)


@app.route('/places/<string:place_id>/edit', methods=['GET', 'PUT', 'DELETE'])
def edit_place(place_id):
    """
    description: Renders the edit place page, handles the edit place logic, handles the delete page logic

    authentication: required

    user must be the owner of the place to edit or delete it
    """
    user = get_current_user(session)
    if user is None:
        return redirect(url_for('view_place', place_id=place_id))

    place = Place.objects(id=place_id).first()
    if place == None:
        abort(404)

    if place.user != user:
        return redirect(url_for('view_place', place_id=place.id))

    if request.method == 'GET':
        return render_template('edit_place.html', user=user, place=place)

    if request.method == 'PUT':
        if request.form.get('name') is not None:
            place.name = request.form.get('name')

        if request.form.get('description') is not None:
            place.description = request.form.get('description')

        if request.form.get('latitude') is not None:
            place.location = request.form.get('latitude')

        if request.form.get('longitude') is not None:
            place.location = request.form.get('longitude')

        if request.form.get('address') is not None:
            user.address = request.form.get('address')

        try:
            place.save()
        except ValidationError as error:
            return render_template('edit_place.html', user=user, errors=error.to_dict())
        else:
            return redirect(url_for('view_place', place_id=place.id))

    if request.method == 'DELETE':
        try:
            place.delete()
        except Exception as error:
            return render_template('edit_place.html', user=user, errors=error.to_dict())
        else:
            return redirect(url_for('home'))


@app.route('/places/<string:place_id>/comments', methods=["POST"])
def add_comment(place_id):
    """
    description: Handles the add comment logic

    authentication: required

    redirects to the view place page on success or failure
    """
    user = get_current_user(session)
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
    """
    description: Renders the search page

    authentication: none
    """
    current_user = get_current_user(session)
    q = request.args.get('q')
    if q is None:
        return redirect(url_for('home'))
    else:
        places = []

        for place in Place.objects.search_text(q).all():
            places.append(place.to_dict())
        return render_template('search.html', current_user=current_user, places=places)


@app.errorhandler(404)
def page_not_found(error):
    """
    description: Renders the not found page

    authentication: none
    """
    current_user = get_current_user(session)
    return render_template('404.html', current_user=current_user.to_dict()), 404


if __name__ == "__main__":
    app.debug = True
    app.secret_key = "EFAB22A53737A1C6BD7F5575A9FA1"
    app.run('0.0.0.0', port=8000)
