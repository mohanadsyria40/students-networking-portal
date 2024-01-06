from django.db import models
from django.contrib.auth.models import User, AbstractUser
from PIL import Image




# models.py

class CustomUser(AbstractUser):
    studentId = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    grade = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='profile_avatars', default='avatar.jpg', blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)
