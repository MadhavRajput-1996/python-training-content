from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Root URL will redirect based on the user's status
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.display_user_profile, name='profile'),
    path('profile/update/', views.profile_update, name='update_profile'),
]