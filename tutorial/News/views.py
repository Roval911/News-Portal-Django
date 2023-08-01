# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from .models import Post, Category, Author, Comment
from .filters import PostFilter
from .forms import PostForms
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.conf import settings
from django.core.cache import cache


DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL
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

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта
        obj = cache.get(f'new-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует также. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'new-{self.kwargs["pk"]}', obj)

        return obj



class NewsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class NewsAdd(PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_Post')
    template_name = 'add.html'
    form_class = PostForms
    success_url = '/news/'


class NewsEdit(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    permission_required = ('News.change_Post')
    template_name = 'edit.html'
    form_class = PostForms
    success_url = '/news/{id}'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDelete(DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    context_object_name ='new'
    success_url = '/News/'



class CategoryNewsDetail(DetailView):
    model = Category
    template_name = 'cat.html'
    context_object_name = 'cat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=self.kwargs['pk'])
        context['subscribers'] = category.subscribers.all()
        return context

def subscribe(request, pk):
    category = Category.objects.get(pk=pk)
    user = request.user
    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        email = user.email
        html = render_to_string(
            'subscribed.html',
            {
                'category': category,
                'user': user,
            },
        )
        msg = EmailMultiAlternatives(
            subject=f'Подписка на {category.name_category} на сайте News Paper',
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=[email, ],
        )
        msg.attach_alternative(html, 'text/html')
        msg.send()
    return redirect(request.META.get('HTTP_REFERER'))


def unsubscribe(request, pk):
    user = request.user
    c = Category.objects.get(id=pk)

    if c.subscribers.filter(id=user.id).exists():
        c.subscribers.remove(user)
    return redirect(request.META.get('HTTP_REFERER'))