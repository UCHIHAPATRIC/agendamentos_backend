from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/resumo/', views.dashboard_resumo, name='dashboard_resumo'),
    path('calendario/', views.gerenciar_agendamentos, name='gerenciar_agendamentos'),
    # Nova rota para atualizar ou deletar um agendamento específico:
    path('calendario/<int:pk>/', views.detalhar_agendamento, name='detalhar_agendamento'),
]