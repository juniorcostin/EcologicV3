from main import db
from flask import Response
from datetime import datetime
import json

now = datetime.now()

#CLASS para a criação da tabela no banco e transformação dos dados em JSON
class Dispositivos(db.Model):
    dispositivo_id = db.Column(db.Integer, primary_key = True)
    dispositivo_nome = db.Column(db.String(40))
    dispositivo_tipo = db.Column(db.String(40))
    dispositivo_ativo = db.Column(db.Boolean)
    dispositivo_descricao = db.Column(db.String(200))
    data_criacao = db.Column(db.Date)
    hora_criacao = db.Column(db.Time)
    data_atualizacao = db.Column(db.Date)
    hora_atualizacao = db.Column(db.Time)
    usuario_criador_id = db.Column(db.Integer)
    entidade_id = db.Column(db.Integer)
    usuario_atualizacao_id = db.Column(db.Integer)

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
                "usuario_atualizacao_id": self.usuario_atualizacao_id
                }

#Endpoint GET /dispositivos para listar todos os Dispositivos
def dispositivos_seleciona_todos():
    dispositivos = Dispositivos.query.all()
    dispositivos_json = [dispositivo.to_json() for dispositivo in dispositivos]
    return gera_response(200, "Dispositivos", dispositivos_json, "Dispositivos Listados Corretamente")

#Endpoint GET /dispositivos/<id> para lista apenas um Dispositivo
def dispositivos_seleciona_um(id):
    dispositivos = Dispositivos.query.filter_by(dispositivo_id=id).first()
    dispositivos_json = dispositivos.to_json()
    return gera_response(200, "Dispositivo", dispositivos_json, "Dispositivo Listado Corretamente")

#Endpoint POST /dispositivos para incluir um novo dispositivo
def dispositivos_criar(body):
    try:
        dispositivo = Dispositivos(
            dispositivo_nome=body["dispositivo_nome"],
            dispositivo_tipo=body["dispositivo_tipo"],
            dispositivo_ativo=body["dispositivo_ativo"],
            dispositivo_descricao=body["dispositivo_descricao"],
            data_criacao=now.strftime('%Y-%m-%d'),
            hora_criacao=now.strftime('%H:%M:%S'),
            data_atualizacao=now.strftime('%Y-%m-%d'),
            hora_atualizacao=now.strftime('%H:%M:%S'),
            usuario_criador_id=body["usuario_criador_id"],
            entidade_id=body["entidade_id"],
            usuario_atualizacao_id=body["usuario_atualizacao_id"]
        )
        db.session.add(dispositivo)
        db.session.commit()
        return gera_response(201, "Dispositivo", dispositivo.to_json(), "Dispositivo criado com sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "Dispositivo", {}, f"Erro ao Cadastrar Dispositivo:{e}")

#Endpoint PUT /dispositivos/<id> para atualizar um Dispositivo
def dispositivos_atualiza(id, body):
    dispositivos = Dispositivos.query.filter_by(dispositivo_id=id).first()
    data_atualizacao = now.strftime('%Y-%m-%d')
    hora_atualizacao = now.strftime('%H:%M:%S')
    try:
        if "dispositivo_nome" in body:
            dispositivos.dispositivo_nome = body["dispositivo_nome"]
            ###### Ajustar data/hora e id usuario atualizacao
            dispositivos.data_atualizacao = data_atualizacao
            dispositivos.hora_atualizacao = hora_atualizacao
            dispositivos.usuario_atualizacao_id = body["usuario_atualizacao_id"]
        if "dispositivo_tipo" in body:
            dispositivos.dispositivo_tipo = body["dispositivo_tipo"]
            ###### Ajustar data/hora e id usuario atualizacao
            dispositivos.data_atualizacao = data_atualizacao
            dispositivos.hora_atualizacao = hora_atualizacao
            dispositivos.usuario_atualizacao_id = body["usuario_atualizacao_id"]
        if "dispositivo_ativo" in body:
            dispositivos.dispositivo_ativo = body["dispositivo_ativo"]
            ###### Ajustar data/hora e id usuario atualizacao
            dispositivos.data_atualizacao = data_atualizacao
            dispositivos.hora_atualizacao = hora_atualizacao
            dispositivos.usuario_atualizacao_id = body["usuario_atualizacao_id"]
        if "dispositivo_descricao" in body:
            dispositivos.dispositivo_descricao = body["dispositivo_descricao"]
            ###### Ajustar data/hora e id usuario atualizacao
            dispositivos.data_atualizacao = data_atualizacao
            dispositivos.hora_atualizacao = hora_atualizacao
            dispositivos.usuario_atualizacao_id = body["usuario_atualizacao_id"]

        db.session.add(dispositivos)
        db.session.commit()
        return gera_response(200, "Dispositivo", dispositivos.to_json(), "Dispositivo atualizado com sucesso")
    except Exception as e:
        return gera_response(400, "Dispositivo", {}, f"Erro ao Atualizar Dispositivo:{e}")

#Endpoint DELETE /dispositivos/<id> para deletar um dispositivo
def dispositivos_deleta(id):
    dispositivos = Dispositivos.query.filter_by(dispositivo_id=id).first()
    try:
        db.session.delete(dispositivos)
        db.session.commit()
        return gera_response(200, "Dispositivo", dispositivos.to_json(), "Dispositivo deletado com sucesso")
    except Exception as e:
        return gera_response(400, "Dispositivo", {}, f"Erro ao deletar Dispositivo:{e}")




##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")