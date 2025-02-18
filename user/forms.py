from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class LoginForm(AuthenticationForm):
    email = forms.EmailField(max_length=254, required=True)

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(),
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'password']
