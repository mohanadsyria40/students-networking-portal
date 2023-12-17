from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from register_forms import MyRegistrationForm, MyLoginForm


def register(request):
  if request.method == 'POST':
    # Use Django's UserCreationForm to process user input
    form = MyRegistrationForm(request.POST)
    if form.is_valid():
      # Create new user and log them in
      user = form.save()
      login(request, user)
      return redirect('home')
  else:
    # Render the registration form
    form = MyRegistrationForm()
  return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        student_id = request.POST['student_id']
        password = request.POST['password']
        user = authenticate(request, student_id=student_id, password=password)
        if user:
            login(request, user)
            return redirect('home')
    else:
        # Render the login form
        form = MyLoginForm()
    return render(request, 'login/login.html', {'form': form})