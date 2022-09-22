from flask import request, Response
from flask_login import current_user
import json
from main import app
from modules.login import login_usuario
from modules.dispositivos import dispositivos_seleciona_todos, dispositivos_seleciona_um, dispositivos_criar, dispositivos_atualiza, dispositivos_deleta
from modules.entidades import entidades_seleciona_todos, entidades_seleciona_um, entidades_criar, entidade_atualiza, entidade_deleta
from modules.usuarios import usuarios_seleciona_todos, usuarios_seleciona_um, usuarios_criar, usuarios_atualiza, usuarios_deleta

####################### LOGIN ############################
@app.route("/login", methods=["GET", "POST"])
def login():
    body = request.get_json()
    return login_usuario(body)

####################### DISPOSITIVOS ############################
#Endpoint GET /dispositivos para listar todos os Dispositivos
@app.route("/dispositivos", methods=["GET"])
def seleciona_dispositivos():
    if current_user.is_authenticated:
        return dispositivos_seleciona_todos()
    return gera_response(401, "Dispositivos", "Autenticação", "Você precisa estar autenticado para realizar essa consulta")

#Endpoint GET /dispositivos/<id> para lista apenas um Dispositivo
@app.route("/dispositivos/<id>", methods=["GET"])
def seleciona_dispositivo(id):
    if current_user.is_authenticated:
        return dispositivos_seleciona_um(id)
    return gera_response(401, "Dispositivos", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

#Endpoint POST /dispositivos para incluir um novo dispositivo
@app.route("/dispositivos", methods=["POST"])
def cria_dispositivos():
    if current_user.is_authenticated:
        body = request.get_json()
        return dispositivos_criar(body)
    return gera_response(401, "Dispositivos", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

#Endpoint PUT /dispositivos/<id> para atualizar um Dispositivo
@app.route("/dispositivos/<id>", methods=["PUT"])
def atualiza_dispositivo(id):
    if current_user.is_authenticated:
        body = request.get_json()
        return dispositivos_atualiza(id, body)
    return gera_response(401, "Dispositivos", "Autenticação", "Você precisa estar autenticado para realizar essa consulta")

#Endpoint DELETE /dispositivos/<id> para deletar um dispositivo
@app.route("/dispositivos/<id>", methods=["DELETE"])
def deleta_dispositivo(id):
    if current_user.is_authenticated:
        return dispositivos_deleta(id)
    return gera_response(401, "Dispositivos", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

####################### ENTIDADES ############################

#Endpoint GET /entidades para listar todos as Entidades
@app.route("/entidades", methods=["GET"])
def seleciona_entidades():
    if current_user.is_authenticated:
        return entidades_seleciona_todos()
    return gera_response(401, "Entidades", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

#Endpoint GET /dispositivos/<id> para lista apenas uma entidade
@app.route("/entidades/<id>", methods=["GET"])
def seleciona_entidade(id):
    if current_user.is_authenticated:
        return entidades_seleciona_um(id)
    return gera_response(401, "Entidades", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

#Endpoint POST /entidades para incluir uma nova entidade
@app.route("/entidades", methods=["POST"])
def cria_entidade():
    if current_user.is_authenticated:
        body = request.get_json()
        return entidades_criar(body)
    return gera_response(401, "Entidades", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

#Endpoint PUT /entidades/<id> para atualizar uma entidade
@app.route("/entidades/<id>", methods=["PUT"])
def atualiza_entidade(id):
    if current_user.is_authenticated:
        body = request.get_json()
        return entidade_atualiza(id, body)
    return gera_response(401, "Entidades", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

#Endpoint DELETE /entidades/<id> para deletar uma entidade
@app.route("/entidades/<id>", methods=["DELETE"])
def deleta_entidade(id):
    if current_user.is_authenticated:
        return entidade_deleta(id)
    return gera_response(401, "Entidades", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

####################### USUARIOS ############################
#Endpoint GET /usuarios para listar todos os Dispositivos
@app.route("/usuarios", methods=["GET"])
def seleciona_usuarios():
    if current_user.is_authenticated:
        return usuarios_seleciona_todos()
    return gera_response(401, "Usuarios", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

#Endpoint GET /usuarios/<id> para lista apenas um Dispositivo
@app.route("/usuarios/<id>", methods=["GET"])
def seleciona_usuario(id):
    if current_user.is_authenticated:
        return usuarios_seleciona_um(id)
    return gera_response(401, "Usuarios", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")
#Endpoint POST /usuarios para incluir um novo dispositivo
@app.route("/usuarios", methods=["POST"])
def cria_usuarios():
    if current_user.is_authenticated:
        body = request.get_json()
        return usuarios_criar(body)
    return gera_response(401, "Usuarios", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

#Endpoint PUT /usuarios/<id> para atualizar um Dispositivo
@app.route("/usuarios/<id>", methods=["PUT"])
def atualiza_usuarios(id):
    if current_user.is_authenticated:
        body = request.get_json()
        return usuarios_atualiza(id, body)
    return gera_response(401, "Usuarios", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

#Endpoint DELETE /usuarios/<id> para deletar um dispositivo
@app.route("/usuarios/<id>", methods=["DELETE"])
def deleta_usuarios(id):
    if current_user.is_authenticated:
        return usuarios_deleta(id)
    return gera_response(401, "Usuarios", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")


##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo
    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")


#Inicializador Flask
app.run()

