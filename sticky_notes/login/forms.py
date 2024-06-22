from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from .models import Login as login_table


class CreateUser(forms.Form):
    """Form for creating users"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    conf_password = forms.CharField(widget=forms.PasswordInput(),
                                    label="confirm password")
    
    def clean(self) -> dict[str, Any]:
        """Check form is valid"""

        cd = self.cleaned_data
        usr = cd.get("username")
        pswrd= cd.get("password")
        conf_pswrd = cd.get("conf_password")

        # Check confirmation password is equal to normal password
        if pswrd != conf_pswrd:
            raise ValidationError(
                "Password and confirmation password not equal"
            )
        
        # Check username isn't taken already
        exists = login_table.objects.filter(username=usr).exists()
        if exists:
            raise ValidationError(
                "Username is already taken"
            )
        
        return super().clean()

class Login(forms.Form):
    """Form for logging in"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self) -> dict[str, Any]:
        """Check form is valid"""

        cd = self.cleaned_data
        usr = cd.get("username")
        pswrd= cd.get("password")

        # Check user exists

        exists = login_table.objects.filter(username=usr,
                                            password=pswrd).exists()
        if not exists:
            raise ValidationError(
                "Invalid credentials"
            )

        return super().clean()