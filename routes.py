from server import app, login_manager, currentLoggedIn
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from flask import request, render_template, redirect, url_for
from users import User
from search import searchFiles
import csv



def get_user(user_id):
    userDict = {}

    with open('provider.csv') as w:
        reader = csv.DictReader(w)
        for row in reader:
            if (row['provider_email'] == user_id):
                userDict['email'] = row['provider_email']
                userDict['password'] = row['password']
                break
    with open('patient.csv') as w:
        reader = csv.DictReader(w)
        for row in reader:
            if (row['patient_email'] == user_id):
                userDict['email'] = row['patient_email']
                userDict['password'] = row['password']

                break

    user_object = User(user_id, userDict['password'])
    return user_object

@login_manager.user_loader
def load_user(user_id):
    # get user information from db
    user = get_user(user_id)
    return user

@app.route('/', methods=['GET','POST'])
def index():
    if current_user.is_authenticated == False:
        if request.method == 'POST':
            with open("patient.csv", "r") as w:
                patient = False
                readLinesArray = w.readlines() # interpret data in patient.csv as an array
                for i in range(4):
                    (email, password) = readLinesArray[i].split(',') # split data into email and password
                    password = password[:-1]
                    # if email and password match
                    if email == request.form["loginEmail"] and \
                        password == request.form["loginPassword"]:

                        patient = True # to detect later whether to check providers.csv file or not
                        break
                
                if patient == True: 
                    user = User(email, password)
                    login_user(user)
                    currentLoggedIn = email
                    return redirect(url_for('loginSuccess'))

            with open("provider.csv", "r") as w:
                provider = False # for detecting whether login failed or not later
                readLinesArray = w.readlines() # interpret data in provider.csv as an array
                for i in range(8):
                    (name, specialisation, password) = readLinesArray[i].split(',') # pretty much same as above
                    password = password[:-1]
                    if name == request.form["loginEmail"] and \
                        password == request.form["loginPassword"]:
                        provider = True
                        break
                if provider == True:
                    user = User(name, password)
                    login_user(user)
                    currentLoggedIn = name
                    print("currentLoggedIn: " + currentLoggedIn)
                    return redirect(url_for('loginSuccess'))
            return render_template("loginPost.html", success=False) # if login failed, return an alert saying "Wrong email/password"
        return render_template("base.html") # runs when the user first opens the page
    else:
        return redirect(url_for('loginSuccess'))

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == "POST":
        print("radio: " + str(request.form["radioSearch"]))
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

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == "POST":
        option = request.form["option"]
        if option == "healthCentre" or option == "suburb":
            typeCentre = request.form["typeCentre"]
            name = request.form["name"]
            postcode = request.form["postcode"]
            phone = request.form["phone"]
            suburb = request.form["suburb"]
            return render_template("profile.html",option=option, typeCentre=typeCentre, name=name, postcode=postcode,
            phone=phone, suburb=suburb)
        elif option == "healthProvider":
            user = request.form["user"]
            typeCentre = request.form["typeCentre"]
            name = request.form["name"]
            postcode = request.form["postcode"]
            phone = request.form["phone"]
            suburb = request.form["suburb"]
            return render_template("profile.html",option=option, user=user, typeCentre=typeCentre, name=name, postcode=postcode,
            phone=phone, suburb=suburb)
        elif option == "service":
            user = request.form["user"]
            service = request.form["service"]
            typeCentre = request.form["typeCentre"]
            name = request.form["name"]
            postcode = request.form["postcode"]
            phone = request.form["phone"]
            suburb = request.form["suburb"]
            return render_template("profile.html",option=option, user=user, service=service, typeCentre=typeCentre, name=name, postcode=postcode,
            phone=phone, suburb=suburb)
    return render_template("profile.html",typeCentre="test")
