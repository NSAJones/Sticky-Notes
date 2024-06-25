"""
This is a short file with only the model used for logging in and
tracking session ids
"""

from django.db import models


# Create your models here.
class Login(models.Model):
    """Form for credentials and storing session_ids"""

    username = models.CharField(primary_key=True, max_length=50)
    password = models.CharField(max_length=50)
    session_id = models.UUIDField(blank=True, null=True)
