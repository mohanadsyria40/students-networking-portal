from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth import get_user_model
from PIL import Image




class CustomUser(AbstractUser):
    studentId = models.CharField(max_length=20, unique=True)
    email = models.EmailField()


    def __str__(self):
        return self.username



class Profile(models.Model):
    student = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    avatar = models.ImageField(
        default='avatar.jpg', # default avatar
        upload_to='profile_avatars' # dir to store the image
    )


    def __str__(self):
        return f'{self.student.get_username()} Profile'


    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

        # resize the image
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            # create a thumbnail
            img.thumbnail(output_size)
            # overwrite the larger image
            img.save(self.avatar.path)

    grade = models.DecimalField(max_digits=3, decimal_places=2)
    description = models.TextField()
