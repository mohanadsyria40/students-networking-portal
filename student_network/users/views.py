from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # Validate user data (length, format, etc.)
        # Use a library like django-registration or write your own validation logic
        if valid_data:
            # Create a new user object
            user = User.objects.create_user(username, email, password)
            # Additional steps depending on your needs:
            # - Activate user account (email verification)
            # - Set user groups or permissions
            # - Send welcome email
            user.is_active = True
            user.save()
            # Log the user in and redirect
            login(request, user)
            return redirect('/')
        else:
            # Display error messages and form with pre-filled data (optional)
            return render(request, 'signup.html', {'errors': errors, 'username': username, 'email': email})
    else:
        # Display the empty registration form
        return render(request, 'signup.html')