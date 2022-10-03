# Importações necessárias para o devido funcionamento
import json
from functools import wraps

import jwt
from flask import Response, current_app, request

from modules.usuarios import Usuarios

# Função que valida o token informado no header do endpoint
def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Criação da variável que armazena o token
        token = None

        # IF para validar se o token foi informado no header do endpoint
        if "authorization" in request.headers:
            token = request.headers["authorization"]

        # IF para exibir uma mensagem de erro 401 caso o token não seja informado
        if not token:
            return gera_response(401, "Autenticação", "Erro ao autenticar!", f"Cliente não está autenticado ou os dados de autenticação são inválidos")

        # IF para validar caso o caso o formato do token esteja inválido
        if not "Bearer " in token:
            return gera_response(401, "Autenticação", "Erro ao autenticar!", f"O formato do token é inválido")

        # Try para iniciar o tratamento do token após passar pelas validações
        try:
            token_pure = token.replace("Bearer ", "")
            decoded = jwt.decode(token_pure, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = Usuarios.query.get(decoded["id"])

        # Except para retorar uma mensagem de erro 403 caso a validação do try falhe
        except:
            return gera_response(403, "Autenticação", "Erro ao autenticar!", f"O token é inválido")

        return f(current_user=current_user, *args, **kwargs)
    return wrapper

##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo
    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")
