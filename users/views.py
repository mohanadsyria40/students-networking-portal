
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from users.forms import StudentRegistrationForm, StudentLoginForm, UserUpdateForm, SetPasswordForm, PasswordResetForm
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q

from .decorators import user_not_authenticated
from .tokens import account_activation_token


def activate(request, uidb64, token):
  user = get_user_model()
  try:
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = user.objects.get(pk=uid)
  except:
    user = None

  if user is not None and account_activation_token.check_token(user, token):
    user.is_active = True
    user.save()

    messages.success(request, "Thank you for your email verification. You can now join the community by logging in :)")
    return redirect('login')

  else:
    messages.error(request, "Ops!! Activation link is invalid")

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

@user_not_authenticated
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
      for key, error in list(form.errors.items()):
        if key == 'captcha' and error[0] == 'This field is required.':
          messages.error(request, "You must pass the reCAPTCHA test")
          continue
        messages.error(request, error)
        
  else:
    form = StudentRegistrationForm()

  return render(request, 'registration/register.html', {'form': form})


@user_not_authenticated
def login_view(request):
  if request.method == "POST":
    form = StudentLoginForm(request=request, data=request.POST)
    if form.is_valid():
      username = request.POST['username']
      password = request.POST['password']
      user = authenticate(request, username=username, password=password)

      if user is not None:
        login(request, user)
        messages.success(request, f'Hello <strong>{user.username}</strong>, you were Logged in successfully!')
        return redirect('forum')


    else:
      for key, error in list(form.errors.items()):
        if key == 'captcha' and error[0] == 'This field is required.':
          messages.error(request, "You must pass the reCAPTCHA test")
          continue
        messages.error(request, error)

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

@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
       form = SetPasswordForm(user, request.POST)
       if form.is_valid():
         form.save()
         messages.success(request, "Your password has been successfully changed!")
         return redirect('login')

       else:
          for error in list(form.errors.values()):
            messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'users/password_reset_confirm.html', {'form': form})


@user_not_authenticated
def password_reset_request(request):
  if request.method == 'POST':
    form = PasswordResetForm(request.POST)
    if form.is_valid():
      user_email = form.cleaned_data['email']
      associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
      if associated_user:
        subject = "Password Reset request"
        message = render_to_string("template_reset_password.html", {
        'user': associated_user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
        'token': account_activation_token.make_token(associated_user),
        "protocol": 'https' if request.is_secure() else 'http'})
        email = EmailMessage(subject, message, to=[associated_user.email])
        if email.send():
            messages.success(request,
                  """
                  <h2>Password reset sent</h2><hr>
                  <p>
                      We've emailed you instructions for setting your password, if an account exists with the email you entered.
                      You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address
                      you registered with, and check your spam folder.
                  </p>
                  """
                  )
        else:
            messages.error(request, f'Problem sending a reset password email to <strong>{associated_user.email}</strong>, check if you typed it correctly.')

      return redirect('forum')

    for key, error in list(form.errors.items()):
          if key == 'captcha' and error[0] == 'This field is required.':
              messages.error(request, "You must pass the reCAPTCHA test")
              continue

  form = PasswordResetForm()
  return render(
    request=request,
    template_name="users/password_reset.html",
    context={'form': form}
    )


def passwordResetConfirm(request, uidb64, token):
  User = get_user_model()
  try:
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
  except:
    user = None

  if user is not None and account_activation_token.check_token(user, token):
    if request.method == 'POST':
      form = SetPasswordForm(user, request.POST)
      if form.is_valid():
        form.save()
        messages.success(request, "Your password has been reset :) You can go ahead and <strong>log in</strong> now")
        return redirect('forum')

      else:
         for error in list(form.errors.values()):
            messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'users/password_reset_confirm.html', {'form': form})

  else:
    messages.error(request, "Ops!! Link is expired")


  messages.error(request, 'Something went wrong, redirecting to the forum page')
  return redirect('forum')


