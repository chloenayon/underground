from flask import Flask, render_template, request, session, redirect, url_for, escape
import urllib2, json

app = Flask(__name__)

mapKey = 'pk.eyJ1IjoiY2thdWJpc2NoIiwiYSI6ImNpaWJ2eGE2dzAxa3\
B3ZWx6NWYwZGx1dWIifQ.jSuKW32Avl_d3_TB2JqGlA'

@app.route('/', methods = ['GET', 'POST'])
def begin():
#    if 'username' in session:
    return render_template("home.html")

@app.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
#        session['username'] = request.form['username']
        return redirect(url_for('begin'))
    else:
        return render_template("login.html")

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    pass
      


if __name__=="__main__":
    app.debug = True
    app.run('0.0.0.0', port=8000)
        
