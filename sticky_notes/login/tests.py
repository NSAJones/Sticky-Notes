"""This file tests the login forms, as there is only one model in this
app, the model is not tested here, however it is used in the boards
app tests"""

from django.test import TestCase
from django.urls import reverse
from .models import Login as login_table
from .forms import CreateUser,Login
from http import HTTPStatus

class LoginFormTest(TestCase):
    """This class tests login forms"""
    
    def setUp(self) -> None:
        """Creates a test user"""

        login_table.objects.create(username="test",
                                   password="test")
    
    def test_register_form(self) -> None:
        """Tests register form validations"""

        # Test valid register form
        data = {"username":"valid",
                "password":"valid",
                "conf_password":"valid"
                }
        form = CreateUser(data=data).is_valid()
        self.assertTrue(form)

        # Test invalid register (user already exists)
        data = {"username":"test",
                "password":"test",
                "conf_password":"test"
                }
        form = CreateUser(data=data).is_valid()
        self.assertFalse(form)

        # Test invalid register (second password invalid)
        data = {"username":"valid",
                "password":"valid",
                "conf_password":"invalid"
                }
        form = CreateUser(data=data).is_valid()
        self.assertFalse(form)
    
    def test_login_form(self) -> None:
        """Tests login form validation"""

        # Test valid credentials
        data = {"username":"test",
                "password":"test",
                }
        form = Login(data=data).is_valid()
        self.assertTrue(form)

        # Test valid credentials
        data = {"username":"invalid",
                "password":"invalid",
                }
        form = Login(data=data).is_valid()
        self.assertFalse(form)




    
