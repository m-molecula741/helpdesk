from django.urls import path
from . import views


urlpatterns = [
    path('', views.TicketsListView.as_view(), name="tickets"),
    path('knowledges/', views.KnowledgesListView.as_view(), name="knowledges"),
    path('create/', views.CreateTicketView.as_view(), name="create_ticket"),
    path('themes/', views.get_themes, name="themes"),
    path('create/knowledge/', views.CreateKnowledge.as_view(), name="create_knowledge"),
    path('comment/<int:pk>/', views.CreateComment.as_view(), name="create_comment"),
    path('close/<int:pk>/', views.CloseTicket.as_view(), name="close_ticket"),
    path('detail/<int:pk>/', views.TicketDetail.as_view(), name="detail_ticket"),
]
