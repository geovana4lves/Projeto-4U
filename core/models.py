from django.db import models
from django.contrib.auth.models import User

class Tarefa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tarefas')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    data_execucao = models.DateField()  
    concluida = models.BooleanField(default=False)
    cor_etiqueta = models.CharField(max_length=7, default="#3498db")  
    tempo_estimado_minutos = models.IntegerField(default=0)  

    def __str__(self):
        return self.titulo

class PostagemMural(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postagens')
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Postagem de {self.usuario.username} em {self.data_criacao.strftime('%d/%m/%Y')}"

class MetaPessoal(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metas')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    prazo = models.DateField()
    atingida = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

class Conquista(models.Model):
    nome = models.CharField(max_length=180)
    descricao = models.TextField()
    icone = models.CharField(max_length=50) 

    def __str__(self):
        return self.nome

class ConquistaUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    conquista = models.ForeignKey(Conquista, on_delete=models.CASCADE)
    data_ganha = models.DateTimeField(auto_now_add=True)

class HistoricoPomodoro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_hora_conclusao = models.DateTimeField(auto_now_add=True)
    duracao_minutos = models.IntegerField(default=60)