from rest_framework import serializers
from .models import Agendamento

class AgendamentoSerializer(serializers.ModelSerializer):
    # Mapeamos as chaves do frontend para os campos do nosso banco
    patientName = serializers.CharField(source='paciente.nome', read_only=True)
    service = serializers.CharField(source='servico.nome', read_only=True)
    notes = serializers.CharField(source='observacoes', allow_blank=True, required=False)
    
    # Campos personalizados para separar a data e a hora
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    class Meta:
        model = Agendamento
        # Definimos exatamente a lista que a sua irmã enviou
        fields = ['id', 'patientName', 'date', 'time', 'service', 'notes']

    def get_date(self, obj):
        # Converte a data_hora para 'YYYY-MM-DD'
        return obj.data_hora.strftime('%Y-%m-%d') if obj.data_hora else None

    def get_time(self, obj):
        # Converte a data_hora para 'HH:MM'
        return obj.data_hora.strftime('%H:%M') if obj.data_hora else None