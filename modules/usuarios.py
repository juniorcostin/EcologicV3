from main import db, login_manager
from flask import Response
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

now = datetime.now()
@login_manager.user_loader
def usuario_logado(usuario_id):
    return Usuarios.query.filter_by(usuario_id=usuario_id).first()

#CLASS para a criação da tabela no banco e transformação dos dados em JSON
class Usuarios(db.Model, UserMixin):
    usuario_id = db.Column(db.Integer, primary_key=True)
    usuario_primeiro_nome = db.Column(db.String(100), nullable=False)
    usuario_segundo_nome = db.Column(db.String(100), nullable=False)
    usuario_email = db.Column(db.String(100), nullable=False, unique=True)
    usuario_senha = db.Column(db.String(255), nullable=False)
    grupo_id = db.Column(db.Integer, nullable=False)
    usuario_ativo = db.Column(db.Boolean, nullable=False)
    entidade_id = db.Column(db.Integer, nullable=False)
    data_criacao = db.Column(db.Date)
    hora_criacao = db.Column(db.Time)
    data_atualizacao = db.Column(db.Date)
    hora_atualizacao = db.Column(db.Time)
    usuario_criador_id = db.Column(db.Integer)
    usuario_atualizacao_id = db.Column(db.Integer)

    def __init__(self,
                 usuario_primeiro_nome,
                 usuario_segundo_nome,
                 usuario_email,
                 usuario_senha,
                 grupo_id,
                 usuario_ativo,
                 entidade_id,
                 data_criacao,
                 hora_criacao,
                 data_atualizacao,
                 hora_atualizacao,
                 usuario_criador_id,
                 usuario_atualizacao_id
                 ):
        self.usuario_primeiro_nome = usuario_primeiro_nome
        self.usuario_segundo_nome = usuario_segundo_nome
        self.usuario_email = usuario_email
        self.usuario_senha = generate_password_hash(usuario_senha)
        self.grupo_id = grupo_id
        self.usuario_ativo = usuario_ativo
        self.entidade_id = entidade_id
        self.data_criacao = data_criacao
        self.hora_criacao = hora_criacao
        self.data_atualizacao = data_atualizacao
        self.hora_atualizacao = hora_atualizacao
        self.usuario_criador_id = usuario_criador_id
        self.usuario_atualizacao_id = usuario_atualizacao_id

    def verifica_senha(self, senha):
        return check_password_hash(self.usuario_senha, senha)

    def to_json(self):
        return {"usuario_id": self.usuario_id,
                "usuario_primeiro_nome": self.usuario_primeiro_nome,
                "usuario_segundo_nome": self.usuario_segundo_nome,
                "usuario_email": self.usuario_email,
                "usuario_senha": self.usuario_senha,
                "grupo_id": self.grupo_id,
                "usuario_ativo": self.usuario_ativo,
                "entidade_id": self.entidade_id,
                "data_criacao": self.data_criacao,
                "hora_criacao": self.hora_criacao,
                "data_atualizacao": self.data_atualizacao,
                "hora_atualizacao": self.hora_atualizacao,
                "usuario_criador_id": self.usuario_criador_id,
                "usuario_atualizacao_id": self.usuario_atualizacao_id
                }

    def get_id(self):
        return (self.usuario_id)

def user_by_email(email):
    try:
        return Usuarios.query.filter(Usuarios.usuario_email == email).one()
    except:
        return None

#Endpoint GET /usuarios para listar todos os usuarios
def usuarios_seleciona_todos():
    usuarios = Usuarios.query.all()
    usuarios_json = [usuario.to_json() for usuario in usuarios]
    return gera_response(200, "Usuarios", usuarios_json, "Usuarios Listados Corretamente")

#Endpoint GET /usuarios/<id> para lista apenas um usuario
def usuarios_seleciona_um(id):
    usuarios = Usuarios.query.filter_by(usuario_id=id).first()
    usuarios_json = usuarios.to_json()
    return gera_response(200, "Usuarios", usuarios_json, "usuario Listado Corretamente")

#Endpoint POST /usuarios para incluir um novo usuario
def usuarios_criar(body):
    try:
        usuario = Usuarios(
            usuario_primeiro_nome=body["usuario_primeiro_nome"],
            usuario_segundo_nome=body["usuario_segundo_nome"],
            usuario_email=body["usuario_email"],
            usuario_senha=body["usuario_senha"],
            data_criacao=now.strftime('%Y-%m-%d'),
            hora_criacao=now.strftime('%H:%M:%S'),
            data_atualizacao=now.strftime('%Y-%m-%d'),
            hora_atualizacao=now.strftime('%H:%M:%S'),
            grupo_id=body["grupo_id"],
            usuario_ativo=body["usuario_ativo"],
            entidade_id=body["entidade_id"],
            usuario_criador_id=body["usuario_criador_id"],
            usuario_atualizacao_id=body["usuario_atualizacao_id"]
        )
        db.session.add(usuario)
        db.session.commit()
        return gera_response(201, "Usuarios", usuario.to_json(), "Usuario criado com sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "Usuarios", {}, f"Erro ao Cadastrar usuario:{e}")

#Endpoint PUT /usuarios/<id> para atualizar um usuario
def usuarios_atualiza(id, body):
    usuarios = Usuarios.query.filter_by(usuario_id=id).first()
    data_atualizacao = now.strftime('%Y-%m-%d')
    hora_atualizacao = now.strftime('%H:%M:%S')
    try:
        if "usuario_email" in body:
            usuarios.usuario_email = body["usuario_email"]
            ###### Ajustar data/hora e id usuario atualizacao
            usuarios.data_atualizacao = data_atualizacao
            usuarios.hora_atualizacao = hora_atualizacao
            usuarios.usuario_atualizacao_id = body["usuario_atualizacao_id"]
        if "usuario_senha" in body:
            usuarios.usuario_senha = body["usuario_senha"]
            ###### Ajustar data/hora e id usuario atualizacao
            usuarios.data_atualizacao = data_atualizacao
            usuarios.hora_atualizacao = hora_atualizacao
            usuarios.usuario_atualizacao_id = body["usuario_atualizacao_id"]
        if "grupo_id" in body:
            usuarios.grupo_id = body["grupo_id"]
            ###### Ajustar data/hora e id usuario atualizacao
            usuarios.data_atualizacao = data_atualizacao
            usuarios.hora_atualizacao = hora_atualizacao
            usuarios.usuario_atualizacao_id = body["usuario_atualizacao_id"]
        if "usuario_ativo" in body:
            usuarios.usuario_ativo = body["usuario_ativo"]
            ###### Ajustar data/hora e id usuario atualizacao
            usuarios.data_atualizacao = data_atualizacao
            usuarios.hora_atualizacao = hora_atualizacao
            usuarios.usuario_atualizacao_id = body["usuario_atualizacao_id"]
        if "entidade_id" in body:
            usuarios.entidade_id = body["entidade_id"]
            ###### Ajustar data/hora e id usuario atualizacao
            usuarios.data_atualizacao = data_atualizacao
            usuarios.hora_atualizacao = hora_atualizacao
            usuarios.usuario_atualizacao_id = body["usuario_atualizacao_id"]

        db.session.add(usuarios)
        db.session.commit()
        return gera_response(200, "Usuarios", usuarios.to_json(), "Usuario atualizado com sucesso")
    except Exception as e:
        return gera_response(400, "Usuarios", {}, f"Erro ao Atualizar usuario:{e}")

#Endpoint DELETE /usuarios/<id> para deletar um dispositivo
def usuarios_deleta(id):
    usuarios = Usuarios.query.filter_by(usuario_id=id).first()
    try:
        db.session.delete(usuarios)
        db.session.commit()
        return gera_response(200, "Dispositivo", usuarios.to_json(), "Usuario deletado com sucesso")
    except Exception as e:
        return gera_response(400, "Dispositivo", {}, f"Erro ao deletar Usuario:{e}")




##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")