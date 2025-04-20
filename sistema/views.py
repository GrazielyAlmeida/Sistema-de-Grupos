from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Aluno, Tema, Grupo
from .forms import AlunoForm, TemaForm
from .utils import distribuir_alunos_e_sortear

# Página inicial


def home(request):
    return render(request, 'home.html')

# Cadastrar aluno


def cadastrar_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            # Mensagem de sucesso
            messages.success(request, "Aluno cadastrado com sucesso!")
            form = AlunoForm()  # Limpa o formulário após o envio
    else:
        form = AlunoForm()
    return render(request, 'cadastrar_aluno.html', {'form': form})

# Listar alunos


def listar_alunos(request):
    alunos = Aluno.objects.all()
    paginator = Paginator(alunos, 10)  # 10 alunos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listar_alunos.html', {'page_obj': page_obj})

# Cadastrar tema


def cadastrar_tema(request):
    """
    View para cadastrar um novo tema.
    """
    if request.method == 'POST':
        form = TemaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tema cadastrado com sucesso!")
            # Redireciona para a lista de temas
            return redirect('listar_temas')
    else:
        form = TemaForm()
    return render(request, 'cadastrar_tema.html', {'form': form})

# Listar temas


def listar_temas(request):
    """
    View para listar todos os temas cadastrados.
    """
    temas = Tema.objects.all()  # Obtém todos os temas do banco de dados
    return render(request, 'listar_temas.html', {'temas': temas})

# Alocar grupos


def alocar_grupos(request, tema_id):
    """
    View para alocar alunos automaticamente nos grupos e sortear a ordem de apresentação.
    """
    tema = get_object_or_404(
        Tema, id=tema_id)  # Busca o tema pelo ID ou retorna 404

    # Verificar se os grupos já foram criados para o tema
    if Grupo.objects.filter(tema=tema).exists():
        messages.warning(
            request, "Os grupos já foram alocados para este tema.")
        return redirect('listar_grupos', tema_id=tema.id)

    alunos = Aluno.objects.all()  # Obtém todos os alunos cadastrados

    if not alunos.exists():
        messages.error(request, "Não há alunos cadastrados para alocar.")
        return redirect('listar_temas')  # Redireciona para a lista de temas

    if alunos.count() < tema.quantidade_grupos:
        messages.error(
            request, "O número de alunos é insuficiente para formar os grupos.")
        return redirect('listar_temas')

    # Chama a função de alocação e sorteio
    distribuir_alunos_e_sortear(tema, alunos)
    messages.success(
        request, "Grupos alocados e ordem de apresentação sorteada com sucesso!")
    # Redireciona para a lista de grupos
    return redirect('listar_grupos', tema_id=tema.id)

# Listar grupos


def listar_grupos(request, tema_id):
    """
    View para listar os grupos de um tema específico.
    """
    tema = get_object_or_404(Tema, id=tema_id)
    grupos = Grupo.objects.filter(tema=tema).order_by('ordem_apresentacao')
    return render(request, 'listar_grupos.html', {'tema': tema, 'grupos': grupos})
