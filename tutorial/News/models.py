from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reiting = models.IntegerField(default=0)

    def update_reiting(self):
        post_reit = self.post_set.all().aggregate(post_reit=Sum('reiting'))['post_reit'] or 0
        comment_reit = self.user.comment_set.all().aggregate(comment_reit=Sum('reiting'))['comment_reit'] or 0
        self.reiting = post_reit * 3 + comment_reit
        self.save()


class Category(models.Model):
    name_category = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscriber')

class CategorySubscriber(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Post(models.Model):
    article = "ART"
    news = "NEWS"
    TYPE_POST = [
        (article, "Статья"),
        (news, "Новость")
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_post = models.CharField(max_length=255, choices=TYPE_POST, default=news)
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    name_post = models.CharField(max_length=255, default='заголовок')
    text_post = models.TextField(default='текст статьи')
    reiting = models.IntegerField(default=0)

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания переходить на страницу новости
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'new-{self.pk}')

    def like(self):
        self.reiting += 1
        self.save()

    def dislike(self):
        self.reiting -= 1
        self.save()

    def preview(self):
        return f'{self.text_post[:124]} ...'

    def __str__(self):
        return f'{self.name_post.title()}: {self.text_post[:20]}'

    def get_absolute_url(self):
        return f'/news/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField(default='Оставьте коментарий')
    time_create = models.DateTimeField(auto_now_add=True)
    reiting = models.IntegerField(default=0)

    def like(self):
        self.reiting += 1
        self.save()

    def dislike(self):
        self.reiting -= 1
        self.save()



