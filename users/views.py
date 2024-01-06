
from imp import get_suffixes
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import StudentRegistrationForm, StudentLoginForm, UserUpdateForm
from django.views import generic
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

# from .decorators import user_not_authenticated
from .tokens import account_activation_token


def activate(request, uidb64, token):
  return redirect('forum')


def activateEmail(request, user, to_email):
  mail_subject = "Activate your user account."
  message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
  email = EmailMessage(mail_subject, message, to=[to_email])
  if email.send():
      messages.success(request, f'Dear <strong>{user}</strong>, please go to you email <strong>{to_email}</strong> inbox and click on \
              received activation link to confirm and complete the registration. <strong>Note:</strong> Check your spam folder.')
  else:
      messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def register(request):
  if request.method == "POST":
    form = StudentRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.is_active=False
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      studentId = request.POST['studentId']
      user.studentId = studentId
      user.save()
      activateEmail(request, user, form.cleaned_data.get('email'))
      # user = authenticate(username=username, password=password)
      # login(request, user)
      # messages.success(request, ("Account is successfully created!"))
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



def profile_view(request, username):
  if request.method == "POST":
    user = request.user
    form = UserUpdateForm(request.POST, request.FILES, instance=user)
    if form.is_valid():
      user_form = form.save()
      messages.success(request, f'{user_form.username}, your profile has been updated')
      return redirect('profile', user_form.username)
    
    for error in list(form.errors.values()):
      messages.error(request, error)
      
      
  user = get_user_model().objects.filter(username=username).first()
  if user:
    form = UserUpdateForm(instance=user)
    return render(
      request=request,
      template_name='users/profile.html',
      context = {"form": form}
    )
    
  return redirect('forum')