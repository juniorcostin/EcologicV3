from config.config import db, admin
from flask import Response
from datetime import datetime
from admin.admin import tabela_entidades
import json

now = datetime.now()

#CLASS para a criação da tabela no banco e transformação dos dados em JSON
class Entidades(db.Model):
    entidade_id = db.Column(db.Integer, primary_key = True)
    entidade_razaosocial = db.Column(db.String(40))
    entidade_ramo = db.Column(db.String(40))
    dispositivos_quantidade = db.Column(db.Integer)
    cpfcnpj = db.Column(db.String(40))
    data_criacao = db.Column(db.Date)
    data_atualizacao = db.Column(db.Date)
    usuario_criador_id = db.Column(db.Integer)
    entidade_ativa = db.Column(db.Boolean)
    usuario_atualizacao_id = db.Column(db.Integer)
    hora_atualizacao = db.Column(db.Time)
    hora_criacao = db.Column(db.Time)
    entidade_nome = db.Column(db.String(40))


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
                "entidade_nome": self.entidade_nome
                }

# Paramentro para criar a tabela dentro da interface Admin do sistema
admin.add_view(tabela_entidades(Entidades, db.session))

#Endpoint GET /entidades para listar todos as Entidades
def entidades_seleciona_todos():
    entidades = Entidades.query.all()
    entidades_json = [entidade.to_json() for entidade in entidades]
    return gera_response(200, "Entidades", entidades_json, "Entidades listadas com sucesso")

#Endpoint GET /entidades/<id> para lista apenas uma Entidade
def entidades_seleciona_um(id):
    entidades = Entidades.query.filter_by(entidade_id=id).first()
    entidades_json = entidades.to_json()
    return gera_response(200, "Entidades", entidades_json, "Entidades listadas com sucesso")

#Endpoint POST /entidades para incluir uma nova Entidade
def entidades_criar(body):
    try:
        entidade = Entidades(
            entidade_razaosocial=body["entidade_razaosocial"],
            entidade_ramo=body["entidade_ramo"],
            dispositivos_quantidade=body["dispositivos_quantidade"],
            cpfcnpj=body["cpfcnpj"],
            data_criacao=now.strftime('%Y-%m-%d'),
            hora_criacao=now.strftime('%H:%M:%S'),
            data_atualizacao=now.strftime('%Y-%m-%d'),
            hora_atualizacao=now.strftime('%H:%M:%S'),
            usuario_criador_id=body["usuario_criador_id"],
            entidade_ativa=body["entidade_ativa"],
            usuario_atualizacao_id=body["usuario_atualizacao_id"],
            entidade_nome=body["entidade_nome"]
        )
        db.session.add(entidade)
        db.session.commit()
        return gera_response(201, "Entidade", entidade.to_json(), "Entidade criada com sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "Entidade", {}, f"Erro ao Cadastrar Entidade:{e}")

#Endpoint PUT /entidades/<id> para atualizar uma Entidade
def entidade_atualiza(id, body):
    entidades = Entidades.query.filter_by(entidade_id=id).first()
    data_atualizacao = now.strftime('%Y-%m-%d')
    hora_atualizacao = now.strftime('%H:%M:%S')
    try:
        if "entidade_razaosocial" in body:
            entidades.entidade_razaosocial = body["entidade_razaosocial"]
            ###### Ajustar data/hora e id usuario atualizacao
            entidades.data_atualizacao = data_atualizacao
            entidades.hora_atualizacao = hora_atualizacao
            entidades.usuario_atualizacao_id = body["usuario_atualizacao_id"]
        if "entidade_ramo" in body:
            entidades.entidade_ramo = body["entidade_ramo"]
            ###### Ajustar data/hora e id usuario atualizacao
            entidades.data_atualizacao = data_atualizacao
            entidades.hora_atualizacao = hora_atualizacao
            entidades.usuario_atualizacao_id = body["usuario_atualizacao_id"]
        if "dispositivos_quantidade" in body:
            entidades.dispositivos_quantidade = body["dispositivos_quantidade"]
            ###### Ajustar data/hora e id usuario atualizacao
            entidades.data_atualizacao = data_atualizacao
            entidades.hora_atualizacao = hora_atualizacao
            entidades.usuario_atualizacao_id = body["usuario_atualizacao_id"]
        if "entidade_ativa" in body:
            entidades.entidade_ativa = body["entidade_ativa"]
            ###### Ajustar data/hora e id usuario atualizacao
            entidades.data_atualizacao = data_atualizacao
            entidades.hora_atualizacao = hora_atualizacao
            entidades.usuario_atualizacao_id = body["usuario_atualizacao_id"]
        if "entidade_nome" in body:
            entidades.entidade_nome = body["entidade_nome"]
            ###### Ajustar data/hora e id usuario atualizacao
            entidades.data_atualizacao = data_atualizacao
            entidades.hora_atualizacao = hora_atualizacao
            entidades.usuario_atualizacao_id = body["usuario_atualizacao_id"]

        db.session.add(entidades)
        db.session.commit()
        return gera_response(200, "Entidades", entidades.to_json(), "Entidade atualizada com sucesso")
    except Exception as e:
        return gera_response(400, "Entidades", {}, f"Erro ao Atualizar Entidade:{e}")

#Endpoint DELETE /entidades/<id> para deletar um dispositivo
def entidade_deleta(id):
    entidades = Entidades.query.filter_by(entidade_id=id).first()
    try:
        db.session.delete(entidades)
        db.session.commit()
        return gera_response(200, "Entidades", entidades.to_json(), "Entidade deletado com sucesso")
    except Exception as e:
        return gera_response(400, "Entidade", {}, f"Erro ao deletar Entidade:{e}")


##################### Função para a geração de mensagens de erro/sucesso ########################
def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")
