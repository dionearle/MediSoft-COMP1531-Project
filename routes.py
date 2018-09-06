from server import app
from flask import request, render_template


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("base.html")