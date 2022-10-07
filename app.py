# Imports nencessários para que os Endpoints funcionem corretamente
import json

from flask import Response, request

from auth.authenticate import jwt_required
from config.config import app
from modules.dispositivos import (dispositivos_atualiza, dispositivos_criar,
                                  dispositivos_deleta,
                                  dispositivos_seleciona_todos,
                                  dispositivos_seleciona_um)
from modules.entidades import (entidade_atualiza, entidade_deleta,
                               entidades_criar, entidades_seleciona_todos,
                               entidades_seleciona_um)
from modules.login import login_usuario
from modules.usuarios import (usuarios_atualiza, usuarios_criar,
                              usuarios_deleta, usuarios_seleciona_todos,
                              usuarios_seleciona_um)
from os import environ

api_endpoint_versao = "/api/v1/"

####################### LOGIN #######################
# Endpoint GET e POST para realizar o login que será salvo em cache
# Para realizar o login o usuário deve estar cadastrado no banco de dados
@app.route(f"{api_endpoint_versao}login", methods=["GET", "POST"])
def login():
    body = request.get_json()
    return login_usuario(body)

####################### DISPOSITIVOS #######################
# Endpoints responsáveis pelo gerenciamento de Dispositivos dentro do banco de dados

# Endpoint GET que lista todos os dispositivos cadastrados dentro do banco de dados
@app.route(f"{api_endpoint_versao}dispositivos", methods=["GET"])
@jwt_required
def seleciona_dispositivos(current_user):
    return dispositivos_seleciona_todos(current_user)

# Endpoint GET que lista apenas um dispositivo, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route(f"{api_endpoint_versao}dispositivos/<id>", methods=["GET"])
@jwt_required
def seleciona_dispositivo(id, current_user):
        return dispositivos_seleciona_um(id, current_user)
    
# Endpoint POST que inclui um novo dispositivo no banco de dados
# Deve ser informado um body no formato JSON com os campos corretos para que seja incluído
@app.route(f"{api_endpoint_versao}dispositivos", methods=["POST"])
@jwt_required
def cria_dispositivos(current_user):
        body = request.get_json()
        return dispositivos_criar(body, current_user)
    
# Endpoint PUT que atualiza um dispositivo, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
# Deve ser informado um body no formado JSON com os campos corretos porém opcionais para que seja atualizado
@app.route(f"{api_endpoint_versao}dispositivos/<id>", methods=["PUT"])
@jwt_required
def atualiza_dispositivo(id, current_user):
        body = request.get_json()
        return dispositivos_atualiza(id, body)

# Endpoint DELETE que deleta um dispositivo, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route(f"{api_endpoint_versao}dispositivos/<id>", methods=["DELETE"])
@jwt_required
def deleta_dispositivo(id, current_user):
        return dispositivos_deleta(id)
    
####################### ENTIDADES #######################
# Endpoints responsáveis pelo gerenciamento de Entidades dentro do banco de dados

# Endpoint GET que lista todos as entidades cadastrados dentro do banco de dados
@app.route(f"{api_endpoint_versao}entidades", methods=["GET"])
@jwt_required
def seleciona_entidades(current_user):
        return entidades_seleciona_todos()

# Endpoint GET que lista apenas uma entidade, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route(f"{api_endpoint_versao}entidades/<id>", methods=["GET"])
@jwt_required
def seleciona_entidade(id, current_user):
        return entidades_seleciona_um(id)

# Endpoint POST que inclui uma nova entidade no banco de dados
# Deve ser informado um body no formato JSON com os campos corretos para que seja incluído
@app.route(f"{api_endpoint_versao}entidades", methods=["POST"])
@jwt_required
def cria_entidade(current_user):
        body = request.get_json()
        return entidades_criar(body)

# Endpoint PUT que atualiza uma entidade, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
# Deve ser informado um body no formado JSON com os campos corretos porém opcionais para que seja atualizado
@app.route(f"{api_endpoint_versao}entidades/<id>", methods=["PUT"])
@jwt_required
def atualiza_entidade(id, current_user):
        body = request.get_json()
        return entidade_atualiza(id, body)
    
# Endpoint DELETE que deleta uma entidade, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route(f"{api_endpoint_versao}entidades/<id>", methods=["DELETE"])
@jwt_required
def deleta_entidade(id, current_user):    
        return entidade_deleta(id)

####################### USUARIOS #######################
# Endpoints responsáveis pelo gerenciamento de Usuários dentro do banco de dados

# Endpoint GET que lista todos os usuários cadastrados dentro do banco de dados
@app.route(f"{api_endpoint_versao}usuarios", methods=["GET"])
@jwt_required
def seleciona_usuarios(current_user):
        return usuarios_seleciona_todos(current_user)
    
# Endpoint GET que lista apenas um usuario, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route(f"{api_endpoint_versao}usuarios/<id>", methods=["GET"])
@jwt_required
def seleciona_usuario(id, current_user):
        return usuarios_seleciona_um(id, current_user)
    
# Endpoint POST que inclui um novo usuario no banco de dados
# Deve ser informado um body no formato JSON com os campos corretos para que seja incluído
@app.route(f"{api_endpoint_versao}usuarios", methods=["POST"])
# Habilitar a obrigatoriedade de login para a criação de usuários
@jwt_required
def cria_usuarios(current_user):
        body = request.get_json()
        return usuarios_criar(body, current_user)

# Endpoint PUT que atualiza um usuario, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
# Deve ser informado um body no formado JSON com os campos corretos porém opcionais para que seja atualizado
@app.route(f"{api_endpoint_versao}usuarios/<id>", methods=["PUT"])
@jwt_required
def atualiza_usuarios(id, current_user):
        body = request.get_json()
        return usuarios_atualiza(id, body, current_user)

# Endpoint DELETE que deleta um usuario, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route(f"{api_endpoint_versao}usuarios/<id>", methods=["DELETE"])
@jwt_required
def deleta_usuarios(id, current_user):
        return usuarios_deleta(id, current_user)

##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo
    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")

#Inicializador Flask
app.run(host="localhost",port=5000, debug=(not environ.get('ENV') == 'PRODUCTION'),threaded=True)

