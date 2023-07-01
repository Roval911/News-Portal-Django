from django.contrib import admin
from .models import Category, Post, Author, Comment
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Comment)