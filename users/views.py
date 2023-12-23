from email import message
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import Student
from .register_forms import StudentRegistrationForm, StudentLoginForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User


@csrf_protect
def register(request):
  if request.method == "POST":
    form = StudentRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.save()
      student = Student.objects.create(user=user,
                                       studentId=form.cleaned_data['studentId'],
                                       email=form.cleaned_data['email'],
                                       first_name=form.cleaned_data['first_name'],
                                       last_name=form.cleaned_data['last_name'],
                                       )
      messages.success(request, "Account is successfully created!")
      return redirect('login')
  else:
    form = StudentRegistrationForm()  
    
  return render(request, 'users/register.html', {'form': form})

def login_view(request):
  form = StudentLoginForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      studentId = form.cleaned_data.get('studentId')('studentId')
      password = form.cleaned_data.get('password')
      print(studentId + password)
      user = authenticate(request, studentId=studentId, password=password)
    
      if user is not None:
        login(request, user)
        return redirect('forum')
    
      else:
        messages.info(request, "Invalid username/student id or password.")
  context = {'form': form}
  return render(request, 'users/login.html', context)

