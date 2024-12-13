from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


# models.py
from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=255)
    

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('forum')


class Thread(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)    
    title = models.CharField(max_length=255)
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

    def delete_if_no_posts(self):
        if not self.post_set.exists():
            self.delete()
    

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    comments_allowed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} Post by {self.student.get_username()} in {self.thread.title}"
    
    def comment_count(self):
        return Comment.objects.filter(post=self).count()
    

class Comment(models.Model):
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='student')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f'{self.student.username} - {self.content[:20]}'

