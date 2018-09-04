from flask import Flask

def valid_time(time):
    return time > 0

app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"
