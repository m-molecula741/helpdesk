from django.urls import path
from . import views


urlpatterns = [
    path('', views.TicketsListView.as_view(), name="tickets"),
    path('create/', views.CreateTicketView.as_view(), name="create_ticket"),
    path('comment/<int:pk>/', views.CreateComment.as_view(), name="create_comment"),
    path('close/<int:pk>/', views.CloseTicket.as_view(), name="close_ticket"),
    path('detail/<int:pk>/', views.TicketDetail.as_view(), name="detail_ticket"),
]
