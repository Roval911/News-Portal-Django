from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import RegisterForm
from django.contrib.auth.models import Group
class RegisterView(CreateView):
   model = User
   form_class = RegisterForm
   template_name = 'sign/signup.html'
   success_url = '/'

   def form_valid(self, form):
      user = form.save()
      group = Group.objects.get_or_create(name='my_group')[0]

      user.groups.add(group)  # добавляем нового пользователя в эту группу
      user.save()
      return super().form_valid(form)

class LoginView(FormView):
   model = User
   form_class = LoginForm
   template_name = 'sign/login.html'
   success_url = '/'

   def form_valid(self, form):
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(self.request, username=username, password=password)
      if user is not None:
         login(self.request, user)
      return super().form_valid(form)


class LogoutView(TemplateView):
   template_name = 'sign/logout.html'

   def get(self, request, *args, **kwargs):
      logout(request)
      return super().get(request, *args, **kwargs)