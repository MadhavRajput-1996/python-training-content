from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfileInfo
from django.core.exceptions import ValidationError


class UserForm(UserCreationForm):
    required_css_class = 'required'

    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}), label_suffix='')
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}), label_suffix='')
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control'}), label_suffix='')
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}), label_suffix='')
    password2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}), label_suffix='')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2


class UserProfileInfoForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = UserProfileInfo
        fields = ('phone', 'employee_id', 'profile_pic')
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')
        if not employee_id:
            raise ValidationError("Employee ID cannot be empty.")
        if UserProfileInfo.objects.filter(employee_id=employee_id).exists():
            raise ValidationError("A user with this employee ID already exists.")
        return employee_id    



class LoginForm(AuthenticationForm):
    required_css_class = 'required'
    username = forms.CharField(label='Username or Email', max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off'}), label_suffix='')

    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}), label_suffix=''
    )
