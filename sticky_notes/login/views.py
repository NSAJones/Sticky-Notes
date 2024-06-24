from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .forms import CreateUser,Login
from .models import Login as login_table
import uuid

def login(request):
    
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
            response = HttpResponse("Login Successful")
            response.set_cookie("session_id",session_id)

            return response
            
    else:
        form = Login()
        
    context = {"form":form}
    context["logged_in"] = authenticate(request)
    return render(request, "login.html",context)

def register(request):
    if request.method == "POST":
        form = CreateUser(request.POST)

        # Check form is valid
        if form.is_valid():
            # Fetch data from forms
            cd = form.cleaned_data
            username = cd.get("username")
            password = cd.get("password")

            # Create user in models
            new_user = login_table(
                username = username,
                password = password
            )
            new_user.save()

            return HttpResponseRedirect("login")
        
    else:
        form = CreateUser()
        
    context = {"form":form}
    context["logged_in"] = authenticate(request)
    return render(request, "register.html",context)

def index(request):
    context = {"logged_in":authenticate(request)}

   
    return render(request,"index.html",context)

def authenticate(request):
    """Checks session_id against database"""
    session_id = request.COOKIES.get("session_id")
    response = login_table.objects.filter(session_id=session_id).exists()
    return response

def get_user(request):
    session_id = request.COOKIES.get("session_id")
    response = login_table.objects.get(session_id=session_id)
    return response