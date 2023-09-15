# Import necessary modules and classes
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User

#---I WROTE THIS CODE---

# Define a form for user registration
class UserForm(forms.ModelForm):
    # Define a password field with a password input widget
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
#---END OF CODE THAT I WROTE---        

#---I WROTE THIS CODE---
# Define a form for user profile information
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ['name']

    # Define a required name field
    name = forms.CharField(required=True)
#---END OF CODE THAT I WROTE---    

#---I WROTE THIS CODE---
# Define a form for user login
class UserLoginForm(forms.Form):
    # Define username and password fields with appropriate widgets
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#---END OF CODE THAT I WROTE---

#---I WROTE THIS CODE---
# Define a form for editing user profile information
class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ['name', 'email', 'profile_image', 'background_image', 'bio']

    # Define a required name field
    name = forms.CharField(required=True)

#---END OF CODE THAT I WROTE---
    


    
