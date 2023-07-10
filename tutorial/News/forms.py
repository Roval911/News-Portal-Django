from django.forms import ModelForm
from .models import Post

class PostForms(ModelForm):
    class Meta:
        model = Post
        fields = ['name_post', 'text_post', 'type_post', 'author', 'category']