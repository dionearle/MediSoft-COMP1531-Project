from server import app, login_manager, userManager, appointmentManager, centreManager
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from flask import request, render_template, redirect, url_for
from users import User,  Patient, HealthProvider
from search import searchFiles
from appointmentManager import AppointmentManager
from save import saveData
import csv
import datetime


def get_user(user_id):
    return userManager.getID(user_id)

@login_manager.user_loader
def load_user(user_id):
    # get user information from db
    user = get_user(user_id)
    return user

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == "POST":
        searchArray = searchFiles(request.form["searchText"], request.form["radioSearch"])
        if (searchArray[0] == True):
            return render_template("searchResults.html", searchArray=searchArray, option=request.form["radioSearch"])

    return render_template('search.html', username=current_user.get_id())

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == False:
        if request.method == 'POST':
            if userManager.correctCredentials(request.form["loginEmail"], request.form["loginPassword"]) == True:
                user = userManager.getID(request.form["loginEmail"])
                login_user(user)
                return redirect(url_for('index'))
            return render_template("login.html", success=False) # if login failed, return an alert saying "Wrong email/password"
        return render_template("login.html") # runs when the user first opens the page
    else:
        return redirect(url_for('index'))


@app.route('/profile/<typeUser>/<name>', methods=['GET', 'POST'])
def profile(typeUser, name):
    if request.method == "POST":
        if typeUser == "centre":
            centre = centreManager.searchHealthCentresByName(name)
            return render_template("profile.html", option="healthCentre", centre=centre[0])
        elif typeUser == "provider":
            if name == current_user.get_id():
                return render_template("profile.html", option="self")
            provider = userManager.searchID(name)
            return render_template("profile.html", option="provider", provider=provider[0])
        elif typeUser == "patient":
            if name == current_user.get_id():
                return render_template("profile.html", option="self")
            patient = userManager.searchPatient(name)
            return render_template("profile.html", option="patient", patient=patient[0])

        option = request.form["option"]
        name = request.form["name"]
        typeCentre = request.form["typeCentre"]
        phone = request.form["phone"]
        suburb = request.form["suburb"]
        abn = request.form["abn"]
        if option == "healthCentre" or option == "suburb":
            centre = centreManager.searchHealthCentresByName(name)
            return render_template("profile.html",option=option, typeCentre=typeCentre, name=name, abn=abn,
            phone=phone, suburb=suburb, rating = 0, providers=centre[0].getProviders())
        elif option == "healthProvider":
            email = request.form["user"]
            return render_template("profile.html",option=option, email=email, typeCentre=typeCentre, name=name, abn=abn,
            phone=phone, suburb=suburb, rating = 0)
        elif option == "service":
            email = request.form["user"]
            service = request.form["service"]
            return render_template("profile.html",option=option, email=email, service=service, typeCentre=typeCentre, name=name, abn=abn,
            phone=phone, suburb=suburb, rating = 0)
    return render_template("profile.html", option="self")

@app.route('/update/<name>', methods=['GET', 'POST'])
def update_profile(name):

    if request.method == "POST":
        new_firstName = request.form["new_firstName"]
        if new_firstName != "":
            current_user.set_FirstName(new_firstName)
        new_lastName = request.form["new_lastName"]
        if new_lastName != "":
            current_user.set_LastName(new_lastName)
        new_phone = request.form["new_phone"]
        if new_phone != "":
            current_user.set_phone(new_phone)
        new_password = request.form["new_password"]
        if new_password != "":
            current_user.set_password(new_password)
        if current_user.isPatient() == True:
            new_medicare = request.form["new_medicare"]
            if new_medicare != "":
                current_user.set_medicare(new_medicare)
        else:
            new_profession = request.form["new_profession"]
            if new_profession != "":
                current_user.set_profession(new_profession)
            new_providerNum = request.form["new_providerNum"]
            if new_providerNum != "":
                current_user.set_providerNum(new_providerNum)

        # write all data to files
        saveData(centreManager, userManager, appointmentManager)
        return render_template("profile.html", option="self")
    return render_template("update_profile.html")

@app.route('/book/<email>', methods=['GET', 'POST'])
@login_required
def book(email):
    fmt='%H:%M'
    time=datetime.datetime.strptime('00:00',fmt)
    min30=datetime.timedelta(minutes=30)
    times=[]
    for i in range(48):
        times.append('%s-%s' % ( time.strftime(fmt), (time+min30).strftime(fmt)))
        time+=min30
           
    return render_template('book.html', times=times, name=email)

@app.route('/bookAppointment/<email>', methods=['GET', 'POST'])
@login_required
def bookAppointment(email):
    # find provider and add the appointment
    # find current user logged in and add the appointment
    # def addAppointment(provider_email, patient_email, date, time):
    # addAppointment(request.form['email'])
    appointmentManager.addAppointment(userManager, email, current_user.get_id(), str(request.form['time']), request.form["date"], request.form['bookReason'])
    saveData(centreManager, userManager, appointmentManager)
    return render_template('index.html', booked=True)

@app.route('/book', methods=['POST'])
@login_required
def reason():
    bookReason = request.form['bookReason']
    processedText = text.upper()
    return processedText

@app.route('/appointments', methods=['GET', 'POST'])
def showBookings():
    return render_template('appointments.html', appointments=appointmentManager.getAppointments(current_user))


@app.route('/profile/updateRatings/<typeUser>/<name>', methods=['POST'])
@login_required
def updateRatings(name, typeUser):
    if typeUser == 'centre':
        centre = centreManager.searchHealthCentresByName(name)[0]
        centre.updateRating(current_user.get_id(), int(request.form['updateRatingBox']))
        saveData(centreManager, userManager, appointmentManager)
        return redirect(url_for('profile', typeUser=typeUser, name=name), code=307)
    elif typeUser == 'provider':
        provider = userManager.getID(name)
        provider.updateRating(current_user.get_id(), int(request.form['updateRatingBox']))
        saveData(centreManager, userManager, appointmentManager)
        return redirect(url_for('profile', typeUser=typeUser, name=name), code=307)
