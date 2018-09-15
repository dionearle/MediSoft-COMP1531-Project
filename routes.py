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
    
@app.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    if request.method == "GET":
        times = ['00:00-00:30', '00:30-01:00', '01:00-01:30', '01:30-02:00', '02:00-02:30', '02:30-03:00', 
                '03:00-03:30', '03:30-04:00', '04:00-04:30', '04:30-05:00', '05:00-05:30', '05:30-06:00', 
                '06:00-06:30', '06:30-07:00', '07:00-07:30', '07:30-08:00', '08:00-08:30', '08:30-09:00', 
                '09:00-09:30', '09:30-10:00', '10:00-10:30', '10:30-11:00', '11:00-11:30', '11:30-12:00',
                
                '12:00-12:30', '12:30-13:00', '13:00-13:30', '13:30-14:00', '14:00-14:30', '14:30-15:00', 
                '15:00-15:30', '15:30-16:00', '16:00-17:30', '16:30-17:00', '17:00-17:30', '17:30-18:00', 
                '18:00-18:30', '18:30-19:00', '19:00-20:30', '19:30-20:00', '20:00-20:30', '20:30-21:00', 
                '21:00-21:30', '21:30-22:00', '22:00-23:30', '22:30-23:00', '23:00-23:30', '23:30-00:00']
                                
    return render_template('book.html', times=times)  
    
@app.route('/book', methods=['POST'])
@login_required
def reason():
    bookReason = request.form['bookReason']
    processedText = text.upper()
    return processedText
    
    
