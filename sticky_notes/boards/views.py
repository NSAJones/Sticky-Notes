from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from login.views import authenticate,get_user
from .models import Board,StickyNote,Invite
from .forms import CreateBoard

# Create your views here.
def dashboard(request):

    if not authenticate(request):
        return HttpResponseRedirect("login")
    
    user = get_user(request)
    
    if request.method == "POST":
        # Create board
        submit_name = request.method.get()
        if submit_name == "create":
            form = CreateBoard(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get("name")

                # Create new board
                b = Board(name=name,owner=user)
                b.save()

                print(form.cleaned_data)
        
        # Delete board
        if submit_name.split("_")[0] == "delete":
            id = submit_name.split("_")[1]
            form = CreateBoard(request.POST)

            if form.is_valid():
                name = form.cleaned_data.get("name")

                # Create new board
                b = Board(name=name,owner=user)
                b.save()

                print(form.cleaned_data)

    owned = []
    invited = []

    # Get boards user owns
    if Board.objects.filter(owner=user).exists():
        owned = Board.objects.filter(owner=user)
    
    # Get boards user is invited to
    if Invite.objects.filter(username=user).exists():
        invited = Invite.objects.filter(username=user)
    
    form = CreateBoard()

    context={"form":form,"owned":owned,"invited":invited}
    return render(request,"dashboard.html",context)
    

def board(request,board_id):
    # Check authentication
    if not authenticate(request):
        return HttpResponseRedirect("login")
    
    # Check user is invited/owner
    user = get_user()
    is_owner = Board.objects.filter(owner=user,id=board_id).exists
    is_invited = Invite.objects.filter(board=board_id,username=user).exists
    if not (is_owner or is_invited):
        return HttpResponseRedirect("dashboard")

    context = {}

    # Check for POST
    if request.method == "POST":
        if request.post.get("save"):
            print(request)

    else:
        notes = StickyNote.objects.filter(board=board_id)
        
    
    return render(request,"board.html",context)


        


def invite(request,board_id):
    pass

