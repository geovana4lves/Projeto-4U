# 4U — Sistema integrado de planejamento diário e gestão de tempo

Projeto Django desenvolvido para o Instituto Federal Baiano — Campus Guanambi,
conforme o *Documento de Requisitos* do sistema 4U.

## Como rodar o projeto

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Acesse http://127.0.0.1:8000/

## Estrutura do projeto

```
Projeto-4U-main/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── .gitignore
├── config/                 # Pacote de configuração do Django (settings, urls, wsgi, asgi)
└── core/                   # App principal com toda a regra de negócio do 4U
    ├── models.py            # Tarefa, PostagemMural, MetaPessoal, Conquista, ConquistaUsuario, HistoricoPomodoro
    ├── forms.py             # Formulários de cadastro, tarefa, mural, meta e perfil
    ├── views.py             # Lógica das telas e regras de conquistas
    ├── urls.py              # Rotas do app
    ├── admin.py             # Registro dos modelos no Django Admin
    ├── migrations/
    └── templates/core/      # Templates HTML (Bootstrap 5)
```

> A reorganização removeu uma pasta `config/config/` e um `manage.py` duplicados
> que eram resíduos de uma segunda execução do `startproject` e não eram usados
> pela aplicação, além de um arquivo solto (`teste`) e dos `__pycache__`
> versionados. O `requirements.txt`, que estava salvo em UTF-16, foi
> reconvertido para UTF-8 padrão.

## Rastreabilidade dos requisitos

| Requisito | Descrição | Onde está implementado |
|---|---|---|
| RF001 | Cadastro de usuários | `cadastro_view` → `/cadastro/` |
| RF002 | Login no sistema | `login_view` → `/login/` |
| RF003 | Edição de perfil | `perfil_view` → `/perfil/` (novo) |
| RF004 | Criar tarefas | `criar_tarefa_view` → `/tarefas/nova/` (novo) |
| RF005 | Editar tarefas | `editar_tarefa_view` → `/tarefas/<id>/editar/` (novo) |
| RF006 | Excluir tarefas | `excluir_tarefa_view` → `/tarefas/<id>/excluir/` (novo) |
| RF007 | Visualizar calendário | `calendario_view` → `/calendario/` |
| RF008 | Personalizar calendário | Cor da etiqueta e edição via `editar_tarefa_view` |
| RF009 | Criar postagens no mural | Formulário embutido em `dashboard_view` (novo) |
| RF010 | Cronômetro nas tarefas | Campo `tempo_estimado_minutos` em `Tarefa`, exibido no dashboard |
| RF011 | Criar metas pessoais | Formulário embutido em `conquistas_view` (novo) |
| RF012 | Sistema de conquistas | `verificar_conquistas()` concede medalhas automaticamente (novo) |
| RF013 | Timer Pomodoro | Widget JS no dashboard + `registrar_pomodoro` (API) |
| RNF001 | Interface intuitiva | Bootstrap 5 + navegação consistente em `base.html` |
| RNF002 | Tempo de resposta < 3s | Operações assíncronas (fetch) para o Pomodoro |
| RNF003 | Compatibilidade com navegadores | Uso de Bootstrap/CSS padrão, sem recursos proprietários |
