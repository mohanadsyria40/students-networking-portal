from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import Student



class MyRegistrationForm(UserCreationForm):
  student_id = forms.CharField(max_length=20, label='Student ID')
  firstname = forms.CharField(max_length=255, label='First Name')
  lastname = forms.CharField(max_length=255, label='Last Name')

  class Meta:
    model = User
    fields = ['student_id', 'firstname', 'lastname', 'email', 'password1', 'password2']
   
   
  def save(self, commit=True, *args, **kwargs):
    user = super().save(commit=False)  # Create User model instance
    if commit:
      user.save()  # Save User model instance

      # Create and associate Student model instance
      student = Student(user=user, student_id=self.cleaned_data['student_id'],
                       firstname=self.cleaned_data['firstname'],
                       lastname=self.cleaned_data['lastname'])
      student.save()

    return user 
    

class MyLoginForm(AuthenticationForm):
  username = forms.CharField(max_length=254, label='Student ID')

  class Meta:
    fields = ['username', 'password']