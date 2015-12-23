from flask import Flask, render_template
from pymongo import MongoClient
#import mongo

app = Flask(__name__)

@app.route('/')
def begin():
    return render_template("home.html")


if __name__=="__main__":
    app.debug = True
    app.run('0.0.0.0', port=8000)
        
