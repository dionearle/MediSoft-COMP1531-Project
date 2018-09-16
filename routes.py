from server import app, login_manager, userManager
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from flask import request, render_template, redirect, url_for
from users import User,  Patient, HealthProvider
from search import searchFiles
import csv


def get_user(user_id):
    return userManager.getID(user_id)

@login_manager.user_loader
def load_user(user_id):
    # get user information from db
    user = get_user(user_id)
    return user

@app.route('/', methods=['GET','POST'])
def index():
    if current_user.is_authenticated == False:
        if request.method == 'POST':
            if userManager.correctCredentials(request.form["loginEmail"], request.form["loginPassword"]) == True:

                user = userManager.getID(request.form["loginEmail"])
                login_user(user)
                return redirect(url_for('loginSuccess'))
            return render_template("loginPost.html", success=False) # if login failed, return an alert saying "Wrong email/password"
        return render_template("base.html") # runs when the user first opens the page
    else:
        return redirect(url_for('loginSuccess'))

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == "POST":
        searchArray = searchFiles(request.form["searchText"], request.form["radioSearch"])
        if (searchArray[0] == True):
            return render_template("searchResults.html", searchArray=searchArray, option=request.form["radioSearch"])
    
    return render_template('search.html', username=current_user.get_id())

@app.route('/loginSuccess', methods=['GET', 'POST'])
@login_required
def loginSuccess():
    currentID = current_user.get_id()
    return render_template("loginSuccess.html", username="hi")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile/<name>', methods=['GET', 'POST'])
def profile(name):
    if request.method == "POST":
        option = request.form["option"]
        if option == "healthCentre" or option == "suburb":
            typeCentre = request.form["typeCentre"]
            name = request.form["name"]
            abn = request.form["abn"]
            phone = request.form["phone"]
            suburb = request.form["suburb"]
            return render_template("profile.html",option=option, typeCentre=typeCentre, name=name, abn=abn,
            phone=phone, suburb=suburb, rating = 0)
        elif option == "healthProvider":
            email = request.form["user"]
            typeCentre = request.form["typeCentre"]
            name = request.form["name"]
            abn = request.form["abn"]
            phone = request.form["phone"]
            suburb = request.form["suburb"]
            return render_template("profile.html",option=option, email=email, typeCentre=typeCentre, name=name, abn=abn,
            phone=phone, suburb=suburb, rating = 0)
        elif option == "service":
            email = request.form["user"]
            service = request.form["service"]
            typeCentre = request.form["typeCentre"]
            name = request.form["name"]
            abn = request.form["abn"]
            phone = request.form["phone"]
            suburb = request.form["suburb"]
            return render_template("profile.html",option=option, email=email, service=service, typeCentre=typeCentre, name=name, abn=abn,
            phone=phone, suburb=suburb, rating = 0)
    return render_template("profile.html")
