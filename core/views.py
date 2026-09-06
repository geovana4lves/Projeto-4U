from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Tarefa, PostagemMural, MetaPessoal, Conquista, ConquistaUsuario, HistoricoPomodoro
from .forms import TarefaForm, PostagemMuralForm, MetaPessoalForm, PerfilForm
import json

def verificar_conquistas(usuario):
    tarefas_concluidas = Tarefa.objects.filter(usuario=usuario, concluida=True).count()
    pomodoros_concluidos = HistoricoPomodoro.objects.filter(usuario=usuario).count()
    metas_atingidas = MetaPessoal.objects.filter(usuario=usuario, atingida=True).count()

    regras = [
        (tarefas_concluidas >= 1, 'Primeiro Passo', 'Concluiu a primeira tarefa.', 'bi bi-check2-circle'),
        (tarefas_concluidas >= 10, 'Produtividade em Dia', 'Concluiu 10 tarefas.', 'bi bi-list-check'),
        (pomodoros_concluidos >= 1, 'Foco Iniciado', 'Completou o primeiro ciclo Pomodoro.', 'bi bi-stopwatch'),
        (pomodoros_concluidos >= 10, 'Mestre do Foco', 'Completou 10 ciclos Pomodoro.', 'bi bi-lightning-charge'),
        (metas_atingidas >= 1, 'Meta Alcançada', 'Atingiu a primeira meta pessoal.', 'bi bi-flag'),
    ]

    for atingida, nome, descricao, icone in regras:
        if atingida:
            conquista, _ = Conquista.objects.get_or_create(
                nome=nome, defaults={'descricao': descricao, 'icone': icone}
            )
            ConquistaUsuario.objects.get_or_create(usuario=usuario, conquista=conquista)

def landing_page(request):
    return render(request, 'core/landing.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return render(request, 'core/login.html')
    return render(request, 'core/login.html')

def cadastro_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'core/cadastro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuário já existe.')
            return render(request, 'core/cadastro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'E-mail já cadastrado.')
            return render(request, 'core/cadastro.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        user = authenticate(request, username=username, password=password)
        login(request, user)
        messages.success(request, 'Conta criada com sucesso!')
        return redirect('dashboard')

    return render(request, 'core/cadastro.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('landing_page')

@login_required
def dashboard_view(request):
    if request.method == 'POST':
        
        form_postagem = PostagemMuralForm(request.POST)
        if form_postagem.is_valid():
            postagem = form_postagem.save(commit=False)
            postagem.usuario = request.user
            postagem.save()
            messages.success(request, 'Postagem publicada no mural!')
        return redirect('dashboard')

    tarefas = Tarefa.objects.filter(usuario=request.user, concluida=False).order_by('data_execucao')
    postagens = PostagemMural.objects.filter(usuario=request.user).order_by('-data_criacao')

    context = {
        'tarefas': tarefas,
        'postagens': postagens,
        'form_postagem': PostagemMuralForm(),
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def calendario_view(request):
    tarefas = Tarefa.objects.filter(usuario=request.user).order_by('data_execucao')
    
    eventos = []
    for t in tarefas:
        eventos.append({
            'id': t.pk,
            'title': t.titulo,
            'start': str(t.data_execucao),
            'concluida': t.concluida,
        })
    
    context = {
        'tarefas': tarefas,
        'eventos_json': json.dumps(eventos),
    }
    return render(request, 'core/calendario.html', context)

@login_required
def conquistas_view(request):

    regras_iniciais = [
        ('Primeiro Passo', 'Concluiu a primeira tarefa.', 'bi bi-check2-circle'),
        ('Produtividade em Dia', 'Concluiu 10 tarefas.', 'bi bi-list-check'),
        ('Foco Iniciado', 'Completou o primeiro ciclo Pomodoro.', 'bi bi-stopwatch'),
        ('Mestre do Foco', 'Completou 10 ciclos Pomodoro.', 'bi bi-lightning-charge'),
        ('Meta Alcançada', 'Atingiu a primeira meta pessoal.', 'bi bi-flag'),
    ]
    for nome, descricao, icone in regras_iniciais:
        Conquista.objects.get_or_create(
            nome=nome, defaults={'descricao': descricao, 'icone': icone}
        )

    if request.method == 'POST':
        form_meta = MetaPessoalForm(request.POST)
        if form_meta.is_valid():
            meta = form_meta.save(commit=False)
            meta.usuario = request.user
            meta.save()
            messages.success(request, 'Meta pessoal criada com sucesso!')
            return redirect('conquistas')
    else:
        form_meta = MetaPessoalForm()

    metas = MetaPessoal.objects.filter(usuario=request.user)
    conquistas_usuario = ConquistaUsuario.objects.filter(usuario=request.user)
    catalogo_conquistas = Conquista.objects.all()

    context = {
        'form_meta': form_meta,
        'metas': metas,
        'conquistas': conquistas_usuario,
        'catalogo': catalogo_conquistas,
    }
    return render(request, 'core/conquistas.html', context)

@login_required
def perfil_view(request):

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=request.user)
    return render(request, 'core/perfil.html', {'form': form})


@login_required
def criar_tarefa_view(request):

    if request.method == 'POST':
        form = TarefaForm(request.POST)
        origem = request.POST.get('origem', 'dashboard')
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.usuario = request.user
            tarefa.save()
            messages.success(request, 'Tarefa criada com sucesso!')
            return redirect(origem if origem in ('dashboard', 'calendario') else 'dashboard')
    else:
        form = TarefaForm()
        origem = request.GET.get('origem', 'dashboard')
    return render(request, 'core/tarefa_form.html', {
        'form': form, 'modo': 'criar', 'origem': origem
    })


@login_required
def editar_tarefa_view(request, pk):

    tarefa = get_object_or_404(Tarefa, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = TarefaForm(request.POST, instance=tarefa)
        origem = request.POST.get('origem', 'calendario')
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarefa atualizada com sucesso!')
            return redirect(origem if origem in ('dashboard', 'calendario') else 'calendario')
    else:
        form = TarefaForm(instance=tarefa)
        origem = request.GET.get('origem', 'calendario')
    return render(request, 'core/tarefa_form.html', {
        'form': form, 'modo': 'editar', 'tarefa': tarefa, 'origem': origem
    })


@login_required
@require_POST
def excluir_tarefa_view(request, pk):

    tarefa = get_object_or_404(Tarefa, pk=pk, usuario=request.user)
    tarefa.delete()
    messages.success(request, 'Tarefa excluída.')
    origem = request.POST.get('origem', 'dashboard')
    return redirect(origem if origem in ('dashboard', 'calendario') else 'dashboard')


@login_required
@require_POST
def concluir_tarefa_view(request, pk):

    tarefa = get_object_or_404(Tarefa, pk=pk, usuario=request.user)
    tarefa.concluida = True
    tarefa.save()
    verificar_conquistas(request.user)
    messages.success(request, f'Tarefa "{tarefa.titulo}" concluída!')
    origem = request.POST.get('origem', 'dashboard')
    return redirect(origem if origem in ('dashboard', 'calendario') else 'dashboard')


@login_required
@require_POST
def concluir_meta_view(request, pk):
    meta = get_object_or_404(MetaPessoal, pk=pk, usuario=request.user)
    meta.atingida = True
    meta.save()
    verificar_conquistas(request.user)
    messages.success(request, f'Meta "{meta.titulo}" atingida! Parabéns!')
    return redirect('conquistas')

@login_required
def registrar_pomodoro(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        duracao = data.get('duracao', 60)

        HistoricoPomodoro.objects.create(
            usuario=request.user,
            duracao_minutos=duracao
        )
        
        verificar_conquistas(request.user)
        return JsonResponse({'status': 'sucesso', 'mensagem': 'Ciclo Pomodoro registrado com sucesso!'})
    return JsonResponse({'status': 'erro'}, status=400)

@login_required
@require_POST
def excluir_postagem_mural(request, pk):
    postagem = get_object_or_404(PostagemMural, pk=pk, usuario=request.user)
    postagem.delete()
    messages.success(request, 'Anotação excluída do mural com sucesso!')
    return redirect('dashboard')