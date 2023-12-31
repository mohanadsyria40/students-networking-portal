
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import StudentRegistrationForm, StudentLoginForm, UserUpdateForm, ProfileUpdateForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin



def register(request):
  if request.method == "POST":
    form = StudentRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save()
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      studentId = request.POST['studentId']
      user.studentId = studentId
      user.save()
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


class MyProfile(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        
        return render(request, 'users/profile.html', context)
    
    def post(self,request):
        user_form = UserUpdateForm(
            request.POST, 
            instance=request.user
        )
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            messages.success(request,'Your profile has been updated successfully')
            
            return redirect('profile')
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form
            }
            messages.error(request,'Error updating you profile')
            
            return render(request, 'users/profile.html', context)