from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Post

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'gender', 'dob', 'email', 'mobile', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'placeholder': 'Content'}),
        }