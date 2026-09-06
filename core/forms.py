from django import forms
from django.contrib.auth.models import User
from .models import Tarefa, PostagemMural, MetaPessoal

class UsuarioCadastroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Senha')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo', 'descricao', 'data_execucao', 'cor_etiqueta', 'tempo_estimado_minutos']
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição da tarefa',
            'data_execucao': 'Prazo',
            'cor_etiqueta': 'Cor da etiqueta',
            'tempo_estimado_minutos': 'Tempo estimado (minutos)',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'data_execucao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cor_etiqueta': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'tempo_estimado_minutos': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PostagemMuralForm(forms.ModelForm):
    class Meta:
        model = PostagemMural
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Escreva uma anotação ou lembrete...'}),
        }

class MetaPessoalForm(forms.ModelForm):
    class Meta:
        model = MetaPessoal
        fields = ['titulo', 'descricao', 'prazo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'prazo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }