from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('temas/', views.listar_temas, name='listar_temas'),  # Listar temas
    path('tema/novo/', views.cadastrar_tema,
         name='cadastrar_tema'),  # Cadastrar tema
    path('tema/<int:tema_id>/alocar/', views.alocar_grupos, name='alocar_grupos'),
    path('tema/<int:tema_id>/grupos/', views.listar_grupos, name='listar_grupos'),
    path('alunos/', views.listar_alunos, name='listar_alunos'),  # Listar alunos
    path('aluno/novo/', views.cadastrar_aluno,
         name='cadastrar_aluno'),  # Cadastrar aluno
]
