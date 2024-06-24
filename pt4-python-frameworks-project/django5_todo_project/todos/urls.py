from django.urls import path
from . import views

app_name = 'todos'

urlpatterns = [
    path('', views.register, name='register'),  # Dedicated path for registration
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('todo/', views.todo_list, name='todo_list'),
    path('todo/create/', views.create_todo, name='create_todo'),
    path('todo/<int:pk>/', views.todo_detail, name='todo_detail'),
    path('todo/update/<int:pk>/', views.update_todo, name='update_todo'),
    path('todo/delete/<int:pk>/', views.delete_todo, name='delete_todo'),
]