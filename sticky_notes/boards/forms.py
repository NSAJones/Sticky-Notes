from typing import Any
from django import forms
from django.core.exceptions import ValidationError


class CreateBoard(forms.Form):
    """form for creating boards"""
    name = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder":"new board name",
               "required":"required"
               }
    ))

class SaveBoard(forms.Form):
    pass
