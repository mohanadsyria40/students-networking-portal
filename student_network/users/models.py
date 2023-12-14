from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class Student(models.Models):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    studentId = models.CharField(max_length=20, primary_key=True)
    email = models.CharField(max_length=255, unique=True)
    
    
    def set_password(self, password):
        self.password = make_password(password)


    def check_password(self, password):
        return self.password == make_password(password)    
    

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    
class Thread(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=3, decimal_places=2)
    description = models.TextField()

class Post(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    
    
    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return self.password == make_password(password)  
    # Add other fields like username, password, etc.