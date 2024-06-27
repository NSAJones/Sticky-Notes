"""This file tests functionality related to boards, sticky notes and
invites"""

from django.test import TestCase
from django.urls import reverse
from login.models import Login
from .models import Invite,StickyNote,Board
from uuid import uuid4
from http.cookies import SimpleCookie

class BoardTest(TestCase):
  """Tests Board app models and views"""

  def setUp(self) -> None:
    """Create test user and test board along with login and invite"""

    self.session_id = uuid4()

    # Create user
    self.test_user = Login.objects.create(username="test-username",
                                     password="test-password",
                                     session_id=self.session_id)
    
    # Create board owned by user
    test_board = Board.objects.create(name="test-board",
                                      owner=self.test_user)
    
    # Create sticky owned by board
    StickyNote.objects.create(creator=self.test_user,
                              board=test_board,
                              text="test-description")
    
    # Set client cookie to allow login
    self.client.cookies = SimpleCookie({"session_id":self.session_id})

    # Create invite user
    self.session_id2 = uuid4()
    self.invite_user = Login.objects.create(username="invite-test",
                                            password="invite-password",
                                            session_id=self.session_id2)
    
    # Create an invite from test user to invite user for test board
    invite = Invite.objects.create(username=self.invite_user,
                                   board=test_board)
    
  def test_dashboard_view(self):
    """Checks that data from the models is pulled correctly into the 
    dashboard view"""
    response = self.client.get(reverse("dashboard"))

    # Check board name is shown
    self.assertContains(response,"test-board",status_code=200)

    # Check username is shown
    self.assertContains(response,"test-username",status_code=200)
  
  def test_board_view(self):
    """Checks that data from the models is pulled correctly into the
    board view"""

    response = self.client.get(reverse("board",kwargs={"board_id":1}))

    # Check sticky note content is shown
    self.assertContains(response,"test-description",status_code=200)

  def test_invite_view(self):
    """Checks that the owner can see invited users"""
    response = self.client.get(reverse("invite",kwargs={"board_id":1}))

    # Check username is shows of invited user
    self.assertContains(response,"invite-test",status_code=200)

  
  def test_model_cascade(self):
    """Checks that deleting a user properly cascades and deletes their
    boards too"""

    # Delete user
    self.test_user.delete()

    # Check for board at id 1, should return false
    self.assertFalse(Board.objects.filter(id=1).exists())
  
  def test_board_invite_view(self):
    """Checks that users invited to a board can access it"""

    # Change session_id cookie to invite user's session_id
    self.client.cookies = SimpleCookie({"session_id":self.session_id2})

    response = self.client.get(reverse("board",kwargs={"board_id":1}))

    # Check sticky note content is shown
    self.assertContains(response,"test-description",status_code=200)
  
  


  

    
    
