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
#this will be where tests for user stories are conducted
# According to the google doc
    # 1: Book and Appointment
    # US7
    # "User-Story Description:
        # As a patient, I want to book an appointment so I can receive healthcare service easily
        # Acceptance Criteria:
            # Enter required information including Medicare number into a form
            # Be able to book an appointment through a healthcare provider?s or centre?s profile page
            # Have an option of 48 equally sized time slots, each of which is 30 minutes long
            # Be able to enter brief information for the appointment
            # Be able to display a confirmation that the appointment has been booked to the user          

    # 2: View Patient History
    # US13
    # User-Story Description:
        # As a patient, I want to be able to view my own appointments history so I can easily access which appointments I have recently attended
        # Acceptance Criteria:
            # The list of appointments should have links to the profile pages of the corresponding health provider and healthcare centre
            # The list of appointments should be chronological and listed with the date of appointment
            
    # US15
    # User-Story Description:
        # As a healthcare provider, I want to be able to view a patient?s appointment history so I can consult with the patient accordingly
        # Acceptance Criteria:
            # The patient?s appointment history should be accessed through their profile page
            # A description of what occured in a specific appointment should be viewable, including any medication prescribed and notes taken at the previous visit
  
    # 3: Manage a patient history
   

    # 	def addAppointment(self, userManager, provider_email, patient_email, date, time, reason):

    # Testing that the appointment added is in the patient class and the provider class
	def test_book_appointment(self):
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

	# Check that booking an appointment in the same timeslot does not work
	def test_book_same_time_slot_appointment(self):
		self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"jack@gmail.com",  "00.00-00.30", "12/31/2018", "Biopsy Required")

		status = self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"hao@gmail.com",  "00.00-00.30", "12/31/2018","Same Time slot")

		assert(status == "Time Slot Taken")

	# Check that you cannot book an appointment in the past
	def test_book_past_appointment(self):
		status = self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"jack@gmail.com",  "00.00-00.30", "09/24/2018","Biopsy Required")

		assert(status == "Date in the past")

	# provider makes an appointment for himself/herself
	def test_provider_makes_appointment(self):
		status = self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"toby@gmail.com", "00.00-00.30", "12/1/2018", "Biopsy Required")

		assert(status == "Provider making appointment")

	# Test that getting the history works
	def test_get_appointment_history(self):
		self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"jack@gmail.com",  "00.00-00.30", "12/31/2018", "Biopsy Required")

		self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"hao@gmail.com",  "00.30-01.00", "12/31/2018","Mole on foot")

		user = self.userManager.getID("toby@gmail.com")
		assert(len(self.appointmentManager.getAppointments(user)) == 2)

	# Test getting the history with an email that does not have any appointments
	def test_get_wrong_id_history(self):
		self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"jack@gmail.com",  "00.00-00.30", "12/31/2018", "Biopsy Required")

		self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"hao@gmail.com",  "00.30-01.00", "12/31/2018","Mole on foot")

		user = self.userManager.getID("gary@gmail.com")
		assert(len(self.appointmentManager.getAppointments(user)) == 0)

	# Test updating an appointment
	def test_update_appointment(self):
		self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"jack@gmail.com",  "00.00-00.30", "12/31/2018", "Biopsy Required")

		# def getAppointmentUsingDate(self, user, date, time)
		user = self.userManager.getID("jack@gmail.com")
		appointment = self.appointmentManager.getAppointmentUsingDate(user, "12/31/2018", "00.00-00.30")
		appointment.notes = "Original Notes"
		appointment.prescribedMedicine = "Original Medicine"
		notes = "Updated Notes"
		medicine = "Updated Medicine"
		self.appointmentManager.updateAppointment(appointment, notes, medicine)
		assert(appointment.notes == "Original Notes\nUpdated Notes")
		assert(appointment.prescribedMedicine == "Original Medicine\nUpdated Medicine")

	# Test updating history with nothing
	def test_update_appointment_nothing(self):
		self.appointmentManager.addAppointment(self.userManager, "toby@gmail.com",
			"jack@gmail.com",  "00.00-00.30", "12/31/2018", "Biopsy Required")

		# def getAppointmentUsingDate(self, user, date, time)
		user = self.userManager.getID("jack@gmail.com")
		appointment = self.appointmentManager.getAppointmentUsingDate(user, "12/31/2018", "00.00-00.30")
		appointment.notes = "Original Notes"
		appointment.prescribedMedicine = "Original Medicine"

		self.appointmentManager.updateAppointment(appointment, "", "")
		assert(appointment.notes == "Original Notes\n")
		assert(appointment.prescribedMedicine == "Original Medicine\n")

	