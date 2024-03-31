from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Ticket(models.Model):
    """Тикеты"""
    class Status(models.TextChoices):
        OPEN = 'open', _('Open')
        IN_PROGRESS = 'in_progress', _('In Progress')
        CLOSED = 'closed', _('Closed')

    class Priority(models.IntegerChoices):
        LOW = 3, _("Low")
        MEDIUM = 2, _("Medium")
        HIGH = 1, _("High")
    
    title = models.CharField(max_length=200)
    description = models.TextField("Описание")
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.OPEN
    )
    priority = models.PositiveSmallIntegerField(
        choices=Priority.choices, db_index=True, default=Priority.MEDIUM
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_tickets', null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='assigned_tickets', null=True, blank=True)
