from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import CreateView


class Login(LoginView):
    """Авторизация"""
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')
    

class Logout(LogoutView):
    """Выход"""
    template_name = 'accounts/login.html'


class RegisterView(CreateView):
    """Регистрация пользователя"""
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
