from userManager import UserManager
from centreManager import CentreManager
from appointmentManager import AppointmentManager
import pytest
class Tests(object):
	def setup_method(self):
		self.centreManager = CentreManager()
		self.userManager = UserManager(self.centreManager)
		self.appointmentManager = AppointmentManager()
		self.centreManager.addProviders(self.userManager)

# (1) BOOK AN APPOINTMENT
	# 4 
			
	# (i) Testing that the appointment added is in the patient class and the provider class
	def test_book_appointment(self): ##
		self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"jack@gmail.com",  "00.00-00.30", "12/31/2018","Biopsy Required")

		# Check that the appointment is in the provider class
		provider = self.userManager.getID("toby@gmail.com")
		providerAppointment = provider.getSpecificAppointment(0)
		assert(providerAppointment.provider == "toby@gmail.com")
		assert(providerAppointment.patient == "jack@gmail.com")
		assert(providerAppointment.date == "12/31/2018")
		assert(providerAppointment.time == "00.00-00.30")
		assert(providerAppointment.reason == "Biopsy Required")
		
		# Check that the appointment is in the patient class
		patient = self.userManager.getID("jack@gmail.com")
		patientAppointment = patient.getSpecificAppointment(0)
		assert(patientAppointment.provider == "toby@gmail.com")
		assert(patientAppointment.patient == "jack@gmail.com")
		assert(patientAppointment.date == "12/31/2018")
		assert(patientAppointment.time == "00.00-00.30")
		assert(patientAppointment.reason == "Biopsy Required")  
		
	# (ii) Check that booking an appointment in the same timeslot does not work
	def test_book_same_time_slot_appointment(self): ##
		self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"jack@gmail.com",  "00.00-00.30", "12/31/2018", "Influenza")

		status = self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"hao@gmail.com",  "00.00-00.30", "12/31/2018","Same Time slot")

		assert(status == "Time Slot Taken")
	
	# (iii) provider makes an appointment for himself/herself
	def test_provider_makes_appointment(self): ##
		status = self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"toby@gmail.com", "00.00-00.30", "12/1/2018", "Arthiritis")

		assert(status == "Provider making appointment")

	# (additional) Check that you cannot book an appointment in the past
	def test_book_past_appointment(self): ##
		status = self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"jack@gmail.com",  "00.00-00.30", "09/24/2018","Constipation")

		assert(status == "Date in the past")

# (2) VIEW PATIENT HISTORY	
	# 2	
	# testing that the history is saved and can be accessed
	def test_get_appointment_history(self): ##
		self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"jack@gmail.com",  "00.00-00.30", "12/31/2018", "High Blood Pressure")

		self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"hao@gmail.com",  "00.30-01.00", "12/31/2018","Vomiting")

		user = self.userManager.getID("toby@gmail.com")
		assert(len(self.appointmentManager.getAppointments(user)) == 2) 

	# test updating with multiple people booking and 2 wanting the same time
	def multiple_appointments_clash(self):
		self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"jack@gmail.com",  "04.00-04.30", "12/31/2018","Biopsy Required")
		
		self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com", 
			"tom@gmail.com", "00.30-01.00", "12/31/2018", "Mole on foot")

		# this appointment has the same time and date as the previous appointment   
		clash = self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"hao@gmail.com",  "00.30-01.00", "12/31/2018","Mole on foot")
			
		assert(clash == "Time Slot Taken")

		user = self.userManager.getID("toby@gmail.com") 
		assert(len(self.appointmentManager.getAppointments(user)) == 1)	 
	
# (3) MANAGE A PATIENT HISTORY
	# 4	
	# test to ensure the provider can update appointment with notes and medicine prescribed 
	def notes_and_medicine(self):
		self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"jack@gmail.com",  "09.00-09.30", "11/23/2018","Biopsy Required")    
			
		user = self.userManager.getID("jack@gmail.com")
		appointment = self.appointmentManager.getAppointmentUsingDate(user, 
			"11/23/2018", "09.00-09.30")
			
		notes = "Baby Shark"
		medicine = "Doo doo doo doo"
		
		self.appointmentManager.updateAppointment(appointment, notes, medicine)
		
		assert(appointment.notes == "Baby Shark")
		assert(appointment.prescribedMedicine == "Doo doo doo doo")	 
		
	# updating notes from a previously inputted notes and medicine
	def test_update_appointment(self): ##
		self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"jack@gmail.com",  "09.00-09.30", "11/23/2018", "Biopsy Required")

		user = self.userManager.getID("jack@gmail.com")
		appointment = self.appointmentManager.getAppointmentUsingDate(user, 
			"11/23/2018", "09.00-09.30")
			
		appointment.notes = "This person did not require a doctor"
		appointment.prescribedMedicine = "Obecalp pills"
		
		newNotes = "I was wrong"
		newMedicine = "Sugar"
		
		self.appointmentManager.updateAppointment(appointment, newNotes, newMedicine)
		assert(appointment.notes == "This person did not require a doctor\nI was wrong")
		assert(appointment.prescribedMedicine == "Obecalp pills\nSugar")
		
	# updating notes then realising no updates are needed -> NULL submission          
	def test_update_appointment_with_nothing(self): ##
		self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"jack@gmail.com",  "08.00-08.30", "11/23/2018", "Biopsy Required")

		user = self.userManager.getID("jack@gmail.com")
		appointment = self.appointmentManager.getAppointmentUsingDate(user, 
			"11/23/2018", "08.00-08.30")
		appointment.notes = "This person did not require a doctor"
		appointment.prescribedMedicine = "Obecalp pills"
		
		newNotes = ""
		newMedicine = ""
		
		self.appointmentManager.updateAppointment(appointment, newNotes, newMedicine)
		assert(appointment.notes == "This person did not require a doctor\n")
		assert(appointment.prescribedMedicine == "Obecalp pills\n")
			
	# Test getting the history with an email that does not have any appointments    
	def test_get_wrong_id_history(self): ##
		self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"jack@gmail.com", "00.00-00.30", "12/31/2018", "Biopsy Required")

		self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com", 
			"hao@gmail.com", "00.30-01.00", "12/31/2018", "Mole on foot")
		
		user = self.userManager.getID("gary@gmail.com")
		assert(len(self.appointmentManager.getAppointments(user)) == 0)
		
		
