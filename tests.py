import unittest
import pytest
from routes import login
from flask.ext.testing import TestCase
# Currently fiddling around with test cases to fully understand how to implement
# https://github.com/realpython/discover-flask/blob/master/tests/base.py
# https://github.com/realpython/discover-flask/blob/master/tests/base.py
# structure based on above links

class my_test(TestCase):
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

class test_cases(my_test):
    
    # tests that flask is set up correct
    def test_user_login(self):
        #login_user(user)        
        #response = self.client.get('/login', content_type='html/text')
        #self.assertEqual(response.status_code, 200)
        
    # Ensure that main page requires user login
    def test_main_route_requires_login(self):
        # response = self.client.get('/', follow_redirects=True)
        # the function supposedly tests for the texts on the screen
        # self.assertIn(b'Log-in to your account', response.data)
        
    # Ensure that welcome page loads
    def test_welcome_route_works_as_expected(self):
    
    
    def test_book_an_appointment(self):
    
    
    def test_view_patient_history(self):
    
    
    def test_manage_patient_history(self):
    
    
    
if __name__ == '__main__':
    unittest.main()
        
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
   
