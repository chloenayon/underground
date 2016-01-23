from flask import Flask, render_template, request, session, redirect, url_for, escape
import urllib2, json
import member_data

app = Flask(__name__)

mapKey = 'pk.eyJ1IjoiY2thdWJpc2NoIiwiYSI6ImNpaWJ2eGE2dzAxa3\
B3ZWx6NWYwZGx1dWIifQ.jSuKW32Avl_d3_TB2JqGlA'

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route('/login', methods = ["GET", "POST"])
def login():
    if 'logged' not in session:
        session['logged'] = False
#    if request.method == "GET":
#        return render_template("index.html")
#    else:
    if request.method == "GET":
        print session
        print session['logged']
        return render_template("login.html")
    else:
        u = request.form['uname']
        p = request.form['passwd']
        if (member_data.verify(u, p)):
            session['logged'] = True
            session['username'] = u
            return redirect(url_for('map'))
        else:
            return render_template("login.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if session['logged'] == False:
        return redirect(url_for('login'))
    else:
        if request.method == "GET":
            return render_template("signup.html")
        else:
            if (member_data.newMember(request.form['first'], request.form['last'], request.form['user'], request.form['mail'], request.form['pass'])):
                return redirect(url_for('login'))
            else:
                return render_template("signup.html")

@app.route('/map', methods= ["GET", "POST"])
def map():
    if session['logged'] == False:
        return redirect(url_for('login'))
    else:
        if request.method == "GET":
            return render_template("mappage.html", name = session['username'])
        else:
            human = request.form["person"]
            list = member_data.getPlaces(human)
            return render_template("mappage.html", name = list)

@app.route('/logout', methods = ["GET", "POST"])
def logout():
    pass

if __name__=="__main__":
    app.debug = True
    app.secret_key = "HappyLittleTrees"
    app.run('0.0.0.0', port=8000)
