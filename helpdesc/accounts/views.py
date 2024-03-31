from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm


class HomeView(View):
     def get(self,request):
        return render(request, 'accounts/home.html')


class Login(LoginView):
    """Авторизация"""
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')
    

class Logout(LogoutView):
    template_name = 'accounts/login.html'
