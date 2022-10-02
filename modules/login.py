from modules.usuarios import Usuarios
from flask import Response, jsonify
from main import app
import json
import datetime
import jwt

import json

def login_usuario(body):
    email = body["usuario_email"]
    usuario_senha = body["usuario_senha"]
    valida_usuario = Usuarios.query.filter_by(usuario_email=email).first()
    if not valida_usuario or not valida_usuario.verifica_senha(usuario_senha):
        return gera_response(401, "Login", email, "Usuario ou senha incorretos")

    
    payload = {
        "id": valida_usuario.usuario_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }

    token = jwt.encode(payload, key=app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({"token": token})

##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")