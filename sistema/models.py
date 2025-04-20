from django.db import models
from django.core.exceptions import ValidationError

# Modelo Aluno


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nome

# Modelo Tema


class Tema(models.Model):
    titulo = models.CharField(max_length=200)
    quantidade_grupos = models.PositiveIntegerField()
    alunos_por_grupo = models.PositiveIntegerField()
    data_apresentacao = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()

    def clean(self):
        if self.horario_inicio >= self.horario_fim:
            raise ValidationError(
                "O horário de início deve ser anterior ao horário de fim.")

    def __str__(self):
        return self.titulo

# Modelo Grupo


class Grupo(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    alunos = models.ManyToManyField(Aluno)
    horario_apresentacao = models.TimeField(null=True, blank=True)
    ordem_apresentacao = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.nome
