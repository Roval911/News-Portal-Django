from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя") # опционально, можно не указывать
    last_name = forms.CharField(label = "Фамилия") # опционально

    class Meta:
        model = User
        fields = ("username",
                  "first_name", # опционально
                  "last_name", # опционально
                  "email",
                  "password1",
                  "password2", )