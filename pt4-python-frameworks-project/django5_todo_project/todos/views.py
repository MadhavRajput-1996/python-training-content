import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, TodoForm
from .models import Todo
from django.db import IntegrityError  

# Get an instance of a logger
logger = logging.getLogger(__name__)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                email = form.cleaned_data.get('email')
                messages.success(request, f'Account created for {email}. Please log in.')
                return redirect('todos:login')
            except IntegrityError as e:
                messages.error(request, 'There was an error saving your account. Please try again.')
                logger.error(f"Error in user registration: {e}")
        else:
            messages.error(request, 'Invalid form data. Please check the form and try again.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    try:
        if request.method == 'POST':
            form = CustomAuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('todos:todo_list')
                else:
                    messages.error(request, 'Invalid email or password. Please try again.')
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
        else:
            form = CustomAuthenticationForm()
    except Exception as e:
        logger.error(f"Error during login: {e}")
        messages.error(request, 'An error occurred during login. Please try again later.')
    return render(request, 'registration/login.html', {'form': form})

@login_required
def user_logout(request):
    try:
        logout(request)
    except Exception as e:
        logger.error(f"Error in user logout: {e}")
        messages.error(request, 'Error logging out. Please try again later.')
    return redirect('todos:login')

@login_required
def todo_list(request):
    try:
        todos = Todo.objects.filter(user=request.user)
    except Exception as e:
        logger.error(f"Error fetching todos: {e}")
        messages.error(request, 'Error fetching todo list. Please try again later.')
        todos = []
    return render(request, 'todos/todo_list.html', {'todos': todos})
@login_required
def create_todo(request):
    try:
        if request.method == 'POST':
            form = TodoForm(request.POST)
            if form.is_valid():
                todo = form.save(commit=False)
                todo.user = request.user
                todo.save()
                return redirect('todos:todo_list')
        else:
            form = TodoForm()
    except Exception as e:
        logger.error(f"Error creating todo: {e}")
        messages.error(request, 'Error creating todo. Please try again later.')
    return render(request, 'todos/todo_form.html', {'form': form})

@login_required
def todo_detail(request, pk):
    try:
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
    except Exception as e:
        logger.error(f"Error retrieving todo detail: {e}")
        messages.error(request, 'Error retrieving todo detail. Please try again later.')
        return redirect('todos:todo_list')
    return render(request, 'todos/todo_detail.html', {'todo': todo})

@login_required
def update_todo(request, pk):
    try:
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
        if request.method == 'POST':
            form = TodoForm(request.POST, instance=todo)
            if form.is_valid():
                form.save()
                return redirect('todos:todo_list')
        else:
            form = TodoForm(instance=todo)
    except Exception as e:
        logger.error(f"Error updating todo: {e}")
        messages.error(request, 'Error updating todo. Please try again later.')
    return render(request, 'todos/todo_form.html', {'form': form})

@login_required
def delete_todo(request, pk):
    try:
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
        if request.method == 'POST':
            todo.delete()
            return redirect('todos:todo_list')
    except Exception as e:
        logger.error(f"Error deleting todo: {e}")
        messages.error(request, 'Error deleting todo. Please try again later.')
    return render(request, 'todos/todo_confirm_delete.html', {'todo': todo})
