
from imp import get_suffixes
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import StudentRegistrationForm, StudentLoginForm, UserUpdateForm
from django.views import generic
from django.urls import reverse_lazy
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



# class profile_view(LoginRequiredMixin, generic.UpdateView):
#     model = get_user_model()
#     form_class = UserUpdateForm
#     template_name = 'users/profile.html'
#     success_url = reverse_lazy('forum')

#     def get_object(self, queryset=None):
#         return self.request.user

#     def form_valid(self, form):
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         return self.render_to_response(self.get_context_data(form=form))


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