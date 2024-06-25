"""
This file contains view functions for the login, register and index
pages, subsequent functions after that are for user authentication,
which is used in the boards application.
"""

from django.shortcuts import render, redirect
from .forms import CreateUser, Login
from .models import Login as login_table
import uuid


def login(request):
    """Login page, POST requests check for a login form and
    its validity, then gives the user a session_id cookie
    if their login is valid"""

    if request.method == "POST":
        form = Login(request.POST)

        if form.is_valid():
            # Get user from form
            username = form.cleaned_data.get("username")

            # Generate UUID
            session_id = uuid.uuid4()

            # Write UUID to sessionID in models
            login_data = login_table.objects.get(username=username)
            login_data.session_id = session_id
            login_data.save()

            # Give sessionID to client as cookie
            response = redirect("dashboard")
            response.set_cookie("session_id", session_id)

            return response

    else:
        form = Login()

    context = {"form": form}
    context["logged_in"] = authenticate(request)
    return render(request, "login.html", context)


def register(request):
    """Page that allows user to register, POST requests
    check for a form and it's validity and then creates
    a user based on that data"""

    if request.method == "POST":
        form = CreateUser(request.POST)

        # Check form is valid
        if form.is_valid():
            # Fetch data from forms
            cd = form.cleaned_data
            username = cd.get("username")
            password = cd.get("password")

            # Create user in models
            new_user = login_table(username=username, password=password)
            new_user.save()

            return redirect("login")

    else:
        form = CreateUser()

    context = {"form": form}
    context["logged_in"] = authenticate(request)
    return render(request, "register.html", context)


def index(request):
    """Small landing page with nothing important"""
    context = {"logged_in": authenticate(request)}

    return render(request, "index.html", context)


def authenticate(request) -> bool:
    """Checks session_id against database from view request"""
    session_id = request.COOKIES.get("session_id")
    if session_id is None:
        return False
    response = login_table.objects.filter(session_id=session_id).exists()
    print(response)
    return response


def get_user(request) -> Login:
    """Gets login object for use from view request"""
    session_id = request.COOKIES.get("session_id")
    response = login_table.objects.get(session_id=session_id)
    return response
