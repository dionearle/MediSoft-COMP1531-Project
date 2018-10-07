from server import app, login_manager, userManager, appointmentManager, centreManager
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from flask import request, render_template, redirect, url_for
from users import User,  Patient, HealthProvider
from search import searchFiles
from appointmentManager import AppointmentManager
from save import saveData
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
    times = ['00:00-00:30', '00:30-01:00', '01:00-01:30', '01:30-02:00', '02:00-02:30', '02:30-03:00',
                '03:00-03:30', '03:30-04:00', '04:00-04:30', '04:30-05:00', '05:00-05:30', '05:30-06:00',
                '06:00-06:30', '06:30-07:00', '07:00-07:30', '07:30-08:00', '08:00-08:30', '08:30-09:00',
                '09:00-09:30', '09:30-10:00', '10:00-10:30', '10:30-11:00', '11:00-11:30', '11:30-12:00',

                '12:00-12:30', '12:30-13:00', '13:00-13:30', '13:30-14:00', '14:00-14:30', '14:30-15:00',
                '15:00-15:30', '15:30-16:00', '16:00-17:30', '16:30-17:00', '17:00-17:30', '17:30-18:00',
                '18:00-18:30', '18:30-19:00', '19:00-20:30', '19:30-20:00', '20:00-20:30', '20:30-21:00',
                '21:00-21:30', '21:30-22:00', '22:00-23:30', '22:30-23:00', '23:00-23:30', '23:30-00:00']
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