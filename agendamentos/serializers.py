from rest_framework import serializers
from .models import Agendamento, Servico, Paciente  # Importamos o modelo Paciente aqui também

# --- TRADUTOR DE AGENDAMENTOS ---
class AgendamentoSerializer(serializers.ModelSerializer):
    patientName = serializers.CharField(source='paciente.nome', read_only=True)
    service = serializers.CharField(source='servico.nome', read_only=True)
    notes = serializers.CharField(source='observacoes', allow_blank=True, required=False)
    
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    class Meta:
        model = Agendamento
        fields = ['id', 'patientName', 'date', 'time', 'service', 'notes']

    def get_date(self, obj):
        return obj.data_hora.strftime('%Y-%m-%d') if obj.data_hora else None

    def get_time(self, obj):
        return obj.data_hora.strftime('%H:%M') if obj.data_hora else None


# --- TRADUTOR DE SERVIÇOS ---
class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = '__all__'


# --- TRADUTOR DE PACIENTES ---
class PacienteSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='nome')
    birthDate = serializers.DateField(source='data_nascimento', required=False, allow_null=True)
    gender = serializers.CharField(source='genero', required=False, allow_blank=True, allow_null=True)
    phone = serializers.CharField(source='telefone', required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Paciente
        fields = ['id', 'name', 'cpf', 'birthDate', 'gender', 'phone']