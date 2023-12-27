from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission


    
class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')    
    
class Student(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="student")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    studentId = models.CharField(max_length=20, primary_key=True, unique=True)
    email = models.CharField(max_length=255, unique=True)
    #threads = models.ManyToManyField(Thread)
    #posts = models.ManyToManyField(Post)
   
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Profile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    grade = models.DecimalField(max_digits=3, decimal_places=2)
    description = models.TextField()
    
