from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime
from .models import Agendamento, Paciente, Servico
from .serializers import AgendamentoSerializer

@api_view(['GET'])
def dashboard_resumo(request):
    hoje = timezone.now().date()
    
    # Filtra agendamentos do dia de hoje
    agendamentos_hoje = Agendamento.objects.filter(data_hora__date=hoje)
    
    # Contagens específicas para os cards do Front-end
    total_hoje = agendamentos_hoje.filter(status='CONFIRMADO').count()
    esperando = agendamentos_hoje.filter(status='ESPERANDO').count()
    a_confirmar = Agendamento.objects.filter(status='A_CONFIRMAR').count()
    total_pacientes = Paciente.objects.count()
    
    return Response({
        "agendamentosHoje": total_hoje,
        "recepcaoEsperando": esperando,
        "agendamentosAConfirmar": a_confirmar,
        "totalPacientes": total_pacientes
    })

# --- ROTA ATUALIZADA PARA ACEITAR GET E POST ---
@api_view(['GET', 'POST'])
def gerenciar_agendamentos(request):
    if request.method == 'GET':
        # Pega todos os agendamentos no banco de dados
        agendamentos = Agendamento.objects.all()
        serializer = AgendamentoSerializer(agendamentos, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        dados = request.data
        
        # 1. Recuperar ou criar o Paciente pelo nome enviado
        nome_paciente = dados.get('patientName')
        if not nome_paciente:
            return Response({"erro": "O nome do paciente é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
        paciente, _ = Paciente.objects.get_or_create(nome=nome_paciente)
        
        # 2. Recuperar ou criar o Serviço/Especialidade pelo nome enviado
        nome_servico = dados.get('service')
        servico = None
        if nome_servico:
            servico, _ = Servico.objects.get_or_create(
                nome=nome_servico, 
                defaults={'preco': 0.00}
            )
            
        # 3. Combinar 'date' (YYYY-MM-DD) e 'time' (HH:MM) num único datetime
        str_data = dados.get('date') 
        str_hora = dados.get('time')
        
        if not str_data or not str_hora:
            return Response({"erro": "Data e horário são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # Junta as strings e converte para objeto datetime
            data_hora_nativa = datetime.strptime(f"{str_data} {str_hora}", "%Y-%m-%d %H:%M")
            # Torna o datetime ciente do fuso horário configurado no Django
            data_hora_fuso = timezone.make_aware(data_hora_nativa)
        except ValueError:
            return Response({"erro": "Formato de data ou hora inválido."}, status=status.HTTP_400_BAD_REQUEST)
            
        # 4. Criar e salvar o Agendamento no banco de dados SQLite
        novo_agendamento = Agendamento.objects.create(
            paciente=paciente,
            servico=servico,
            data_hora=data_hora_fuso,
            observacoes=dados.get('notes', ''),
            status='A_CONFIRMAR' # Todo agendamento novo começa a confirmar
        )
        
        # Retorna o agendamento acabado de criar no formato do formulário
        serializer = AgendamentoSerializer(novo_agendamento)
        return Response(serializer.data, status=status.HTTP_201_CREATED)