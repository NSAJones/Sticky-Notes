from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from .models import Invite,Board
from login.models import Login


class CreateBoard(forms.Form):
    """form for creating boards"""
    name = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder":"new board name",
               "required":"required"
               }
    ))

class InviteUser(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder":"username",
               "required":"required"
               }
    ))

    def __init__(self,*args,**kwargs):
        self.board_id = kwargs.pop("board_id")
        super(InviteUser,self).__init__(*args,**kwargs)

    def clean(self) -> dict[str, Any]:

        cd = self.cleaned_data

        # Check username exists
        if not Login.objects.filter(username=cd.get("username")).exists():
            raise ValidationError("Username does not exist")
        
        username_row = Login.objects.get(username=cd.get("username"))
        board_row = Board.objects.get(id=self.board_id)

        # Check user isn't invited already
        if Invite.objects.filter(username=username_row,board=board_row).exists():
            raise ValidationError("User already invited")

        return super().clean()