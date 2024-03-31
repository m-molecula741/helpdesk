from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.CreateTicketView.as_view(), name="create_ticket"),
]