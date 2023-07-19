# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from .models import Post, Category, Author, Comment
from .filters import PostFilter
from .forms import PostForms


class PostList(ListView):
    model = Post
    template_name = 'News.html'
    context_object_name = 'news'
    ordering = ['-time_create']
    paginate_by = 10



class NewsDetail(DetailView):
    model = Post
    template_name = 'New.html'
    context_object_name = 'new'


class NewsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class NewsAdd(CreateView, PermissionRequiredMixin):
    permission_required = ('news.add_post')
    template_name = 'add.html'
    form_class = PostForms


class NewsEdit(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    permission_required = ('news.change_post')
    template_name = 'edit.html'
    form_class = PostForms

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDelete(DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    context_object_name ='new'
    success_url = '/News/'
