from django.contrib.auth.forms import UserCreationForm, LoginForm
from django import forms

class MyRegistrationForm(UserCreationForm):
  student_id = forms.CharField(max_length=20, label='Student ID')
  firstname = forms.CharField(max_length=255, label='First Name')
  lastname = forms.CharField(max_length=255, label='Last Name')

  class Meta:
    fields = ['student_id', 'firstname', 'lastname', 'email', 'password1', 'password2']
    
    
class MyLoginForm(LoginForm):
  student_id = forms.CharField(max_length=20, label='Student ID')

  class Meta:
    fields = ['student_id', 'password']