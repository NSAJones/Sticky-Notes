"""
This file has urls for the dashboard, boards and invites pulled from
this application's view
"""

from django.urls import path
from .views import board, invite, dashboard

urlpatterns = [
    path("boards/<int:board_id>", board, name="board"),
    path("boards/invites/<int:board_id>", invite, name="invite"),
    path("dashboard", dashboard, name="dashboard"),
]
