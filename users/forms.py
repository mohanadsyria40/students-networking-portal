from pickle import FALSE
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django import forms
from django.contrib.auth import get_user_model
from pkg_resources import require
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox



CustomUser = get_user_model()

class StudentRegistrationForm(UserCreationForm):
  captcha = ReCaptchaField()
  
  class Meta:
    model = CustomUser
    fields = ['username', 'studentId', 'email', 'first_name', 'last_name',  'password1', 'password2']

  
class StudentLoginForm(AuthenticationForm):
  captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
  
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
    captcha = ReCaptchaField()
     
    class Meta:
        model = CustomUser
        fields = ['password1', 'password2']
     
     

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
