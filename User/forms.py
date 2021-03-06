from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError

# User creation form for signing up as the new user 
class createuserform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def clean_email(self):
        email=self.cleaned_data['email']
        if not email.endswith('@gmail.com'):
            raise ValidationError('Domain of email is not valid')
        return email


class UserUpdateform(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email']

# form used for the updating the profile of the respective User
class UpdateProfileform(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['addressline1','addressline2','mobilenumber','pincode','state']
