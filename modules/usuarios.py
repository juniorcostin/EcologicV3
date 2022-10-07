# Imports nencessários para que os Endpoints funcionem corretamente
import json
from datetime import datetime
from multiprocessing import set_forkserver_preload

from admin.admin import tabela_usuarios
from config.config import admin, db
from flask import Response
from werkzeug.security import check_password_hash, generate_password_hash

# Funções para definição de data/hora para alteração e criação
def data():
    data = datetime.now()
    return data.strftime('%Y-%m-%d')
def hora():
    hora = datetime.now()
    return hora.strftime('%H:%M:%S')

####################### DATABASE #######################

# CLASS que realiza a criação das colunas no banco de dados caso ele já não esteja incluso
# Também possui a função to_json que converte os campos do banco de dados para JSON
# Além das definições para encriptografia de senhas 
class Usuarios(db.Model):
    usuario_id = db.Column(db.Integer, primary_key=True)
    usuario_primeiro_nome = db.Column(db.String(100), nullable=False)
    usuario_segundo_nome = db.Column(db.String(100), nullable=False)
    usuario_email = db.Column(db.String(100), nullable=False, unique=True)
    usuario_senha = db.Column(db.String(255), nullable=False)
    usuario_ativo = db.Column(db.Boolean, nullable=False)
    entidade_id = db.Column(db.Integer, nullable=False)
    data_criacao = db.Column(db.Date)
    hora_criacao = db.Column(db.Time)
    data_atualizacao = db.Column(db.Date)
    hora_atualizacao = db.Column(db.Time)
    usuario_criador_id = db.Column(db.Integer)
    usuario_atualizacao_id = db.Column(db.Integer)
    admin = db.Column(db.Boolean, nullable=False)
    cadastrar = db.Column(db.Boolean, nullable=False)
    editar = db.Column(db.Boolean, nullable=False)
    deletar = db.Column(db.Boolean, nullable=False)
    visualizar = db.Column(db.Boolean, nullable=False)

    def __init__(self,
                 usuario_primeiro_nome,
                 usuario_segundo_nome,
                 usuario_email,
                 usuario_senha,
                 usuario_ativo,
                 entidade_id,
                 data_criacao,
                 hora_criacao,
                 data_atualizacao,
                 hora_atualizacao,
                 usuario_criador_id,
                 usuario_atualizacao_id,
                 admin,
                 cadastrar,
                 editar,
                 deletar,
                 visualizar
                 ):
        self.usuario_primeiro_nome = usuario_primeiro_nome
        self.usuario_segundo_nome = usuario_segundo_nome
        self.usuario_email = usuario_email
        self.usuario_senha = generate_password_hash(usuario_senha)
        self.usuario_ativo = usuario_ativo
        self.entidade_id = entidade_id
        self.data_criacao = data_criacao
        self.hora_criacao = hora_criacao
        self.data_atualizacao = data_atualizacao
        self.hora_atualizacao = hora_atualizacao
        self.usuario_criador_id = usuario_criador_id
        self.usuario_atualizacao_id = usuario_atualizacao_id
        self.admin = admin
        self.cadastrar = cadastrar
        self.editar = editar
        self.deletar = deletar
        self.visualizar = visualizar

    def verifica_senha(self, senha):
        return check_password_hash(self.usuario_senha, senha)

    def to_json(self):
        return {"usuario_id": self.usuario_id,
                "usuario_primeiro_nome": self.usuario_primeiro_nome,
                "usuario_segundo_nome": self.usuario_segundo_nome,
                "usuario_email": self.usuario_email,
                "usuario_senha": self.usuario_senha,
                "usuario_ativo": self.usuario_ativo,
                "entidade_id": self.entidade_id,
                "data_criacao": self.data_criacao,
                "hora_criacao": self.hora_criacao,
                "data_atualizacao": self.data_atualizacao,
                "hora_atualizacao": self.hora_atualizacao,
                "usuario_criador_id": self.usuario_criador_id,
                "usuario_atualizacao_id": self.usuario_atualizacao_id,
                "admin": self.admin,
                "cadastrar": self.cadastrar,
                "editar": self.editar,
                "deletar": self.deletar,
                "visualizar": self.visualizar
                }

# Paramentro para criar a tabela dentro da interface Admin do sistema
admin.add_view(tabela_usuarios(Usuarios, db.session))

# Função que filtra usuários pelo e-mail
def user_by_email(email):
    try:
        return Usuarios.query.filter(Usuarios.usuario_email == email).one()
    except:
        return None

# Endpoint GET que lista todos os usuários cadastrados dentro do banco de dados
def usuarios_seleciona_todos(current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_entidade_id = current_user.entidade_id
        login_admin = current_user.admin
        login_visualizar = current_user.visualizar

        # If para validar se o usuário tem as permissões
        if login_admin == True or login_visualizar == True:
            usuarios = Usuarios.query.filter_by(entidade_id=login_entidade_id)
            usuarios_json = [usuario.to_json() for usuario in usuarios]
            return gera_response(200, "Usuarios", usuarios_json, "Usuarios listados com sucesso!")
        else:
            return gera_response(403, "Usuarios", {}, "Você não tem permissão para listar os usuários!")
    except Exception as e:
        return gera_response(400, "Usuarios", {}, f"Falha ao listar usuarios! Mensagem: {e}")

# Endpoint GET que lista apenas um dispositivo, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
def usuarios_seleciona_um(id, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_entidade_id = current_user.entidade_id
        login_admin = current_user.admin
        login_visualizar = current_user.visualizar

        # IF para validar se o ID informado está cadastrado no banco de dados
        if not Usuarios.query.filter_by(usuario_id=id).first():
            return gera_response(400, "Usuarios", {}, f"Falha ao listar usuario! Mensagem: O usuário ID:{id} não existe!")

        # IF para validar se o usuário informado é da mesma entidade que o usuário logado
        valida_entidade = Usuarios.query.filter_by(usuario_id=id).first()
        if valida_entidade.to_json()["entidade_id"] != login_entidade_id:
            return gera_response(403, "Usuarios", {}, "Você não tem permissão para listar o usuário!")

        # If para validar se o usuário tem as permissões
        if login_admin == True or login_visualizar == True:
            usuario = Usuarios.query.filter_by(usuario_id=id, entidade_id=login_entidade_id).first()
            usuarios_json = usuario.to_json()
            return gera_response(200, "Usuarios", usuarios_json, "Usuario listado com sucesso!")
        else:
            return gera_response(403, "Usuarios", {}, "Você não tem permissão para listar o usuário!")
    except Exception as e:
        return gera_response(400, "Usuarios", {}, f"Falha ao listar usuario! Mensagem: {e}")

# Endpoint POST que é responsável por realizar a criação de um novo usuário dentro do banco de dados
# Deve ser informado o body da requisição com as informações corretas para a criação
def usuarios_criar(body, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_usuario_id = current_user.usuario_id
        login_entidade_id = current_user.entidade_id
        login_admin = current_user.admin
        login_cadastrar = current_user.cadastrar
        body_usuario_email = body["usuario_email"]

        # IF para validar se o email informado já está cadastrado no banco de dados
        if Usuarios.query.filter_by(usuario_email=body_usuario_email).first():
            return gera_response(400, "Usuarios", {}, f"Falha ao criar usuario! Mensagem: O email {body_usuario_email} já existe!")

        # IF que valida se o usuário tem as permissões necessárias para realizar a criação de outros usuários
        if login_admin == True or login_cadastrar == True:
            usuario = Usuarios(
                usuario_primeiro_nome=body["usuario_primeiro_nome"],
                usuario_segundo_nome=body["usuario_segundo_nome"],
                usuario_email=body["usuario_email"],
                usuario_senha=body["usuario_senha"],
                data_criacao=data(),
                hora_criacao=hora(),
                data_atualizacao=data(),
                hora_atualizacao=hora(),
                usuario_ativo=body["usuario_ativo"],
                entidade_id=login_entidade_id,
                usuario_criador_id=login_usuario_id,
                usuario_atualizacao_id=0,
                admin=body["admin"],
                cadastrar=body["cadastrar"],
                editar=body["editar"],
                deletar=body["deletar"],
                visualizar=body["visualizar"]
            )
            db.session.add(usuario)
            db.session.commit()
            return gera_response(201, "Usuarios", usuario.to_json(), "Usuario cadastrado com sucesso!")
        else:
            return gera_response(403, "Usuarios", {}, "Você não tem permissão para cadastrar o usuário!")
    except Exception as e:
        print(e)
        return gera_response(400, "Usuarios", {}, f"Erro ao Cadastrar usuario:{e}")

# Endpoint PUT responsável pela atualização de usuários
# Deve ser informado o ID do usuário existente no banco de dados
# O body da requisição não necessáriamente precisa conter todos os campos
def usuarios_atualiza(id, body, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_usuario_id = current_user.usuario_id
        login_entidade_id = current_user.entidade_id
        login_admin = current_user.admin
        login_editar = current_user.editar

        # IF para validar se o ID informado está cadastrado no banco de dados
        if not Usuarios.query.filter_by(usuario_id=id).first():
            return gera_response(400, "Usuarios", {}, f"Falha ao listar usuario! Mensagem: O usuário ID:{id} não existe!") 

        usuarios = Usuarios.query.filter_by(usuario_id=id).first()
        usuario_json = usuarios.to_json()
        
        # IF para validar se a entidade do usuário logado é igual ao do usuário informado
        if usuario_json["entidade_id"] != login_entidade_id:
            return gera_response(403, "Usuarios", {}, "Você não tem permissão para editar o usuário!")

        # IF para validar se o usuário tem as permissões nencessárias para editar o usuário
        if login_admin == True or login_editar == True:
            if "usuario_email" in body:
                usuarios.usuario_email = body["usuario_email"]
                usuarios.data_atualizacao = data()
                usuarios.hora_atualizacao = hora()
                usuarios.usuario_atualizacao_id = login_usuario_id
            if "usuario_senha" in body:
                usuarios.usuario_senha = body["usuario_senha"]
                usuarios.data_atualizacao = data()
                usuarios.hora_atualizacao = hora()
                usuarios.usuario_atualizacao_id = login_usuario_id
            if "usuario_ativo" in body:
                usuarios.usuario_ativo = body["usuario_ativo"]
                usuarios.data_atualizacao = data()
                usuarios.hora_atualizacao = hora()
                usuarios.usuario_atualizacao_id = login_usuario_id
            if "entidade_id" in body:
                usuarios.entidade_id = body["entidade_id"]
                usuarios.data_atualizacao = data()
                usuarios.hora_atualizacao = hora()
                usuarios.usuario_atualizacao_id = login_usuario_id
            if "admin" in body:
                usuarios.admin = body["admin"]
                usuarios.data_atualizacao = data()
                usuarios.hora_atualizacao = hora()
                usuarios.usuario_atualizacao_id = login_usuario_id
            if "cadastrar" in body:
                usuarios.cadastrar = body["cadastrar"]
                usuarios.data_atualizacao = data()
                usuarios.hora_atualizacao = hora()
                usuarios.usuario_atualizacao_id = login_usuario_id
            if "editar" in body:
                usuarios.editar = body["deletar"]
                usuarios.data_atualizacao = data()
                usuarios.hora_atualizacao = hora()
                usuarios.usuario_atualizacao_id = login_usuario_id
            if "visualizar" in body:
                usuarios.visualizar = body["visualizar"]
                usuarios.data_atualizacao = data()
                usuarios.hora_atualizacao = hora()
                usuarios.usuario_atualizacao_id = login_usuario_id

            db.session.add(usuarios)
            db.session.commit()
            return gera_response(200, "Usuarios", usuarios.to_json(), "Usuario atualizado com sucesso!")
    except Exception as e:
        return gera_response(400, "Usuarios", {}, f"Erro ao Atualizar usuario:{e}")

# Endpoint DELETE responsável por deletar um usuário
# Deve ser informado o ID do usuário 
def usuarios_deleta(id, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_entidade_id = current_user.entidade_id
        login_admin = current_user.admin
        login_deletar = current_user.deletar

        # IF para validar se o ID informado está cadastrado no banco de dados
        if not Usuarios.query.filter_by(usuario_id=id).first():
            return gera_response(400, "Usuarios", {}, f"Falha ao listar usuario! Mensagem: O usuário ID:{id} não existe!")

        usuarios = Usuarios.query.filter_by(usuario_id=id).first()
        usuario_json = usuarios.to_json()
        
        # IF para validar se a entidade do usuário logado é igual ao do usuário informado
        if usuario_json["entidade_id"] != login_entidade_id:
            return gera_response(403, "Usuarios", {}, "Você não tem permissão para editar o usuário!")

        # IF para validar se o usuário tem a permissão necessária para deletar o usuário
        if login_admin == True or login_deletar == True:
            db.session.delete(usuarios)
            db.session.commit()
            return gera_response(200, "Usuarios", usuarios.to_json(), "Usuario deletado com sucesso!")
    except Exception as e:
        return gera_response(400, "Usuarios", {}, f"Erro ao deletar usuario! Mensagem:{e}")

##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")
