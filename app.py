from flask import *
from models import *
import datetime
app = Flask(__name__)

try:
    connect('heroku_1p1fq4fq', host='mongodb://heroku_1p1fq4fq:n28s1p9g2mtingmu9ideuk9j04@ds049935.mongolab.com:49935/heroku_1p1fq4fq')
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
        except Exception as error:
            return render_template('signup.html', error="Username or email is taken")
        else:
            session['user'] = user.to_dict()
            return redirect(url_for('home'))

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

@app.route('/logout', methods=["GET"])
def logout():
    session.clear()
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


@app.route('/users/<string:username>/edit', methods=["POST"])
def edit_user(username):
    """
    description: Renders the edit user page, handles edit user logic

    authentication: required
    """
    current_user = get_current_user(session)
    if current_user is None:
        return abort(404)

    if request.method == 'POST':

        if current_user.username != username:
            return redirect(url_for('profile', username=username))
        else:
            if request.form.get('first_name') is not None:
                current_user.first_name = request.form.get('first_name')

            if request.form.get('last_name') is not None:
                current_user.last_name = request.form.get('lastName')

            if request.form.get('username') is not None:
                print request.form.get('username')
                current_user.username = request.form.get('username')

            if request.form.get('password') is not None:
                current_user.password = request.form.get('password')

            if request.form.get('email') is not None:
                current_user.email = request.form.get('email')

            try:
                current_user.save()
            except ValidationError as error:
                print error
                return redirect(url_for('profile', username=current_user.username))
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
            latitude=float(request.form.get('latitude')),
            longitude=float(request.form.get('longitude')),
            address=request.form.get('address'),
            category=request.form.get('category')
        )

        try:
            place.save()
        except Exception as error:
            print error
            return redirect(url_for('profile', username=current_user.username))
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
        comments = []
        for comment in Comment.objects(place=place_id).all():
            comments.append(comment.to_dict())
        return render_template('place.html', current_user=current_user.to_dict(), place=place.to_dict(), comments=comments)


@app.route('/places/<string:place_id>/edit', methods=['POST'])
def edit_place(place_id):
    """
    description: Renders the edit place page, handles the edit place logic, handles the delete page logic

    authentication: required

    user must be the owner of the place to edit or delete it
    """
    current_user = get_current_user(session)
    if current_user is None:
        return redirect(url_for('view_place', place_id=place_id))

    place = Place.objects(id=place_id).first()
    if place == None:
        abort(404)

    if place.user != user:
        return redirect(url_for('view_place', place_id=place.id))

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
            return render_template('edit_place.html', current_user=current_user.to_dict(), error='something happened')
        else:
            return redirect(url_for('view_place', place_id=place.id))

    if request.method == 'DELETE':
        try:
            place.delete()
        except Exception as error:
            return render_template('edit_place.html', user=user, error=error.to_dict())
        else:
            return redirect(url_for('home'))


@app.route('/places/<string:place_id>/comments', methods=["GET", "POST"])
def add_comment(place_id):
    """
    description: Handles the add comment logic

    authentication: required

    redirects to the view place page on success or failure
    """
    current_user = get_current_user(session)
    if current_user is None:
        return redirect(url_for('view_place', place_id=place_id))

    place = Place.objects(id=place_id).first()
    if place == None:
        abort(404)

    comment = Comment(
        place=place,
        user=current_user,
        text=request.form.get('text'),
        date=datetime.date.today().strftime('%b %d, %Y')
    )

    try:
        comment.save()
    except ValidationError as error:
        return render_template('place.html', current_user=current_user.to_dict(), error='Problem saving your comment')
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
        return render_template('search.html', current_user=current_user.to_dict(), places=places)


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
