# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver

from django.db import models

class Paciente(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=50, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nome
    
class Servico(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    class StatusChoices(models.TextChoices):
        A_CONFIRMAR = 'A_CONFIRMAR', 'A Confirmar'
        CONFIRMADO = 'CONFIRMADO', 'Confirmado'
        ESPERANDO = 'ESPERANDO', 'Recepção (Esperando)'
        FINALIZADO = 'FINALIZADO', 'Finalizado'

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.SET_NULL, null=True)
    data_hora = models.DateTimeField()
    status = models.CharField(
        max_length=20, 
        choices=StatusChoices.choices, 
        default=StatusChoices.A_CONFIRMAR
    )
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.paciente.nome} - {self.data_hora}"