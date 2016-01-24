from flask import Flask, render_template, request, session, redirect, url_for, escape
import urllib2, json
import member_data
import models


app = Flask(__name__)




@app.route('/', methods=["GET"])

@app.route('/login', methods=["GET", "POST"])
@app.route('/signup', methods=["GET", "POST"])

@app.route('/users/<string:username>', methods=["GET"])
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
