from django.db import models
from login.models import Login

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(Login, on_delete=models.CASCADE)


class StickyNote(models.Model):
    creator = models.ForeignKey(Login, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    text = models.TextField(max_length=600)


class Invite(models.Model):
    username = models.ForeignKey(Login, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)


