from django.urls import path
from . import views


urlpatterns = [
    path('', views.TicketsListView.as_view(), name="tickets"),
    path('create/', views.CreateTicketView.as_view(), name="create_ticket"),
    path('<int:pk>/', views.TicketDetail.as_view(), name="detail_ticket"),
]
