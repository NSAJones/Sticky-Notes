from django.shortcuts import render,HttpResponse,redirect
from login.views import authenticate,get_user
from login.models import Login
from .models import Board,StickyNote,Invite
from .forms import CreateBoard,InviteUser
import json

def dashboard(request):
    """Page that shows data to the user about their profile,
    user has to be logged in. Allows POST requests from the
    following submit buttons:

    create
        Used to create a board, uses a form for the name of
        the new board to be created.
    delete_board
        Tied to a specific board, will delete the board by id
    user_delete
        Will delete the user and all of their boards (through
        cascade)
    log_out
        Logs the user out by removing their session_id
    """

    if not authenticate(request):
        return redirect("login")
    
    user = get_user(request)
    
    if request.method == "POST":
        # Create board
        if request.POST.get("create"):
            form = CreateBoard(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get("name")

                # Create new board
                b = Board(name=name,owner=user)
                b.save()

                print(form.cleaned_data)

        # Delete board
        elif request.POST.get("delete_board"):
            id = request.POST.get("id")[0]
            board_delete = Board.objects.get(id=id)
            board_delete.delete()

        # Delete user
        elif request.POST.get("user_delete"):
            user.delete()
            # Redirect user to login and delete session_id
            response = redirect("login")
            response.delete_cookie("session_id")
            return response
        
        # Log user out
        elif request.POST.get("log_out"):
            # Make session_id blank in models
            Login.objects.filter(
                username=user.username).update(session_id=None)
            
            # Delete session_id cookie
            response = redirect("login")
            response.delete_cookie("session_id")
            return response

            


    owned = []
    invited = []

    # Get boards user owns
    if Board.objects.filter(owner=user).exists():
        owned = Board.objects.filter(owner=user)
    
    # Get boards user is invited to
    if Invite.objects.filter(username=user).exists():
        invited = Invite.objects.filter(username=user)
    
    form = CreateBoard()

    context={"form":form,"owned":owned,"invited":invited,"user":user.username}
    context["logged_in"] = authenticate(request)
    return render(request,"dashboard.html",context)
    

def board(request,board_id):
    """Page that shows sticky notes and allows users to edit 
    them. Requires the user to be logged in. Has the 
    following POST scenarios:

    ajax
        When the save button is pressed, an ajax function is
        triggered which fetches all the data from the sticky
        notes and sends it
    new_note
        Creates a new note when a submit button is pressed
    delete_note.x
        When an image button is pressed on a sticky note,
        deletes that note, has an id attached 
    
    """

    # Check authentication
    if not authenticate(request):
        return redirect("login")
    
    # Check user is invited/owner
    user = get_user(request)
    
    is_owner = Board.objects.filter(owner=user,id=board_id).exists()
    is_invited = Invite.objects.filter(board=board_id,username=user).exists()
    if not (is_owner or is_invited):
        return redirect("dashboard")
    
    board_obj = Board.objects.get(id=board_id)

    context = {}

    # Check for POST
    if request.method == "POST":
        print(request.POST)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        # Save notes
        if is_ajax:
            note_list = json.load(request)["notes"]
            for n in note_list:
                StickyNote.objects.filter(id=n["id"]).update(text=n["text"])

        # Create new note
        elif request.POST.get("new_note"):
            new_note = StickyNote(creator=user,board=board_obj,text="")
            new_note.save()

        # Delete existing note
        elif request.POST.get("delete_note.x"):
            id = request.POST.get("id")
            StickyNote.objects.filter(id=id).delete()


    notes = StickyNote.objects.filter(board=board_id)
    context["notes"] = notes
    context["logged_in"] = authenticate(request)
    context["board_id"] = board_id
    
    return render(request,"board.html",context)



def invite(request,board_id):
    """Page available only to the owner of the board, allows
    an invite to be sent to another user, as well as remove
    existing invites. Has the following POST scenarios:

    invite
        Checks the user is valid and if so creates an invite
    delete
        Deletes a specific user, an invite id is attached
    """
    if not authenticate(request):
        return redirect("login")
    
    user = get_user(request)
    board_row = Board.objects.get(id=board_id)
    is_owner = Board.objects.filter(owner=user,id=board_id).exists()

    if not is_owner:
        return redirect("dashboard")

    context = {}
    form = InviteUser(board_id=board_id)

    if request.method == "POST":
        # Create Invite
        if request.POST.get("invite"):
            form = InviteUser(request.POST,board_id=board_id)
            if form.is_valid():
                user_str = form.cleaned_data.get("username")
                user_row = Login.objects.get(username=user_str)
                Invite(username=user_row,board=board_row).save()
        
        # Delete Invite
        if request.POST.get("delete"):
            invite_id = request.POST.get("id")
            Invite.objects.get(id=invite_id).delete()


    invites = Invite.objects.filter(board=board_row)
    context["form"] = form
    context["invites"] = invites
    context["board_id"] = board_id
    context["logged_in"] = authenticate(request)
    
    return render(request,"invite.html",context)

