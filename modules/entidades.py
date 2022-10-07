# Imports nencessários para que os Endpoints funcionem corretamente
import json
from datetime import datetime
from types import CellType

from admin.admin import tabela_entidades
from config.config import admin, db
from flask import Response

from modules.usuarios import Usuarios


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
class Entidades(db.Model):
    entidade_id = db.Column(db.Integer, primary_key = True)
    entidade_razaosocial = db.Column(db.String(40), nullable=False)
    entidade_ramo = db.Column(db.String(40), nullable=False)
    dispositivos_quantidade = db.Column(db.Integer, nullable=False)
    cpfcnpj = db.Column(db.String(40), nullable=False)
    data_criacao = db.Column(db.Date, nullable=False)
    data_atualizacao = db.Column(db.Date, nullable=False)
    usuario_criador_id = db.Column(db.Integer, nullable=False)
    entidade_ativa = db.Column(db.Boolean, nullable=False)
    usuario_atualizacao_id = db.Column(db.Integer, nullable=False)
    hora_atualizacao = db.Column(db.Time, nullable=False)
    hora_criacao = db.Column(db.Time, nullable=False)
    entidade_nome = db.Column(db.String(40), nullable=False)
    longitude = db.Column(db.String(50))
    latitude = db.Column(db.String(50))
    cep = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)


    def to_json(self):
        return {"entidade_id": self.entidade_id,
                "entidade_razaosocial": self.entidade_razaosocial,
                "entidade_ramo": self.entidade_ramo,
                "dispositivos_quantidade": self.dispositivos_quantidade,
                "cpfcnpj": self.cpfcnpj,
                "data_criacao": self.data_criacao,
                "data_atualizacao": self.data_atualizacao,
                "usuario_criador_id": self.usuario_criador_id,
                "entidade_ativa": self.entidade_ativa,
                "usuario_atualizacao_id": self.usuario_atualizacao_id,
                "hora_atualizacao": self.hora_atualizacao,
                "hora_criacao": self.hora_criacao,
                "entidade_nome": self.entidade_nome,
                "longitude": self.longitude,
                "latitude": self.latitude,
                "cep": self.cep,
                "estado": self.estado,
                "cidade": self.cidade
                }

# Paramentro para criar a tabela dentro da interface Admin do sistema
admin.add_view(tabela_entidades(Entidades, db.session))

# Endpoint GET que lista todos as entidades cadastrados dentro do banco de dados
def entidades_seleciona_todos(current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_entidade_id = current_user.entidade_id
        login_admin = current_user.admin
        login_visualizar = current_user.visualizar

     # If para validar se o usuário tem as permissões
        if login_admin == True or login_visualizar == True:
            entidades = Entidades.query.filter_by(entidade_id = login_entidade_id)
            entidades_json = [entidade.to_json() for entidade in entidades]
            return gera_response(200, "Entidades", entidades_json, "Entidades listados com sucesso!")
        else:
            return gera_response(403, "Entidades", {}, "Você não tem permissão para listar as entidades!")
    except Exception as e:
        return gera_response(400, "Entidades", {}, f"Falha ao listar entidades! Mensagem: {e}")

# Endpoint GET que lista apenas uma entidade, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
def entidades_seleciona_um(id, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_entidade_id = current_user.entidade_id
        login_admin = current_user.admin
        login_visualizar = current_user.visualizar

        # IF para validar se o ID informado está cadastrado no banco de dados
        if not Entidades.query.filter_by(entidade_id=id).first():
            return gera_response(400, "Entidades", {}, f"Falha ao listar entidade! Mensagem: A entidade ID:{id} não existe!")

        # IF para validar se a entidade informado é da mesma entidade que o usuário logado
        valida_entidade = Entidades.query.filter_by(entidade_id=id).first()
        if valida_entidade.to_json()["entidade_id"] != login_entidade_id:
            return gera_response(403, "Entidades", {}, "Você não tem permissão para listar a entidade!")

        # If para validar se o usuário tem as permissões
        if login_admin == True or login_visualizar == True:
            entidades = Entidades.query.filter_by(entidade_id = login_entidade_id).first()
            entidades_json = entidades.to_json()
            return gera_response(200, "Entidades", entidades_json, "Entidade listado com sucesso!")
        else:
            return gera_response(403, "Entidades", {}, "Você não tem permissão para listar a entidade!")
    except Exception as e:
        return gera_response(400, "Entidades", {}, f"Falha ao listar entidade! Mensagem: {e}")

# Endpoint POST que é responsável por realizar a criação de um novo dispositivo dentro do banco de dados
# Deve ser informado o body da requisição com as informações corretas para a criação
def entidades_criar(body, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_usuario_id = current_user.usuario_id
        login_admin = current_user.admin
        login_cadastrar = current_user.cadastrar

        # IF que valida se o usuário tem as permissões necessárias para realizar a criação
        if login_admin == True or login_cadastrar == True:
            entidade = Entidades(
                entidade_razaosocial=body["entidade_razaosocial"],
                entidade_ramo=body["entidade_ramo"],
                dispositivos_quantidade=body["dispositivos_quantidade"],
                cpfcnpj=body["cpfcnpj"],
                data_criacao=data(),
                hora_criacao=hora(),
                data_atualizacao=data(),
                hora_atualizacao=hora(),
                usuario_criador_id=login_usuario_id,
                entidade_ativa=body["entidade_ativa"],
                usuario_atualizacao_id=0,
                entidade_nome=body["entidade_nome"],
                longitude=body["longitude"],
                latitude=body["latitude"],
                cep=body["cep"],
                cidade=body["cidade"],
                estado=body["estado"]
            )
            db.session.add(entidade)
            db.session.commit()
            return gera_response(201, "Entidades", entidade.to_json(), "Entidade criada com sucesso!")
        else:
            return gera_response(403, "Entidades", {}, "Você não tem permissão para cadastrar a entidade!")
    except Exception as e:
        print(e)
        return gera_response(400, "Entidades", {}, f"Falha ao cadastrar entidade! Mensagem:{e}")

# Endpoint PUT responsável pela atualização de uma entidade
# Deve ser informado o ID da entidade existente no banco de dados
# O body da requisição não necessáriamente precisa conter todos os campos
def entidade_atualiza(id, body, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_usuario_id = current_user.usuario_id
        login_entidade_id = current_user.entidade_id
        login_admin = current_user.admin
        login_editar = current_user.editar

        # IF para validar se o ID informado está cadastrado no banco de dados
        if not Entidades.query.filter_by(entidade_id=id).first():
            return gera_response(400, "Entidades", {}, f"Falha ao atualizar entidade! Mensagem: A entidade ID:{id} não existe!") 

        entidades = Entidades.query.filter_by(entidade_id=id).first()
        entidade_json = entidades.to_json()
        
        # IF para validar se a entidade do usuário logado é igual ao do usuário informado
        if entidade_json["entidade_id"] != login_entidade_id:
            return gera_response(403, "Entidades", {}, "Você não pertence a essa entidade!")
        # IF para validar se o usuário tem as permissões nencessárias para editar o usuário
        if login_admin == True or login_editar == True:
            if "entidade_razaosocial" in body:
                entidades.entidade_razaosocial = body["entidade_razaosocial"]
                entidades.data_atualizacao = data()
                entidades.hora_atualizacao = hora()
                entidades.usuario_atualizacao_id = login_usuario_id
            if "entidade_ramo" in body:
                entidades.entidade_ramo = body["entidade_ramo"]
                entidades.data_atualizacao = data()
                entidades.hora_atualizacao = hora()
                entidades.usuario_atualizacao_id = login_usuario_id
            if "dispositivos_quantidade" in body:
                entidades.dispositivos_quantidade = body["dispositivos_quantidade"]
                entidades.data_atualizacao = data()
                entidades.hora_atualizacao = hora()
                entidades.usuario_atualizacao_id = login_usuario_id
            if "entidade_ativa" in body:
                entidades.entidade_ativa = body["entidade_ativa"]
                entidades.data_atualizacao = data()
                entidades.hora_atualizacao = hora()
                entidades.usuario_atualizacao_id = login_usuario_id
            if "entidade_nome" in body:
                entidades.entidade_nome = body["entidade_nome"]
                entidades.data_atualizacao = data()
                entidades.hora_atualizacao = hora()
                entidades.usuario_atualizacao_id = login_usuario_id
            if "longitude" in body:
                entidades.longitude = body["longitude"]
                entidades.data_atualizacao = data()
                entidades.hora_atualizacao = hora()
                entidades.usuario_atualizacao_id = login_usuario_id
            if "latitude" in body:
                entidades.latitude = body["latitude"]
                entidades.data_atualizacao = data()
                entidades.hora_atualizacao = hora()
                entidades.usuario_atualizacao_id = login_usuario_id
            if "cep" in body:
                entidades.cep = body["cep"]
                entidades.data_atualizacao = data()
                entidades.hora_atualizacao = hora()
                entidades.usuario_atualizacao_id = login_usuario_id
            if "cidade" in body:
                entidades.cidade = body["cidade"]
                entidades.data_atualizacao = data()
                entidades.hora_atualizacao = hora()
                entidades.usuario_atualizacao_id = login_usuario_id
            if "estado" in body:
                entidades.estado = body["estado"]
                entidades.data_atualizacao = data()
                entidades.hora_atualizacao = hora()
                entidades.usuario_atualizacao_id = login_usuario_id

            db.session.add(entidades)
            db.session.commit()
            return gera_response(200, "Entidades", entidades.to_json(), "Entidade atualizada com sucesso")

        else:
            return gera_response(403, "Entidades", {}, "Você não tem permissão para atualizar a entidade!")

    except Exception as e:
        return gera_response(400, "Entidades", {}, f"Erro ao Atualizar Entidade:{e}")

# Endpoint DELETE responsável por deletar uma entidade
# Deve ser informado o ID da entidade 
def entidade_deleta(id, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_entidade_id = current_user.entidade_id
        login_admin = current_user.admin
        login_deletar = current_user.deletar

        # IF para validar se o ID informado está cadastrado no banco de dados
        if not Entidades.query.filter_by(entidade_id=id).first():
            return gera_response(400, "Entidades", {}, f"Falha ao deletar entidade! Mensagem: A entidade ID:{id} não existe!")

        entidade = Entidades.query.filter_by(entidade_id=id).first()
        entidade_json = entidade.to_json()
        
        # IF para validar se a entidade do usuário logado é igual ao do usuário informado
        if entidade_json["entidade_id"] != login_entidade_id:
            return gera_response(403, "Entidades", {}, "Você não tem permissão para deletar a entidade!")

        # IF para validar se existem usuários vinculados a essa entidade
        if Usuarios.query.filter_by(entidade_id=id).first():
            return gera_response(403, "Entidades", {}, "Existem usuários vinculados a essa entidade!")

        # IF para validar se o usuário tem a permissão necessária para deletar o usuário
        if login_admin == True or login_deletar == True:
            db.session.delete(entidade)
            db.session.commit()
            return gera_response(200, "Entidades", entidade.to_json(), "Entidade deletado com sucesso!")
    except Exception as e:
        return gera_response(400, "Entidades", {}, f"Erro ao deletar entidade! Mensagem:{e}")


##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo
    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")
