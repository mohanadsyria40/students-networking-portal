from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import *
from .forms import PostCreationForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def forum(request):
    threads = Thread.objects.all()
    return render(request, "forum/index.html", {"threads": threads})


def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    posts = Post.objects.filter(thread=thread)
    return render(request, 'forum/thread_detail.html', {"thread": thread, "posts": posts})


@login_required(login_url='users/login')
def create_post(request):
      # Replace CombinedForm with the actual combined form you create

    if request.method == 'POST':
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
    
    
def delete_post(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    # Check if the user is the author of the post
    if post.student == request.user:
        thread_pk = post.thread.pk  # Assuming your Thread model has a field named pk or id
        post.delete()
        messages.success(request, 'Post deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this post.')

    return redirect(reverse('thread_detail', args=[str(thread_pk)]))