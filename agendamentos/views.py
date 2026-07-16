from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime
from .models import Agendamento, Paciente, Servico
from .serializers import AgendamentoSerializer, ServicoSerializer, PacienteSerializer

@api_view(['GET'])
def dashboard_resumo(request):
    hoje = timezone.now().date()
    

    agendamentos_hoje = Agendamento.objects.filter(data_hora__date=hoje)
    

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

# ---GET E POST ---
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
        

        nome_servico = dados.get('service')
        servico = None
        if nome_servico:
            servico, _ = Servico.objects.get_or_create(
                nome=nome_servico, 
                defaults={'preco': 0.00}
            )
            
#  Combinar 'date' (YYYY-MM-DD) e 'time' (HH:MM) num único datetime
        str_data = dados.get('date') 
        str_hora = dados.get('time')
        
        if not str_data or not str_hora:
            return Response({"erro": "Data e horário são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            data_hora_nativa = datetime.strptime(f"{str_data} {str_hora}", "%Y-%m-%d %H:%M")
            data_hora_fuso = timezone.make_aware(data_hora_nativa)
        except ValueError:
            return Response({"erro": "Formato de data ou hora inválido."}, status=status.HTTP_400_BAD_REQUEST)
            
#  Criar e salvar o Agendamento no banco de dados SQLite
        novo_agendamento = Agendamento.objects.create(
            paciente=paciente,
            servico=servico,
            data_hora=data_hora_fuso,
            observacoes=dados.get('notes', ''),
            status='A_CONFIRMAR'
        )
        
        serializer = AgendamentoSerializer(novo_agendamento)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['PUT', 'DELETE'])
def detalhar_agendamento(request, pk):
    try:
# Tenta encontrar o agendamento pelo ID 
        agendamento = Agendamento.objects.get(pk=pk)
    except Agendamento.DoesNotExist:
        return Response({"erro": "Agendamento não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
# --- EXCLUIR (DELETE) ---
    if request.method == 'DELETE':
        agendamento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
# --- ATUALIZAÇÃO (PUT) ---
    elif request.method == 'PUT':
        dados = request.data
        
# Atualiza Paciente
        nome_paciente = dados.get('patientName')
        if nome_paciente:
            paciente, _ = Paciente.objects.get_or_create(nome=nome_paciente)
            agendamento.paciente = paciente
            
# Atualiza Serviço
        nome_servico = dados.get('service')
        if nome_servico:
            servico, _ = Servico.objects.get_or_create(nome=nome_servico, defaults={'preco': 0.00})
            agendamento.servico = servico
            
# Atualiza Data e Hora
        str_data = dados.get('date') 
        str_hora = dados.get('time')
        if str_data and str_hora:
            try:
                data_hora_nativa = datetime.strptime(f"{str_data} {str_hora}", "%Y-%m-%d %H:%M")
                agendamento.data_hora = timezone.make_aware(data_hora_nativa)
            except ValueError:
                return Response({"erro": "Formato de data ou hora inválido."}, status=status.HTTP_400_BAD_REQUEST)
                
# Atualiza Observações
        if 'notes' in dados:
            agendamento.observacoes = dados.get('notes')
            
        agendamento.save()
        
        serializer = AgendamentoSerializer(agendamento)
        return Response(serializer.data)

# --- LISTAR SERVIÇOS ---
@api_view(['GET'])
def listar_servicos(request):
    servicos = Servico.objects.all()
    serializer = ServicoSerializer(servicos, many=True)
    return Response(serializer.data)

# --- GERENCIAR PACIENTES (CLIENTES)  ---
@api_view(['GET', 'POST'])
def gerenciar_pacientes(request):
    if request.method == 'GET':
        pacientes = Paciente.objects.all()
        serializer = PacienteSerializer(pacientes, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        serializer = PacienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- DETALHAR PACIENTES (CLIENTES) ---
@api_view(['PUT', 'DELETE'])
def detalhar_paciente(request, pk):
    try:
        paciente = Paciente.objects.get(pk=pk)
    except Paciente.DoesNotExist:
        return Response({"erro": "Paciente não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = PacienteSerializer(paciente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        paciente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)