from .models import Post
from django.contrib.auth import get_user_model



def forum_statistics(request):
    total_posts = Post.objects.count()
    total_members = get_user_model().objects.count()
    
    return {
        'total_posts': total_posts,
        'total_members': total_members,
    }