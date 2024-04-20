from django.shortcuts import render
from django.views.generic.base import View
from tickets.models import New


class HomeView(View):
     """Отображение домашней страницы"""
     def get(self,request):
        news = New.objects.filter().order_by('-id')
        return render(request, 'home.html', context={"news": news})
