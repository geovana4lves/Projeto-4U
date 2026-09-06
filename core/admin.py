from django.contrib import admin
from .models import Tarefa, PostagemMural, MetaPessoal, Conquista, ConquistaUsuario, HistoricoPomodoro

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'data_execucao', 'concluida']
    list_filter = ['concluida', 'usuario']

@admin.register(PostagemMural)
class PostagemMuralAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'data_criacao']

@admin.register(MetaPessoal)
class MetaPessoalAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'usuario', 'prazo', 'atingida']

@admin.register(Conquista)
class ConquistaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'icone']

@admin.register(ConquistaUsuario)
class ConquistaUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'conquista', 'data_ganha']

@admin.register(HistoricoPomodoro)
class HistoricoPomodoroAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'duracao_minutos', 'data_hora_conclusao']
