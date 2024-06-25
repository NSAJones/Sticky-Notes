"""
This file has urls for the login,register and index page pulled from
this application's view
"""

from django.urls import path
from .views import login, register, index

urlpatterns = [
    path("login", login, name="login"),
    path("register", register, name="register"),
    path("", index, name="index"),
]
