from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


# models.py
from django.db import models


class Thread(models.Model):
    CATEGORY_CHOICES = [
        ('Academic questions', 'Academic questions'),
        ('Courses', 'Courses'),
        ('Registration', 'Registration'),
        ('Events', 'Events')
    ]
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=255)
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} Post by {self.student.get_username()} in {self.thread.title}"
    
    def comment_count(self):
        return Comment.objects.filter(post=self).count()
    

class Comment(models.Model):
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.username} - {self.content[:20]}'

    def get_absolute_url(self):
        return reverse('forum-detail', kwargs={'pk': self.post.thread.forum.pk})
