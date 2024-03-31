from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Ticket


class CreateTicketView(CreateView):
    model = Ticket
    fields = ['title', 'description', 'status', 'priority']  # поля, которые будут отображаться в форме
    template_name = 'tickets/create_ticket.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('home')
