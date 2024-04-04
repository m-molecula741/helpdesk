from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView
from .models import Ticket
from django.views.generic.detail import DetailView
from tickets.models import Ticket, Status, Priority, Theme, KnowledgeBase
from django.views.generic import ListView
from tickets.forms import CommentForm
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse


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


class TicketsListView(ListView):
    """Получения списка тикетов"""

    model = Ticket
    template_name = 'tickets/tickets.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_support'] = self.request.user.groups.filter(name='tech_support')
        return context
    
    def get_user_tickets(self, user):
        if user.groups.filter(name='tech_support').exists():  # Для пользователей в группе поддержки
            return Ticket.objects.filter(assigned_to=user).order_by('-created_at')
        else:  # Для всех остальных пользователей
            return Ticket.objects.filter(created_by=user).order_by('-created_at')

    def get_queryset(self):
        user_tickets = self.get_user_tickets(self.request.user)
        return user_tickets

class TicketDetail(DetailView):
    """Получение тикета"""
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_support'] = self.request.user.groups.filter(name='tech_support')
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
        ticket = Ticket.objects.get(id=pk)
        # Сохраняем данные в сессию
        request.session['ticket_title'] = ticket.title
        request.session['ticket_description'] = ticket.description
        return redirect(reverse('create_knowledge'))


class CreateKnowledge(CreateView):
    """Создание записи в базе знаний"""
    model = KnowledgeBase
    fields = ['title', 'solution', 'theme']
    template_name = 'tickets/create_knowledge.html'

    @method_decorator(user_passes_test(lambda user: user.groups.filter(name='tech_support').exists()))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateKnowledge, self).get_context_data(**kwargs)
        context['themes'] = Theme.objects.all()
        
        # Получаем данные закрытого тикета из сессии и передаем их в форму
        ticket_title = self.request.session.get('ticket_title')
        ticket_description = self.request.session.get('ticket_description')
        print(ticket_title)
        print(ticket_description)
        if ticket_title and ticket_description:
            context['form'] = self.get_form(self.form_class)  # Используем функцию get_form для получения формы
            context['form'].fields['title'].initial = ticket_title
            context['form'].fields['solution'].initial = ticket_description
        
        print(context)
        return context


    def get_success_url(self):
        return reverse_lazy('tickets')  # Правильный URL для перенаправления


def get_themes(request):
    topics = Theme.objects.all().values('id', 'name')  # Получаем данные в виде списка словарей
    return JsonResponse(list(topics), safe=False)


class KnowledgesListView(ListView):
    """Получение списка базы знаний"""

    model = KnowledgeBase
    template_name = 'tickets/knowledges.html'
    paginate_by = 4
    
    def get_user_knowledges(self, request):
        return KnowledgeBase.objects.filter(theme=request.GET.get("id")).order_by('-id')

    def get_queryset(self):
        knowledges = self.get_user_knowledges(self.request)
        return knowledges
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['theme'] = Theme.objects.get(id=self.request.GET.get("id"))
        return context


class ChangeStatusToInProgress(View):
    """Взять тикет в работу"""
    def post(self, request, pk):
        is_updated = Ticket.objects.filter(id=pk).update(status=Status.IN_PROGRESS)
        return redirect(reverse('tickets'))
