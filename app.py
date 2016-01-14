from flask import Flask, render_template, request, session, redirect, url_for, escape
import urllib2, json
import member_data

app = Flask(__name__)

mapKey = 'pk.eyJ1IjoiY2thdWJpc2NoIiwiYSI6ImNpaWJ2eGE2dzAxa3\
B3ZWx6NWYwZGx1dWIifQ.jSuKW32Avl_d3_TB2JqGlA'

@app.route('/', methods = ["GET", "POST"])
def begin():
    if request.method == "GET":
        return render_template("home.html")
    else:
        return render_template("home.html")


@app.route('/login', methods= ["GET", "POST"])
def input():
    if request.method == "GET":
        return render_template("login.html")
    else:
        return redirect(url_for('login', vr=request.form["person"]))
    
@app.route('/map', methods= ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        human = request.form["person"]
        list = member_data.getPlaces(human)
        return render_template("mappage.html", name = list)


@app.route('/signup', methods = ["GET", "POST"])
def signup():
    return render_template("signup.html")


@app.route('/logout', methods = ["GET", "POST"])
def logout():
    pass
      

if __name__=="__main__":
    app.debug = True
    app.run('0.0.0.0', port=8000)
        
