from django.contrib.auth.backends import ModelBackend
from .models import Student

class StudentAuthenticationBackend(ModelBackend):
    def authenticate(self, request, studentId=None, password=None, username=None):
        if studentId:
            try:
                user = Student.objects.get(studentId=studentId)
                django_user = user.user
                if django_user.check_password(password):  # Password check here
                    return user  # Return the user if password matches
            except Student.DoesNotExist:
                pass
        elif username:
            try:
                user = Student.objects.get(username=username)
                django_user = user.user
                if django_user.check_password(password):  # Password check here
                    return user  # Return the user if password matches
            except Student.DoesNotExist:
                pass
        return None