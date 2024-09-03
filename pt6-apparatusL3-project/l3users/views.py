from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, View
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db import transaction, IntegrityError
from .forms import UserForm, UserProfileInfoForm, LoginForm
import logging
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from .models import UserProfileInfo


logger = logging.getLogger(__name__)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'l3users/index.html'


class RegisterView(CreateView):
    template_name = 'l3users/registration.html'
    form_class = UserForm
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['profile_form'] = UserProfileInfoForm(self.request.POST, self.request.FILES)
        else:
            context['profile_form'] = UserProfileInfoForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        profile_form = context['profile_form']

        if form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    profile = profile_form.save(commit=False)
                    profile.user = user

                    default_group = Group.objects.get(name='Participant')
                    user.groups.add(default_group)
                    profile.group = default_group

                    profile.save()

                messages.success(self.request, f"Registration successful for user {user.username}. Please log in.")
                return redirect('login')

            except IntegrityError as e:
                logger.error(f"IntegrityError: {e} - form data: {self.request.POST}")
                messages.error(self.request, "A user with that username, email, or employee ID already exists.")
            except Exception as e:
                logger.error(f"Unexpected error during registration: {e}")
                messages.error(self.request, "An unexpected error occurred. Please try again later.")
        else:
            messages.error(self.request, "There were errors in the form. Please correct them and try again.")

        return self.render_to_response(context)


class LoginView(View):
    template_name = 'l3users/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/dashboard')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(
                    request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/dashboard')
                else:
                    messages.error(request, "Invalid email or password.")
            except Exception as e:
                logger.error(f"Error during login attempt: {e}")
                messages.error(
                    request, "An unexpected error occurred. Please try again later.")
        else:
            messages.error(
                request, "Email address or Password is incorrect.")
        return render(request, self.template_name, {'form': form})


class RedirectToLoginOrHome(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return redirect('login')


class UserProfileView(TemplateView):
    template_name = 'l3users/user_profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfileInfo.objects.get(user=self.request.user)
        context['user_profile'] = user_profile
        return context
    
def custom_logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('/login')  # Change 'home' to the name of your home URL pattern