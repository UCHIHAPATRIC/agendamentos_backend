from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import Agendamento, Paciente

@api_view(['GET'])
def dashboard_resumo(request):
    hoje = timezone.now().date()
    
    # Filtra agendamentos do dia de hoje
    agendamentos_hoje = Agendamento.objects.filter(data_hora__date=hoje)
    
    # Contagens específicas para os cards do Front-end
    total_hoje = agendamentos_hoje.filter(status='CONFIRMADO').count()
    esperando = agendamentos_hoje.filter(status='ESPERANDO').count()
    a_confirmar = Agendamento.objects.filter(status='A_CONFIRMAR').count() # Pode ser de qualquer dia
    total_pacientes = Paciente.objects.count()
    
    return Response({
        "agendamentosHoje": total_hoje,
        "recepcaoEsperando": esperando,
        "agendamentosAConfirmar": a_confirmar,
        "totalPacientes": total_pacientes
    })