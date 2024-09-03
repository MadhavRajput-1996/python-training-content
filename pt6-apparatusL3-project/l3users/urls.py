from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import IndexView, RegisterView, LoginView, RedirectToLoginOrHome, UserProfileView, custom_logout_view

urlpatterns = [
    path('', RedirectToLoginOrHome.as_view(), name='redirect-to-login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', IndexView.as_view(), name='dashboard'),
    path('logout/',custom_logout_view, name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),

]
