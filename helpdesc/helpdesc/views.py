from django.shortcuts import render
from django.views.generic.base import View


class HomeView(View):
     """Отображение домашней страницы"""
     def get(self,request):
        return render(request, 'home.html')
