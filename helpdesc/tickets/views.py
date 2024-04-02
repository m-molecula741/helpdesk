from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView
from .models import Ticket
from django.views.generic.detail import DetailView
from tickets.models import Ticket, Status, Priority
from tickets.forms import CommentForm
from django.urls import reverse
from django.shortcuts import redirect



class CreateTicketView(CreateView):
    """Создание тикета пользователем"""
    model = Ticket
    fields = ['title', 'description']  # поля, которые будут отображаться в форме
    template_name = 'tickets/create_ticket.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
            form.instance.status = Status.OPEN
            form.instance.priority = Priority.MEDIUM
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('tickets')


class TicketsListView(View):
    """Получения списка тикетов"""
    def get_user_tickets(self, user):
        if user.groups.filter(name='tech_support').exists():  # Для пользователей в группе поддержки
            return Ticket.objects.filter(assigned_to=user)
        else:  # Для всех остальных пользователей
            return Ticket.objects.filter(created_by=user)

    def get(self, request):
        user_tickets = self.get_user_tickets(request.user)
        return render(
            request, 'tickets/tickets.html', 
            {'tickets': user_tickets, 'is_support': request.user.groups.filter(name='tech_support').exists()}
            )


class TicketDetail(DetailView):
    """Получение тикета"""
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class CreateComment(View):
    """Добавление коммента"""
    def post(self, request, pk):
        ticket = Ticket.objects.get(id=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
        
        return redirect(reverse('tickets'))


class CloseTicket(View):
    """Закрытие тикета"""
    def post(self, request, pk):
        is_updated = Ticket.objects.filter(id=pk).update(status=Status.CLOSED)
        return redirect(reverse('tickets'))
