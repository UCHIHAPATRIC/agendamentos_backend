from django.contrib import admin
from .models import Paciente, Servico, Agendamento

admin.site.register(Paciente)
admin.site.register(Servico)
admin.site.register(Agendamento)