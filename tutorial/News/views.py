# from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category, Author, Comment


class PostList(ListView):
    model = Post
    template_name = 'News.html'
    context_object_name = 'news'


class NewsDetail(DetailView):
    model = Post
    template_name = 'New.html'
    context_object_name = 'new'
