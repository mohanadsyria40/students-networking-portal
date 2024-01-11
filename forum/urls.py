from django.urls import path
from . import views

urlpatterns = [
    path("", views.forum, name='forum'),
    path("thread_detail/<int:pk>/", views.thread_detail, name="thread_detail"),
    path("create_post", views.create_post, name="create_post"),
    path("delete_post/<int:post_pk>/", views.delete_post, name="delete_post"),
]
