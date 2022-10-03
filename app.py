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


####################### LOGIN #######################
# Endpoint GET e POST para realizar o login que será salvo em cache
# Para realizar o login o usuário deve estar cadastrado no banco de dados
@app.route("/login", methods=["GET", "POST"])
def login():
    body = request.get_json()
    return login_usuario(body)

####################### DISPOSITIVOS #######################
# Endpoints responsáveis pelo gerenciamento de Dispositivos dentro do banco de dados

# Endpoint GET que lista todos os dispositivos cadastrados dentro do banco de dados
@app.route("/dispositivos", methods=["GET"])
@jwt_required
def seleciona_dispositivos(current_user):
    return dispositivos_seleciona_todos()

# Endpoint GET que lista apenas um dispositivo, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route("/dispositivos/<id>", methods=["GET"])
@jwt_required
def seleciona_dispositivo(id, current_user):
        return dispositivos_seleciona_um(id)
    
# Endpoint POST que inclui um novo dispositivo no banco de dados
# Deve ser informado um body no formato JSON com os campos corretos para que seja incluído
@app.route("/dispositivos", methods=["POST"])
@jwt_required
def cria_dispositivos(current_user):
        body = request.get_json()
        return dispositivos_criar(body)
    
# Endpoint PUT que atualiza um dispositivo, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
# Deve ser informado um body no formado JSON com os campos corretos porém opcionais para que seja atualizado
@app.route("/dispositivos/<id>", methods=["PUT"])
@jwt_required
def atualiza_dispositivo(id, current_user):
        body = request.get_json()
        return dispositivos_atualiza(id, body)

# Endpoint DELETE que deleta um dispositivo, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route("/dispositivos/<id>", methods=["DELETE"])
@jwt_required
def deleta_dispositivo(id, current_user):
        return dispositivos_deleta(id)
    
####################### ENTIDADES #######################
# Endpoints responsáveis pelo gerenciamento de Entidades dentro do banco de dados

# Endpoint GET que lista todos as entidades cadastrados dentro do banco de dados
@app.route("/entidades", methods=["GET"])
@jwt_required
def seleciona_entidades(current_user):
        return entidades_seleciona_todos()

# Endpoint GET que lista apenas uma entidade, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route("/entidades/<id>", methods=["GET"])
@jwt_required
def seleciona_entidade(id, current_user):
        return entidades_seleciona_um(id)

# Endpoint POST que inclui uma nova entidade no banco de dados
# Deve ser informado um body no formato JSON com os campos corretos para que seja incluído
@app.route("/entidades", methods=["POST"])
@jwt_required
def cria_entidade(current_user):
        body = request.get_json()
        return entidades_criar(body)

# Endpoint PUT que atualiza uma entidade, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
# Deve ser informado um body no formado JSON com os campos corretos porém opcionais para que seja atualizado
@app.route("/entidades/<id>", methods=["PUT"])
@jwt_required
def atualiza_entidade(id, current_user):
        body = request.get_json()
        return entidade_atualiza(id, body)
    
# Endpoint DELETE que deleta uma entidade, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route("/entidades/<id>", methods=["DELETE"])
@jwt_required
def deleta_entidade(id, current_user):    
        return entidade_deleta(id)

####################### USUARIOS #######################
# Endpoints responsáveis pelo gerenciamento de Usuários dentro do banco de dados

# Endpoint GET que lista todos os usuários cadastrados dentro do banco de dados
@app.route("/usuarios", methods=["GET"])
@jwt_required
def seleciona_usuarios(current_user):
        return usuarios_seleciona_todos()
    
# Endpoint GET que lista apenas um usuario, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route("/usuarios/<id>", methods=["GET"])
@jwt_required
def seleciona_usuario(id, current_user):
        return usuarios_seleciona_um(id)
    
# Endpoint POST que inclui um novo usuario no banco de dados
# Deve ser informado um body no formato JSON com os campos corretos para que seja incluído
@app.route("/usuarios", methods=["POST"])
@jwt_required
def cria_usuarios(current_user):
        body = request.get_json()
        return usuarios_criar(body)

# Endpoint PUT que atualiza um usuario, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
# Deve ser informado um body no formado JSON com os campos corretos porém opcionais para que seja atualizado
@app.route("/usuarios/<id>", methods=["PUT"])
@jwt_required
def atualiza_usuarios(id, current_user):
        body = request.get_json()
        return usuarios_atualiza(id, body)

# Endpoint DELETE que deleta um usuario, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route("/usuarios/<id>", methods=["DELETE"])
@jwt_required
def deleta_usuarios(id, current_user):
        return usuarios_deleta(id)

##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo
    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")

#Inicializador Flask
app.run()

