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
    return render_template('index.html', loggedInUser=current_user.get_id())

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == "POST":
        searchArray = searchFiles(request.form["searchText"], request.form["radioSearch"])
        if (searchArray[0] == True):
            return render_template("searchResults.html", loggedInUser=current_user.get_id(), searchArray=searchArray, option=request.form["radioSearch"])

    return render_template('search.html', loggedInUser=current_user.get_id(), username=current_user.get_id())

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
            return render_template("login.html",  success=False) # if login failed, return an alert saying "Wrong email/password"
        return render_template("login.html") # runs when the user first opens the page
    else:
        return redirect(url_for('index'))


@app.route('/profile/<typeUser>/<name>', methods=['GET', 'POST'])
@login_required
def profile(typeUser, name):
    if request.method == "POST":
        if typeUser == "centre":
            centre = centreManager.searchHealthCentresByName(name)
            return render_template("profile.html", error = None, loggedInUser=current_user.get_id(), option="healthCentre", centre=centre[0])
        elif typeUser == "provider":
            if name == current_user.get_id():
                return render_template("profile.html", error = None, loggedInUser=current_user.get_id(), option="self")
            provider = userManager.searchID(name)
            return render_template("profile.html", error = None, loggedInUser=current_user.get_id(), option="provider", provider=provider[0])
        elif typeUser == "patient":
            if name == current_user.get_id():
                return render_template("profile.html", error = None, loggedInUser=current_user.get_id(), option="self")
            patient = userManager.searchPatient(name)
            return render_template("profile.html", error = None, loggedInUser=current_user.get_id(),  option="patient", patient=patient[0])

        # option = request.form["option"]
        # name = request.form["name"]
        # typeCentre = request.form["typeCentre"]
        # phone = request.form["phone"]
        # suburb = request.form["suburb"]
        # abn = request.form["abn"]
        # if option == "healthCentre" or option == "suburb":
        #     centre = centreManager.searchHealthCentresByName(name)
        #     return render_template("profile.html",option=option, typeCentre=typeCentre, name=name, abn=abn,
        #     phone=phone, suburb=suburb, rating = 0, providers=centre[0].getProviders())
        # elif option == "healthProvider":
        #     email = request.form["user"]
        #     return render_template("profile.html",option=option, email=email, typeCentre=typeCentre, name=name, abn=abn,
        #     phone=phone, suburb=suburb, rating = 0)
        # elif option == "service":
        #     email = request.form["user"]
        #     service = request.form["service"]
        #     return render_template("profile.html",option=option, email=email, service=service, typeCentre=typeCentre, name=name, abn=abn,
        #     phone=phone, suburb=suburb, rating = 0)
    return render_template("profile.html", loggedInUser=current_user.get_id(), option="self")

@app.route('/update/<name>', methods=['GET', 'POST'])
@login_required
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
            new_expertise = request.form["new_expertise"]
            if new_expertise != "":
                current_user.set_expertise(new_expertise)

        # write all data to files
        saveData(centreManager, userManager, appointmentManager)
        return render_template("profile.html", loggedInUser=current_user.get_id(), option="self")
    return render_template("update_profile.html", loggedInUser=current_user.get_id())

def getTimes(email):
    provider = userManager.getID(email)
    start_time = provider.get_startWorkingHours()
    end_time = provider.get_endWorkingHours()
    fmt='%H:%M'
    time=datetime.datetime.strptime(start_time,fmt)
    end=datetime.datetime.strptime(end_time,fmt)
    min30=datetime.timedelta(minutes=30)
    times=[]
    while time < end:
        times.append('%s-%s' % ( time.strftime(fmt), (time+min30).strftime(fmt)))
        time+=min30

    return times

@app.route('/book/<email>', methods=['GET', 'POST'])
@login_required
def book(email):
    times = getTimes(email)

    return render_template('book.html', loggedInUser=current_user.get_id(), times=times, name=email, error="")

@app.route('/bookAppointment/<email>', methods=['GET', 'POST'])
@login_required
def bookAppointment(email):
    # find provider and add the appointment
    # find current user logged in and add the appointment
    # def addAppointment(provider_email, patient_email, date, time):
    # addAppointment(request.form['email'])

    if request.form['date'] == "": # empty date field
        times = getTimes(email)
        return render_template('book.html', loggedInUser=current_user.get_id(), times=times, name=email, error="Error: Enter a date!")

    success = appointmentManager.addAppointment(userManager, email, current_user.get_id(), str(request.form['time']), request.form["date"], request.form['bookReason'])

    if success == "Time Slot Taken": # no time slots available
        times = getTimes(email)
        return render_template('book.html', loggedInUser=current_user.get_id(), times=times, name=email, error="Error: Time slot taken!")
    elif success == "Date in the past":
        times = getTimes(email)
        return render_template('book.html', loggedInUser=current_user.get_id(), times=times, name=email, error="Error: Date in the past!")
    elif success == "Provider making appointment":
        times = getTimes(email)
        return render_template('book.html', loggedInUser=current_user.get_id(), times=times, name=email, error="Error: Provider cannot make appointment with provider")


    saveData(centreManager, userManager, appointmentManager)
    return render_template('index.html', loggedInUser=current_user.get_id(), booked=True)

@app.route('/book', methods=['POST'])
@login_required
def reason():
    bookReason = request.form['bookReason']
    processedText = text.upper()
    return processedText

@app.route('/appointments', methods=['GET', 'POST'])
@login_required
def showBookings():
    if request.method == 'POST':
        appointmentIndex = int(request.form['appointmentIndex'])
        appointmentNotes = str(request.form['notes'])
        appointmentPrescribedMedicine = str(request.form['prescribedMedicine'])
        currentAppointment = current_user.getSpecificAppointment(appointmentIndex)
        currentAppointment.notes = appointmentNotes
        currentAppointment.prescribedMedicine = appointmentPrescribedMedicine
        currentAppointment.accessed = True
        patient = userManager.getID(currentAppointment.patient)

        #if a referral was made, we want to store the patient in the list of referrals for the specialist chosen
        if current_user.getProfession() == "GP":
            newReferral = str(request.form['radioRefer'])
            if newReferral != "NoRefer":
                patient.addReferral(newReferral)
        saveData(centreManager, userManager, appointmentManager)
        return render_template('index.html', loggedInUser=current_user.get_id(), updated=True)

    # sorted function converts the date attribute in the appointment to a "datetime" object,
    # which then can be used to compare two dates
    # the sorted function returns the new sorted list, and the lambda function is used to get the date attribute
    return render_template('appointments.html', loggedInUser=current_user.get_id(), appointments=appointmentManager.getAppointments(current_user))

#current_user.getSpecificAppointment(appointmentIndex)

@app.route('/accessedAppointment', methods=['GET', 'POST'])
@login_required
def accessedAppointment():
    if request.method == 'POST':

        appointmentIndex = (int(request.form['appointment']) - 1)
        # Get patient appointments
        patient_id = current_user.getSpecificAppointment(appointmentIndex).patient
        patient = userManager.getID(patient_id)
        appointments = appointmentManager.getAppointments(patient)


        specialists = userManager.searchExpertise("")
        saveData(centreManager, userManager, appointmentManager)
        return render_template('accessedAppointment.html', loggedInUser=current_user.get_id(), 
            appointment=current_user.getSpecificAppointment(appointmentIndex), 
            appointmentIndex=appointmentIndex, appointments=appointments, specialists = specialists)
    return render_template('accessedAppointment.html', loggedInUser=current_user.get_id())

@app.route('/profile/updateRatings/<typeUser>/<name>', methods=['POST'])
@login_required
def updateRatings(name, typeUser):
    if typeUser == 'centre':
        centre = centreManager.searchHealthCentresByName(name)[0]
        centre.updateRating(current_user.get_id(), int(request.form['updateRatingBox']))
        saveData(centreManager, userManager, appointmentManager)
        return redirect(url_for('profile', loggedInUser=current_user.get_id(), typeUser=typeUser, name=name), code=307)
    elif typeUser == 'provider':
        if appointmentManager.appointmentCompleted(current_user, name) == True:
            provider = userManager.getID(name)
            provider.updateRating(current_user.get_id(), int(request.form['updateRatingBox']))
            saveData(centreManager, userManager, appointmentManager)
            return redirect(url_for('profile', loggedInUser=current_user.get_id(), typeUser=typeUser, name=name), code=307)
        else:
            provider = userManager.searchID(name)
            return render_template("profile.html", loggedInUser=current_user.get_id(), option="provider", provider=provider[0],
                error="No History with this provider! No Rating can be provided.")


@app.route('/history', methods=['GET'])
@login_required
def history():
    return render_template('appointment_history.html', loggedInUser=current_user.get_id(), appointments=appointmentManager.getAppointments(current_user))

@app.route('/historyDetails', methods=['GET', 'POST'])
@login_required
def historyDetails():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        user = userManager.getID(request.form['user'])

        appointment = appointmentManager.getAppointmentUsingDate(user, date, time) #the appointment history instance

        return render_template('appointmentDetails.html', loggedInUser=current_user.get_id(), appointment=appointment)

@app.route('/viewHistoryFromAppointment', methods=['GET', 'POST'])
@login_required
def viewHistoryFromAppointment():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        user = userManager.getID(request.form['user'])

        currentDate = request.form['currentDate']
        currentTime = request.form['currentTime']
        currentUser = userManager.getID(request.form['currentPatient'])

        activeAppointment = int(request.form['activeAppointment']) #is the appointment currently happening boolean
        appointment = appointmentManager.getAppointmentUsingDate(user, date, time) #the appointment history instance
        currentAppointment = appointmentManager.getAppointmentUsingDate(currentUser, currentDate, currentTime) #the appointment that the edit is happening from

        return render_template('appointmentDetails.html', loggedInUser=current_user.get_id(), appointment=appointment, activeAppointment=activeAppointment, currentAppointment=currentAppointment)
    return render_template('appointmentDetails.html', loggedInUser=current_user.get_id())

@app.route('/updateHistory', methods=['GET', 'POST'])
@login_required
def updateHistory():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        user = userManager.getID(request.form['patient'])

        appointment = appointmentManager.getAppointmentUsingDate(user, date, time) #the appointment history instance

        currentDate = request.form['currentDate']
        currentTime = request.form['currentTime']
        currentPatient = userManager.getID(request.form['currentPatient'])

        currentAppointment = appointmentManager.getAppointmentUsingDate(currentPatient, currentDate, currentTime) #the appointment that the edit is happening from
        return render_template('update_history.html', loggedInUser=current_user.get_id(), appointment=appointment, currentAppointment=currentAppointment)
    return render_template('update_history.html', loggedInUser=current_user.get_id())

@app.route('/successfulUpdate', methods=['GET', 'POST'])
@login_required
def successfulUpdate():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        user = userManager.getID(request.form['patient'])

        appointment = appointmentManager.getAppointmentUsingDate(user, date, time)

        currentDate = request.form['currentDate']
        currentTime = request.form['currentTime']
        currentPatient = userManager.getID(request.form['currentPatient'])
        currentAppointment = appointmentManager.getAppointmentUsingDate(currentPatient, currentDate, currentTime) #the appointment that the edit is happening from

        addedNotes = str(request.form['addedNotes'])
        addedMedicine = str(request.form['addedMedicine'])

        appointmentManager.updateAppointment(appointment, addedNotes, addedMedicine)

        currentAppointment.accessed = True
        currentAppointment.notes = appointment.notes
        currentAppointment.prescribedMedicine = appointment.prescribedMedicine

        saveData(centreManager, userManager, appointmentManager)
        return render_template('appointmentDetails.html', loggedInUser=current_user.get_id(), appointment=appointment)
    return render_template('index.html', loggedInUser=current_user.get_id())
