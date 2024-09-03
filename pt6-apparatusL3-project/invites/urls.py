from django.urls import path
from .views import *

app_name = 'invites'

urlpatterns = [
    path('<int:pk>/edit-invite', UpdateInvite.as_view(), name='update_invite'),
]