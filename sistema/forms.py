from django import forms
from .models import Aluno, Tema


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'matricula']


class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ['titulo', 'quantidade_grupos', 'alunos_por_grupo',
                  'data_apresentacao', 'horario_inicio', 'horario_fim']
        widgets = {
            'data_apresentacao': forms.DateInput(attrs={'type': 'date'}),
            'horario_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'horario_fim': forms.TimeInput(attrs={'type': 'time'}),
        }
