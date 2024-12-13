# from django.contrib.auth.backends import ModelBackend
# from .models import Student

# class StudentAuthenticationBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):

#         # Try to find user by username or student ID
#         try:
#             user = Student.objects.get(studentId=username)
#         except Student.DoesNotExist:
#             try:
#                 user = Student.objects.get(user__username=username)
#             except Student.DoesNotExist:
#                 return None

#         # Check the password
#         if user.user.check_password(password):
#             return user

#         return None