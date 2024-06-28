
import os
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Post, CustomUser
from .forms import CustomUserCreationForm, PostForm

class UserRegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class UserLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        # Set session data upon successful login
        self.request.session['first_name'] = form.get_user().first_name
        return super().form_valid(form)

class UserProfileView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'profile.html'
    context_object_name = 'user_posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['first_name'] = self.request.session.get('first_name', 'Anonymous')
        return context

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        # Clear session data upon logout
        if 'first_name' in request.session:
            del request.session['first_name']
        return super().dispatch(request, *args, **kwargs)

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetching first_name of authors for each post
        for post in context['posts']:
            post.author_first_name = post.author.first_name
            
            # Check if the logged-in user is the owner of the post
            if self.request.user.is_authenticated and self.request.user == post.author:
                post.can_edit_delete = True
            else:
                post.can_edit_delete = False
        
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_object = self.object
        
        # Accessing the first_name of the author
        author_first_name = post_object.author.first_name
        
        # Add first_name to the context to use in the template
        context['author_first_name'] = author_first_name
        
        # Check if the logged-in user is the owner of the post
        if self.request.user.is_authenticated and self.request.user == post_object.author:
            context['can_edit_delete'] = True
        else:
            context['can_edit_delete'] = False
        
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        # Remove old image if updating with a new one
        post = form.save(commit=False)
        old_post = Post.objects.get(pk=post.pk)  # Fetch old post instance
        if old_post.image and old_post.image != post.image:
            if os.path.isfile(old_post.image.path):
                os.remove(old_post.image.path)
        post.save()
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
