from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Status(models.TextChoices):
    OPEN = 'open', _('Open')
    IN_PROGRESS = 'in_progress', _('In Progress')
    CLOSED = 'closed', _('Closed')

class Priority(models.IntegerChoices):
    LOW = 3, _("Low")
    MEDIUM = 2, _("Medium")
    HIGH = 1, _("High")


class Ticket(models.Model):
    """Тикеты"""   
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


    def __str__(self):
        return self.title
    

class Comment(models.Model):
    """Коммменты"""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"comment to {self.ticket} ticket"


class Theme(models.Model):
    """Темы"""
    name = models.CharField(max_length=60)

    def __str__(self) -> str:
        return self.name


class KnowledgeBase(models.Model):
    """База знаний"""
    title = models.CharField(max_length=200)
    solution = models.TextField("Решение")
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, null=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.title


class New(models.Model):
    """Новости"""
    title = models.CharField(max_length=200)
    content = models.TextField("Контент")
    image = models.ImageField("Изображение", upload_to="news/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
