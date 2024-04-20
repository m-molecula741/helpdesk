from django.contrib import admin

from .models import Ticket, Comment, Theme, KnowledgeBase, New

admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(Theme)
admin.site.register(KnowledgeBase)
admin.site.register(New)