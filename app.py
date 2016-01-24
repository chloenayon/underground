from flask import *
import urllib2, json
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
def get_user(username):
    if 'user' not in session:
        return redirect(url_for('home'))

    user = User.objects(username=username).first()

    if user == None:
        abort(404)
    else:
        places = Place.objects(user=user).all()
        lists = List.objects(user=user).all()
        return render_template('user_profile.html', user=user, places=places, lists=lists)


@app.route('/users/<string:username>/edit', methods=["GET", "POST"])

@app.route('/places/create', methods=["GET", "POST"])
@app.route('/places/<string:place_id>', methods=["GET"])
@app.route('/places/<string:place_id>/edit', methods=["GET", "POST"])
@app.route('/places/<string:place_id>/delete', methods=["POST"])
@app.route('/places/<string:place_id>/comments', methods=["POST"])

@app.route('/lists/create', methods=["GET", "POST"])
@app.route('/lists/<string:list_id>', methods=["GET"])
@app.route('/lists/<string:list_id>/edit', methods=["GET", "POST"])
@app.route('/lists/<string:list_id>/delete', methods=["POST"])

@app.route('/search', methods=["GET"])

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


#
# @app.route('/login', methods = ["GET", "POST"])
# def login():
#     if 'logged' not in session:
#         session['logged'] = False
#     if request.method == "GET":
#         print session
#         print session['logged']
#         return render_template("login.html")
#     else:
#         u = request.form['uname']
#         p = request.form['passwd']
#         if (member_data.verify(u, p)):
#             session['logged'] = True
#             session['username'] = u
#             return redirect(url_for('map'))
#         else:
#             return render_template("login.html")
#
# #To add a place:
# # ** you can only add a place to the map of a specific member
# #
# #member_template.addPlace(request.form['uname'], request.form['lat'], request.form['lon'], request.form['title'], request.form['address'])
# #
# #
# #
# #
# #
# #
#
# @app.route('/signup', methods=["GET", "POST"])
# def signup():
#     if session['logged'] == False:
#         return redirect(url_for('login'))
#     else:
#         if request.method == "GET":
#             return render_template("signup.html")
#         else:
#             if (member_data.newMember(request.form['first'], request.form['last'], request.form['user'], request.form['mail'], request.form['pass'])):
#                 return redirect(url_for('login'))
#             else:
#                 return render_template("signup.html")
#
# @app.route('/map', methods= ["GET", "POST"])
# def map():
#     if session['logged'] == False:
#         return redirect(url_for('login'))
#     else:
#         if request.method == "GET":
#             return render_template("mappage.html", name = session['username'])
#         else:
#             human = request.form["person"]
#             list = member_data.getPlaces(human)
#             return render_template("mappage.html", name = list)

if __name__=="__main__":
    app.debug = True
    app.secret_key = "HappyLittleTrees"
    app.run('0.0.0.0', port=8000)
