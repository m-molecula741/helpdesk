from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView
from .models import Ticket
from django.views.generic.detail import DetailView
from tickets.models import Ticket


class CreateTicketView(CreateView):
    """Создание тикета пользователем"""
    model = Ticket
    fields = ['title', 'description', 'status', 'priority']  # поля, которые будут отображаться в форме
    template_name = 'tickets/create_ticket.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('home')


class TicketsListView(View):
    """Получения списка тикетов"""
    def get_user_tickets(self, user):
        if user.groups.filter(name='tech_support').exists():  # Для пользователей в группе поддержки
            return Ticket.objects.filter(assigned_to=user)
        else:  # Для всех остальных пользователей
            return Ticket.objects.filter(created_by=user)

    def get(self, request):
        user_tickets = self.get_user_tickets(request.user)
        return render(request, 'tickets/tickets.html', {'tickets': user_tickets})


class TicketDetail(DetailView):
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
