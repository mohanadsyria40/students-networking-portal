from django.urls import path
from . import views

urlpatterns = [
    path("", views.forum, name='forum'),
    path("thread_detail/<int:pk>/", views.thread_detail, name="thread_detail"),
    path("create_post", views.create_post, name="create_post"),
]
