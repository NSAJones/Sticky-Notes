"""
This file includes models for creating Boards, adding sticky notes to
those boards and inviting other users to those boards
"""

from django.db import models
from login.models import Login


class Board(models.Model):
    """Model for storing boards and their owners"""

    name = models.CharField(max_length=50)
    owner = models.ForeignKey(Login, on_delete=models.CASCADE)


class StickyNote(models.Model):
    """Model for storing sticky notes and who and where
    they belong to"""

    creator = models.ForeignKey(Login, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    text = models.TextField(max_length=600)


class Invite(models.Model):
    """Model for storing invites from the owner of a board
    to other users"""

    username = models.ForeignKey(Login, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
