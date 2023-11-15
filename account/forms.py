from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import User

class SignUpForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password (again)',
                                widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email']
        labels = {'email' : 'Email'}