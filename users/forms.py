from pickle import FALSE
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django import forms
from django.contrib.auth import get_user_model
from pkg_resources import require


CustomUser = get_user_model()

class StudentRegistrationForm(UserCreationForm):
  username = forms.CharField(max_length=30, label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
  studentId = forms.CharField(max_length=20, label='Student ID', widget=forms.TextInput(attrs={'placeholder': 'Student ID'}))
  first_name = forms.CharField(max_length=255, label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
  last_name = forms.CharField(max_length=255, label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
  email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
  password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
  password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
  
  
  class Meta:
    model = CustomUser
    fields = ['username', 'studentId', 'email', 'first_name', 'last_name',  'password1', 'password2']

  
class StudentLoginForm(AuthenticationForm):
  username = forms.CharField(max_length=30, label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
  password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
  
  class Meta:
    model = CustomUser  
    fields = ['username', 'password']
    
    

class UserUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    
    class Meta:
        model = CustomUser
        fields = ['avatar', 'username', 'studentId', 'email', 'first_name', 'last_name', 'grade', 'description']
        
    def clean_studentId(self):
      studentId = self.cleaned_data.get('studentId')

      # Your validation logic goes here
      if not studentId:
          raise forms.ValidationError("Student ID is required.")

      return studentId
    


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = CustomUser
        fields = ['password1', 'password2']
     
     

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
