from django import forms
from django.contrib.auth import authenticate, get_user_model, password_validation

# UserModel = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=32,
        required=True,
    )
    password = forms.CharField(
        max_length=32,
        widget=forms.PasswordInput,
        required=True,
    )
