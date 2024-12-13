
from django import forms
from django.shortcuts import render
from pkg_resources import require
from .models import *


        
class PostCreationForm(forms.ModelForm):
    thread_title = forms.CharField(label="Topic Title", max_length=255, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all())  # Add category field

    class Meta:
        model = Post
        fields = ['content', 'title' ]

        
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']