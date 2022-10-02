# Imports nencessários para que os Endpoints funcionem corretamente
from flask import request, Response
from flask_login import current_user
from authenticate import jwt_required
import json
from main import app
from modules.login import login_usuario
from modules.dispositivos import dispositivos_seleciona_todos, dispositivos_seleciona_um, dispositivos_criar, dispositivos_atualiza, dispositivos_deleta
from modules.entidades import entidades_seleciona_todos, entidades_seleciona_um, entidades_criar, entidade_atualiza, entidade_deleta
from modules.usuarios import usuarios_seleciona_todos, usuarios_seleciona_um, usuarios_criar, usuarios_atualiza, usuarios_deleta

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
    # IF que analisa se o usuário está autenticado ou não
    return dispositivos_seleciona_todos()

# Endpoint GET que lista apenas um dispositivo, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route("/dispositivos/<id>", methods=["GET"])
def seleciona_dispositivo(id):
    # IF que analisa se o usuário está autenticado ou não
    if current_user.is_authenticated:
        return dispositivos_seleciona_um(id)
    return gera_response(401, "Dispositivos", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

# Endpoint POST que inclui um novo dispositivo no banco de dados
# Deve ser informado um body no formato JSON com os campos corretos para que seja incluído
@app.route("/dispositivos", methods=["POST"])
def cria_dispositivos():
    # IF que analisa se o usuário está autenticado ou não
    if current_user.is_authenticated:
        body = request.get_json()
        return dispositivos_criar(body)
    return gera_response(401, "Dispositivos", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

# Endpoint PUT que atualiza um dispositivo, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
# Deve ser informado um body no formado JSON com os campos corretos porém opcionais para que seja atualizado
@app.route("/dispositivos/<id>", methods=["PUT"])
def atualiza_dispositivo(id):
    # IF que analisa se o usuário está autenticado ou não
    if current_user.is_authenticated:
        body = request.get_json()
        return dispositivos_atualiza(id, body)
    return gera_response(401, "Dispositivos", "Autenticação", "Você precisa estar autenticado para realizar essa consulta")

# Endpoint DELETE que deleta um dispositivo, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route("/dispositivos/<id>", methods=["DELETE"])
def deleta_dispositivo(id):
    # IF que analisa se o usuário está autenticado ou não
    if current_user.is_authenticated:
        return dispositivos_deleta(id)
    return gera_response(401, "Dispositivos", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

####################### ENTIDADES #######################
# Endpoints responsáveis pelo gerenciamento de Entidades dentro do banco de dados

# Endpoint GET que lista todos as entidades cadastrados dentro do banco de dados
@app.route("/entidades", methods=["GET"])
def seleciona_entidades():
    # IF que analisa se o usuário está autenticado ou não
    if current_user.is_authenticated:
        return entidades_seleciona_todos()
    return gera_response(401, "Entidades", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

# Endpoint GET que lista apenas uma entidade, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route("/entidades/<id>", methods=["GET"])
def seleciona_entidade(id):
    # IF que analisa se o usuário está autenticado ou não
    if current_user.is_authenticated:
        return entidades_seleciona_um(id)
    return gera_response(401, "Entidades", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

# Endpoint POST que inclui uma nova entidade no banco de dados
# Deve ser informado um body no formato JSON com os campos corretos para que seja incluído
@app.route("/entidades", methods=["POST"])
def cria_entidade():
    # IF que analisa se o usuário está autenticado ou não
    if current_user.is_authenticated:
        body = request.get_json()
        return entidades_criar(body)
    return gera_response(401, "Entidades", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

# Endpoint PUT que atualiza uma entidade, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
# Deve ser informado um body no formado JSON com os campos corretos porém opcionais para que seja atualizado
@app.route("/entidades/<id>", methods=["PUT"])
def atualiza_entidade(id):
    # IF que analisa se o usuário está autenticado ou não
    if current_user.is_authenticated:
        body = request.get_json()
        return entidade_atualiza(id, body)
    return gera_response(401, "Entidades", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

# Endpoint DELETE que deleta uma entidade, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route("/entidades/<id>", methods=["DELETE"])
def deleta_entidade(id):
    # IF que analisa se o usuário está autenticado ou não
    if current_user.is_authenticated:
        return entidade_deleta(id)
    return gera_response(401, "Entidades", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

####################### USUARIOS #######################
# Endpoints responsáveis pelo gerenciamento de Usuários dentro do banco de dados

# Endpoint GET que lista todos os usuários cadastrados dentro do banco de dados
@app.route("/usuarios", methods=["GET"])
def seleciona_usuarios():
    # IF que analisa se o usuário está autenticado ou não
    if current_user.is_authenticated:
        return usuarios_seleciona_todos()
    return gera_response(401, "Usuarios", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

# Endpoint GET que lista apenas um usuario, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route("/usuarios/<id>", methods=["GET"])
def seleciona_usuario(id):
    # IF que analisa se o usuário está autenticado ou não
    if current_user.is_authenticated:
        return usuarios_seleciona_um(id)
    return gera_response(401, "Usuarios", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

# Endpoint POST que inclui um novo usuario no banco de dados
# Deve ser informado um body no formato JSON com os campos corretos para que seja incluído
@app.route("/usuarios", methods=["POST"])
def cria_usuarios():
    # IF que analisa se o usuário está autenticado ou não
    if current_user.is_authenticated:
        body = request.get_json()
        return usuarios_criar(body)
    return gera_response(401, "Usuarios", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

# Endpoint PUT que atualiza um usuario, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
# Deve ser informado um body no formado JSON com os campos corretos porém opcionais para que seja atualizado
@app.route("/usuarios/<id>", methods=["PUT"])
def atualiza_usuarios(id):
    # IF que analisa se o usuário está autenticado ou não
    if current_user.is_authenticated:
        body = request.get_json()
        return usuarios_atualiza(id, body)
    return gera_response(401, "Usuarios", "Autenticação",
                         "Você precisa estar autenticado para realizar essa consulta")

# Endpoint DELETE que deleta um usuario, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
@app.route("/usuarios/<id>", methods=["DELETE"])
def deleta_usuarios(id):
    # IF que analisa se o usuário está autenticado ou não
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

