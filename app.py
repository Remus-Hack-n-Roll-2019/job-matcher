from flask import Flask
app = Flask(__name__)

@app.route("/")
def start():
    return "<h1> Our website!!</h1>"