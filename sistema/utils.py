import random
from datetime import timedelta, datetime
from .models import Grupo, Aluno


def distribuir_alunos_e_sortear(tema, alunos):
    # Embaralhar os alunos para garantir aleatoriedade
    alunos = list(alunos)
    random.shuffle(alunos)

    # Criar os grupos
    grupos = []
    for i in range(tema.quantidade_grupos):
        grupo = Grupo.objects.create(
            tema=tema,
            nome=f"Grupo {i + 1}"
        )
        grupos.append(grupo)

    # Distribuir os alunos igualmente entre os grupos
    for i, aluno in enumerate(alunos):
        grupos[i % tema.quantidade_grupos].alunos.add(aluno)

    # Sortear a ordem dos grupos
    random.shuffle(grupos)

    # Calcular horários de apresentação
    tempo_por_grupo = timedelta(minutes=30)  # Tempo mínimo por grupo
    horario_atual = datetime.combine(datetime.today(), tema.horario_inicio)

    for ordem, grupo in enumerate(grupos, start=1):
        grupo.ordem_apresentacao = ordem
        grupo.horario_apresentacao = horario_atual.time()
        grupo.save()
        horario_atual += tempo_por_grupo
