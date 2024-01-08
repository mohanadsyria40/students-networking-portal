
from django import forms
from django.shortcuts import render
from .models import *



class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['category', 'title']
        
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['category', 'title']
        
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['category', 'title']