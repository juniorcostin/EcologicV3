# Imports nencessários para que os Endpoints funcionem corretamente
import json
from datetime import datetime
from itertools import count

from admin.admin import tabela_dispositivos
from config.config import admin, db
from flask import Response

from modules.entidades import Entidades


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
class Dispositivos(db.Model):
    dispositivo_id = db.Column(db.Integer, primary_key = True)
    dispositivo_nome = db.Column(db.String(40), nullable=False)
    dispositivo_tipo = db.Column(db.String(40), nullable=False)
    dispositivo_ativo = db.Column(db.Boolean, nullable=False)
    dispositivo_descricao = db.Column(db.String(200), nullable=False)
    data_criacao = db.Column(db.Date, nullable=False)
    hora_criacao = db.Column(db.Time, nullable=False)
    data_atualizacao = db.Column(db.Date, nullable=False)
    hora_atualizacao = db.Column(db.Time, nullable=False)
    usuario_criador_id = db.Column(db.Integer, nullable=False)
    entidade_id = db.Column(db.Integer, nullable=False)
    usuario_atualizacao_id = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.String(50))
    longitude = db.Column(db.String(50))

    def to_json(self):
        return {"dispositivo_id": self.dispositivo_id,
                "dispositivo_nome": self.dispositivo_nome,
                "dispositivo_tipo": self.dispositivo_tipo,
                "dispositivo_ativo": self.dispositivo_ativo,
                "dispositivo_descricao": self.dispositivo_descricao,
                "data_criacao": self.data_criacao,
                "hora_criacao": self.hora_criacao,
                "data_atualizacao": self.data_atualizacao,
                "hora_atualizacao": self.hora_atualizacao,
                "usuario_criador_id": self.usuario_criador_id,
                "entidade_id": self.entidade_id,
                "usuario_atualizacao_id": self.usuario_atualizacao_id,
                "latitude": self.latitude,
                "longitude": self.longitude
                }

# Paramentro para criar a tabela dentro da interface Admin do sistema
admin.add_view(tabela_dispositivos(Dispositivos, db.session))

# Endpoint GET que lista todos os dispositivos cadastrados dentro do banco de dados
def dispositivos_seleciona_todos(current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_entidade_id = current_user.entidade_id
        login_admin = current_user.admin
        login_visualizar = current_user.visualizar

        # If para validar se o usuário tem as permissões
        if login_admin == True or login_visualizar == True:
            dispositivos = Dispositivos.query.filter_by(entidade_id = login_entidade_id)
            dispositivos_json = [dispositivo.to_json() for dispositivo in dispositivos]
            return gera_response(200, "Dispositivos", dispositivos_json, "Dispositivos listados com sucesso!")
        else:
            return gera_response(403, "Usuarios", {}, "Você não tem permissão para listar os dispositivos!")
    except Exception as e:
        return gera_response(400, "Dispositivos", {}, f"Falha ao listar dispositivos! Mensagem: {e}")

# Endpoint GET que lista apenas um dispositivo, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
def dispositivos_seleciona_um(id, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_entidade_id = current_user.entidade_id
        login_admin = current_user.admin
        login_visualizar = current_user.visualizar

        # IF para validar se o ID informado está cadastrado no banco de dados
        if not Dispositivos.query.filter_by(dispositivo_id=id).first():
            return gera_response(400, "Dispositivos", {}, f"Falha ao listar usuario! Mensagem: O dispositivo ID:{id} não existe!")

        # IF para validar se o dispositivo informado é da mesma entidade que o usuário logado
        valida_entidade = Dispositivos.query.filter_by(dispositivo_id=id).first()
        if valida_entidade.to_json()["entidade_id"] != login_entidade_id:
            return gera_response(403, "Dispositivos", {}, "Você não tem permissão para listar o dispositivo!")

        # If para validar se o usuário tem as permissões
        if login_admin == True or login_visualizar == True:
            dispositivos = Dispositivos.query.filter_by(dispositivo_id=id, entidade_id = login_entidade_id).first()
            dispositivos_json = dispositivos.to_json()
            return gera_response(200, "Dispositivos", dispositivos_json, "Dispositivo listado com sucesso!")
        else:
            return gera_response(403, "Dispositivos", {}, "Você não tem permissão para listar o dispositivo!")
    except Exception as e:
        return gera_response(400, "Dispositivos", {}, f"Falha ao listar dispositivo! Mensagem: {e}")

# Endpoint POST que é responsável por realizar a criação de um novo dispositivo dentro do banco de dados
# Deve ser informado o body da requisição com as informações corretas para a criação
def dispositivos_criar(body, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_usuario_id = current_user.usuario_id
        login_entidade_id = current_user.entidade_id
        login_admin = current_user.admin
        login_cadastrar = current_user.cadastrar
        quantidade_permitida = Entidades.query.filter_by(entidade_id=login_entidade_id).first()
        quantidade_permitida = quantidade_permitida.to_json()

        # IF para validar quantos dispositivos a entidade permite
        if Dispositivos.query.filter_by(entidade_id=login_entidade_id).count() >= quantidade_permitida["dispositivos_quantidade"]:
            return gera_response(400, "Dispositivos", {}, f"Falha ao cadastrar dispositivo! Mensagem: A entidade atingiu o limite máximo de dispostivios cadastrados")

        # IF que valida se o usuário tem as permissões necessárias para realizar a criação
        if login_admin == True or login_cadastrar == True:
            dispositivo = Dispositivos(
                dispositivo_nome=body["dispositivo_nome"],
                dispositivo_tipo=body["dispositivo_tipo"],
                dispositivo_ativo=body["dispositivo_ativo"],
                dispositivo_descricao=body["dispositivo_descricao"],
                data_criacao=data(),
                hora_criacao=hora(),
                data_atualizacao=data(),
                hora_atualizacao=hora(),
                usuario_criador_id=login_usuario_id,
                entidade_id=login_entidade_id,
                usuario_atualizacao_id=0,
                latitude=body["latitude"],
                longitude=body["longitude"]
            )
            db.session.add(dispositivo)
            db.session.commit()
            return gera_response(201, "Dispositivos", dispositivo.to_json(), "Dispositivo criado com sucesso!")
        else:
            return gera_response(403, "Dispositivos", {}, "Você não tem permissão para cadastrar o dispositivo!")
    except Exception as e:
        return gera_response(400, "Dispositivos", {}, f"Falha ao cadastrar dispositivo! Mensagem:{e}")

# Endpoint PUT responsável pela atualização de um dispositivo
# Deve ser informado o ID do dispositivo existente no banco de dados
# O body da requisição não necessáriamente precisa conter todos os campos
def dispositivos_atualiza(id, body, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_usuario_id = current_user.usuario_id
        login_entidade_id = current_user.entidade_id
        login_admin = current_user.admin
        login_editar = current_user.editar

        # IF para validar se o ID informado está cadastrado no banco de dados
        if not Dispositivos.query.filter_by(dispositivo_id=id).first():
            return gera_response(400, "Dispositivos", {}, f"Falha ao atualizar dispositivo! Mensagem: O dispositivo ID:{id} não existe!") 

        dispositivos = Dispositivos.query.filter_by(dispositivo_id=id).first()
        dispositivo_json = dispositivos.to_json()
        
        # IF para validar se a entidade do usuário logado é igual ao do usuário informado
        if dispositivo_json["entidade_id"] != login_entidade_id:
            return gera_response(403, "Dispositivos", {}, "Você não pertence a entidade deste dispositivo!")

        # IF para validar se o usuário tem as permissões nencessárias para editar o usuário
        if login_admin == True or login_editar == True:
            if "dispositivo_nome" in body:
                dispositivos.dispositivo_nome = body["dispositivo_nome"]
                dispositivos.data_atualizacao = data()
                dispositivos.hora_atualizacao = hora()
                dispositivos.usuario_atualizacao_id = login_usuario_id
            if "dispositivo_tipo" in body:
                dispositivos.dispositivo_tipo = body["dispositivo_tipo"]
                dispositivos.data_atualizacao = data()
                dispositivos.hora_atualizacao = hora()
                dispositivos.usuario_atualizacao_id = login_usuario_id
            if "dispositivo_ativo" in body:
                dispositivos.dispositivo_ativo = body["dispositivo_ativo"]
                dispositivos.data_atualizacao = data()
                dispositivos.hora_atualizacao = hora()
                dispositivos.usuario_atualizacao_id = login_usuario_id
            if "dispositivo_descricao" in body:
                dispositivos.dispositivo_descricao = body["dispositivo_descricao"]
                dispositivos.data_atualizacao = data()
                dispositivos.hora_atualizacao = hora()
                dispositivos.usuario_atualizacao_id = login_usuario_id
            if "latitude" in body:
                dispositivos.latitude = body["latitude"]
                dispositivos.data_atualizacao = data()
                dispositivos.hora_atualizacao = hora()
                dispositivos.usuario_atualizacao_id = login_usuario_id
            if "longitude" in body:
                dispositivos.longitude = body["longitude"]
                dispositivos.data_atualizacao = data()
                dispositivos.hora_atualizacao = hora()
                dispositivos.usuario_atualizacao_id = login_usuario_id
            db.session.add(dispositivos)
            db.session.commit()
            return gera_response(200, "Dispositivos", dispositivos.to_json(), "Dispositivo atualizado com sucesso!")
    except Exception as e:
        return gera_response(400, "Dispositivos", {}, f"Falha ao atualizar dispositivo! Mensagem:{e}")

# Endpoint DELETE responsável por deletar um dispositivo
# Deve ser informado o ID do dispositivo 
def dispositivos_deleta(id, current_user):
    try:
        # Criação de variáveis para a validação se o usuário cupre os requisitos
        login_entidade_id = current_user.entidade_id
        login_admin = current_user.admin
        login_deletar = current_user.deletar

        # IF para validar se o ID informado está cadastrado no banco de dados
        if not Dispositivos.query.filter_by(dispositivo_id=id).first():
            return gera_response(400, "Dispositivos", {}, f"Falha ao deletar dispositivo! Mensagem: O dispositivo ID:{id} não existe!")

        dispositivo = Dispositivos.query.filter_by(dispositivo_id=id).first()
        dispositivo_json = dispositivo.to_json()
        
        # IF para validar se a entidade do usuário logado é igual ao do usuário informado
        if dispositivo_json["entidade_id"] != login_entidade_id:
            return gera_response(403, "Dispositivos", {}, "Você não tem permissão para deletar o dispositivo!")

        # IF para validar se o usuário tem a permissão necessária para deletar o usuário
        if login_admin == True or login_deletar == True:
            db.session.delete(dispositivo)
            db.session.commit()
            return gera_response(200, "Dispositivos", dispositivo.to_json(), "Dispositivo deletado com sucesso!")
    except Exception as e:
        return gera_response(400, "Dispositivos", {}, f"Erro ao deletar dispositivo! Mensagem:{e}")

##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo
    if(mensagem):
        body["mensagem"] = mensagem
    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")
