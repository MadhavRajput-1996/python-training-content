from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .forms import UserRegisterForm, UserUpdateForm
from music.forms import MusicCategoryForm
from music.models import MusicCategory


def home(request):
    # Check if the user is logged in
    if request.user.is_authenticated:
        return redirect('dashboard')  # If logged in, redirect to dashboard
    else:
        return redirect('register')  # If not logged in, redirect to register page

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()  # Save the user but don't log them in
                messages.success(request, 'Your account has been created! Please log in.')
                return redirect('login')  # Redirect to login after successful registration
            except Exception as e:
                messages.error(request, f'An unexpected error occurred: {e}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully!')
            return redirect('dashboard')  # Redirect to dashboard upon successful login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')

@login_required
def display_user_profile(request):
    """
    Display the profile information of the logged-in user.
    """
    user = request.user  # Get the currently logged-in user
    return render(request, 'users/profile.html', {'user': user})

@login_required
def profile_update(request):
    """
    Allow the user to update their profile.
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if u_form.is_valid():
            try:
                u_form.save()
                messages.success(request, 'Your profile has been updated successfully!')
                return redirect('dashboard')  # Redirect to dashboard
            except ValidationError as e:
                messages.error(request, f'Error: {e.message}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'dashboard.html', {'u_form': u_form})

@login_required
def dashboard(request):
    music_category_form = MusicCategoryForm()
    user_update_form = UserUpdateForm(instance=request.user)
    categories = MusicCategory.objects.filter(user=request.user)

    context = {
        'music_category_form': music_category_form,
        'user_update_form': user_update_form,
        'categories': categories,
    }

    return render(request, 'users/dashboard.html', context)  

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')
