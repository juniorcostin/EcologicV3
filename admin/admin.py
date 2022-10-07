from flask_admin.contrib.sqla import ModelView
from datetime import datetime



###### Usuários ######
class tabela_usuarios(ModelView):
    column_list = [
        "admin", 
        "cadastrar", 
        "editar", 
        "deletar",
        "visualizar",
        "usuario_primeiro_nome", 
        "usuario_email", 
        "usuario_ativo", 
        "entidade_id"
        ]
    column_labels = dict(
        admin = 'Admin',
        cadastrar = 'Cadastrar',
        editar = 'Editar',
        deletar = 'Deletar',
        visualizar = 'Visualizar',
        usuario_primeiro_nome = 'Nome', 
        usuario_email = 'Email',
        usuario_ativo = 'Ativo',
        entidade_id = 'ID da Entidade'
        )

    form_create_rules = [
        'admin',
        'cadastrar',
        'editar',
        'deletar',
        'visualizar',
        'usuario_primeiro_nome',
        'usuario_segundo_nome',
        'usuario_email',
        'usuario_senha',
        'usuario_ativo',
        'entidade_id',
        'data_criacao',
        'hora_criacao',
        'data_atualizacao',
        'hora_atualizacao',
        'usuario_criador_id',
        'usuario_atualizacao_id'
    ]

    form_edit_rules = [
        'admin',
        'cadastrar',
        'editar',
        'deletar',
        'usuario_primeiro_nome',
        'usuario_ativo',
        'data_atualizacao',
        'hora_atualizacao',
        'usuario_atualizacao_id'
    ]

    column_searchable_list = ["usuario_email", "entidade_id"]


###### Entidades ######
class tabela_entidades(ModelView):
    column_list = [
        "entidade_id",
        "entidade_nome", 
        "entidade_ramo", 
        "dispositivos_quantidade",
        "cpfcnpj"
        ]
    column_labels = dict(
        entidade_nome = 'Nome',
        entidade_ramo = 'Ramo',
        dispositivos_quantidade = 'Quantidade de Dispositivos',
        cpfcnpj = 'CPF / CNPJ',
        entidade_id = 'ID'
        )
    column_searchable_list = ["entidade_nome", "cpfcnpj", "entidade_id"]

###### Dispositivos ######
class tabela_dispositivos(ModelView):
    column_list = [
        "dispositivo_nome", 
        "dispositivo_tipo", 
        "dispositivo_descricao",
        "dispositivo_ativo", 
        "entidade_id"
        ]
    column_labels = dict(
        dispositivo_nome = 'Nome',
        dispositivo_tipo = 'Tipo',
        dispositivo_descricao = 'Descrição',
        dispositivo_ativo = 'Ativo',
        entidade_id = 'ID da Entidade'
        )
    column_searchable_list = ["dispositivo_nome", "dispositivo_tipo", "entidade_id"]


