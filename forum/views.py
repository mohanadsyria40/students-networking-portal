from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import *
from .forms import ThreadForm

def forum(request):
    return render(request, "forum/index.html", {})

def thread_list(request):
    threads = Thread.objects.all()
    return render(request, 'forum/thread_list.html', {"threads": threads})

def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    posts = Post.objects.filter(thread=thread)
    return render(request, 'forum/thread_detail', {"thread": thread, "posts": posts})


def new_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.student = request.user
            thread.save()
            return redirect('thread_detail', pk = thread.pk)
    else:
        form = ThreadForm()
    return render(request, "forum/new_thread.html", {"form": form})
