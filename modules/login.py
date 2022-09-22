from modules.usuarios import Usuarios
from flask import Response
from flask_login import login_user
import json

def login_usuario(body):
    email = body["usuario_email"]
    usuario_senha = body["usuario_senha"]
    valida_usuario = Usuarios.query.filter_by(usuario_email=email).first()
    if not valida_usuario or not valida_usuario.verifica_senha(usuario_senha):
        return gera_response(401, "Login", email, "Usuario ou senha incorretos")
    login_user(valida_usuario)
    return "usuario logado"

##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")