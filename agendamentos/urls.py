from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/resumo/', views.dashboard_resumo, name='dashboard_resumo'),
    path('calendario/', views.gerenciar_agendamentos, name='gerenciar_agendamentos'),
    path('calendario/<int:pk>/', views.detalhar_agendamento, name='detalhar_agendamento'),
    path('servicos/', views.listar_servicos, name='listar_servicos'),
    path('pacientes/', views.gerenciar_pacientes, name='gerenciar_pacientes'),
    path('pacientes/<int:pk>/', views.detalhar_paciente, name='detalhar_paciente'),
]