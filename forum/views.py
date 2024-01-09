from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import *
from .forms import ThreadForm, PostForm, CommentForm
from django.contrib.auth.decorators import login_required

def forum(request):
    threads = Thread.objects.all()
    return render(request, "forum/index.html", {"threads": threads})


def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    posts = Post.objects.filter(thread=thread)
    return render(request, 'forum/thread_detail.html', {"thread": thread, "posts": posts})

@login_required(login_url='users/login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.student = request.user

            # Check if a new thread is being created
            thread_choice = request.POST.get('thread_choice')
            if thread_choice == 'new':
                thread_form = ThreadForm(request.POST)
                if thread_form.is_valid():
                    new_thread = thread_form.save(commit=False)
                    new_thread.student = request.user
                    new_thread.save()
                    post.thread = new_thread
            else:
                # Existing thread is selected
                thread_form = None  # Initialize thread_form as None
                thread_id = request.POST.get('thread_choice')
                existing_thread = get_object_or_404(Thread, pk=thread_id)
                post.thread = existing_thread

            post.save()
            return redirect('forum')

    else:
        form = PostForm()
        thread_form = None  # Initialize thread_form as None

    threads = Thread.objects.all()
    return render(
        request,
        "forum/create_post.html",
        {"form": form, "thread_form": thread_form, "threads": threads},
    )