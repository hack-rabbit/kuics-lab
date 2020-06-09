from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django import forms

from registration.forms import RegistrationForm


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    error_messages = {
        'invalid_login': 'Incorrect username or password.'
    }

    username = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


class RegisterForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

    error_messages = {
        'password_mismatch': 'The specified passwords do not match.',
        'username_too_short': 'This username is too short. It must contain at least 4 characters.',
    }

    username = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(max_length=75, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password Confirm'}))

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 4:
            raise forms.ValidationError(
                self.error_messages['username_too_short'],
                code='username__too__short',
            )
        return username
