from django.urls import path
from . import views

urlpatterns = [
    path("", views.forum, name='forum'),
    path("thread_detail/<int:pk>/", views.thread_detail, name="thread_detail"),
    path("create_post", views.create_post, name="create_post"),
    path("delete_post/<int:post_pk>/", views.delete_post, name="delete_post"),
    path("post/<int:post_id>/", views.post_detail, name='post_detail'),
    path("post/<int:post_id>/comment/", views.add_comment_to_post, name="add_comment_to_post"),
    path("comment/<int:comment_id>/delete/", views.delete_comment, name='delete_comment'),
    path("category/<str:cats>/", views.category_view, name="category"),
]
