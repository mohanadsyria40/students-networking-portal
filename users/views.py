
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from .models import Student
from .register_forms import StudentRegistrationForm, StudentLoginForm



def register(request):
  if request.method == "POST":
    form = StudentRegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      user = authenticate(username=username, password=password)
      login(request, user)
      messages.success(request, ("Account is successfully created!"))
      return redirect('forum')
  else:
    form = StudentRegistrationForm()  
    
  return render(request, 'registration/register.html', {'form': form})

def login_view(request):
  if request.method == "POST":
      username = request.POST['username']
      password = request.POST['password']   
      user = authenticate(request, username=username, password=password)

      if user is not None:
        login(request, user)
        messages.success(request, "Logged in successfully!")
        return redirect('forum')

    
      else:
        messages.info(request, "Invalid username or password.")
        return redirect('login')
    
  else:
    form = StudentLoginForm()        
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
  logout(request) 
  messages.success(request, "You were logged out!")
  return redirect('forum')