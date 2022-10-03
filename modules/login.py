# Importações necessárias para o devido funcionamento
import datetime
import json

import jwt
from flask import Response
from config.config import app

from modules.usuarios import Usuarios

# Função para realizar o login do usuário
def login_usuario(body):
    # Criação de variável para o armazenamento dos dados informados pelo usuário
    email = body["usuario_email"]
    usuario_senha = body["usuario_senha"]

    # Variável que armazena o email filtrado pelo banco de dados
    valida_usuario = Usuarios.query.filter_by(usuario_email=email).first()

    # IF para validar se o email ou senha estão corretos e existem no banco de dados
    if not valida_usuario or not valida_usuario.verifica_senha(usuario_senha):
        return gera_response(401, "Login", email, "Usuario ou senha incorretos")

    # Criação do playload para criação do token
    # Formatando o tempo de expiração com o timedelta 
    payload = {
        "id": valida_usuario.usuario_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    # Criação do token com o jwt.encode 
    token = jwt.encode(payload, key=app.config["SECRET_KEY"], algorithm="HS256")

    return gera_response(200, "Autenticação", "Sucesso ao autenticar!", token)

##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, token = False):
    body = {}
    body[nome_conteudo] = conteudo
    if(token):
        body["token"] = token
    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")
