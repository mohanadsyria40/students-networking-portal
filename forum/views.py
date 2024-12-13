from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import *
from .forms import PostCreationForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def forum(request):
    total_posts = Post.objects.count()
    total_members = get_user_model().objects.count()
    threads = Thread.objects.all()
    return render(
        request, "forum/index.html",
        {"threads": threads,
         "total_posts": total_posts,
         "total_members": total_members,
         })


def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    posts = Post.objects.filter(thread=thread)
    
    posts_with_comments = []
    for post in posts:
        comments = Comment.objects.filter(post=post)
        posts_with_comments.append((post, comments))
        
    return render(request, 'forum/thread_detail.html', {"thread": thread, "posts": posts})


@login_required(login_url='users/login')
def create_post(request):
    if request.method == 'POST':
        # create an instance from the form with the passed data
        form = PostCreationForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.student = request.user

            thread_choice = request.POST.get('thread_choice') 
            if thread_choice == 'new':
                # Create a new thread
                new_thread = Thread.objects.create(
                    title=form.cleaned_data['thread_title'],
                    category=form.cleaned_data['category'],
                    student=request.user
                )
                post.thread = new_thread
            else:
                # Use an existing thread
                existing_thread = get_object_or_404(Thread, pk=thread_choice)
                post.thread = existing_thread
            
            post.save()
            messages.success(request, "Your question was successfully posted!")
            return redirect(reverse('thread_detail', args=[str(post.thread.pk)]))
        
        else:
            messages.error(request, "Failed to post the question! make sure information are valid")
        
    else:
        form = PostCreationForm()
        
        
    threads = Thread.objects.all()
    return render(
        request,
        "forum/create_post.html",
        {"form": form, "threads": threads},
    )
    
    
@login_required(login_url='users/login')
def delete_post(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    # Check if the user is the author of the post
    if post.student == request.user:
        thread_pk = post.thread.pk  # Assuming your Thread model has a field named pk or id

        # Check if the associated thread has no more posts
        if not Post.objects.filter(thread=post.thread).exclude(pk=post.pk).exists():
            # If no more posts, delete the thread
            post.thread.delete()
            redirect_url = reverse('forum')  # Redirect to the forum page
        else:
            # If there are still posts, redirect to the thread detail
            redirect_url = reverse('thread_detail', args=[str(thread_pk)])

        post.delete()
        messages.success(request, 'Post deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this post.')

    return redirect(redirect_url)



def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post)
    return render(request, 'forum/post_detail.html',{"post": post , "request_user": request.user, "comments": comments})

    
    
# define the view to be validated when comment is initiated
@login_required(login_url='users/login')
def add_comment_to_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if not post.comments_allowed:
        messages.error(request, 'Comments are not allowed for this post.')
        return redirect('post_detail', post_id=post.id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # check
            parent_comment_id = request.GET.get('parent_comment_id')
            parent_comment = None
            if parent_comment_id:
                parent_comment = get_object_or_404(Comment, pk=parent_comment_id)

            # save comment to the database after assigning its fields
            comment = form.save(commit=False)
            comment.post = post
            comment.student = request.user
            if parent_comment:
                comment.parent_comment = parent_comment
            comment.save()
            messages.success(request, "Your comment was added successfully!")
            return redirect('post_detail', post_id=post.id)
        
    else:
        form = CommentForm()
            
    return render(request, 'forum/add_comment_to_post.html', {"form": form})



def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    if comment.student == request.user:
        comment.delete()
        messages.success(request, "Comment was successfully deleted!")
    
    else:
        messages.error(request, "You don't have permission to delete this comment")
    
    return redirect('post_detail', post_id=comment.post.id)





def category_view(request, cats):
    category_posts = Post.objects.filter(thread__category__name=cats.replace('-', ' '))
    return render(request, 'forum/category_page.html', {"cats": cats.title(), "category_posts": category_posts})