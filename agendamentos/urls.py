from django.urls import path
from . import views

urlpatterns = [
    # Rota correspondente a: /api/dashboard/resumo/
    path('dashboard/resumo/', views.dashboard_resumo, name='dashboard_resumo'),
]