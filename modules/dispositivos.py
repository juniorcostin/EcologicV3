# Imports nencessários para que os Endpoints funcionem corretamente
from main import db
from flask import Response
import json

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

# Endpoint GET que lista todos os dispositivos cadastrados dentro do banco de dados
def dispositivos_seleciona_todos():
    try:
        dispositivos = Dispositivos.query.all()
        dispositivos_json = [dispositivo.to_json() for dispositivo in dispositivos]
        return gera_response(200, "Dispositivos", dispositivos_json, "Dispositivos listados com sucesso!")
    except Exception as e:
        return gera_response(400, "Dispositivos", {}, f"Falha ao listar dispositivos! Mensagem: {e}")

# Endpoint GET que lista apenas um dispositivo, sendo filtrado pelo ID
# O ID deve ser informado na URL e também deve estar cadastrado no banco de dados
def dispositivos_seleciona_um(id):
    if id not in Dispositivos.query.filter_by(dispositivo_id=id).first():
        return gera_response(400, "Dispositivos", {}, f"Falha ao listar dispositivo! Mensagem: Dispositivo {id} não foi encontrado no banco de dados")
    try:
        dispositivos = Dispositivos.query.filter_by(dispositivo_id=id).first()
        dispositivos_json = dispositivos.to_json()
        return gera_response(200, "Dispositivos", dispositivos_json, "Dispositivo listado com sucesso!")
    except Exception as e:
        return gera_response(400, "Dispositivos", {}, f"Falha ao listar dispositivo! Mensagem: {e}")

#Endpoint POST /dispositivos para incluir um novo dispositivo
def dispositivos_criar(body):
    try:
        dispositivo = Dispositivos(
            dispositivo_nome=body["dispositivo_nome"],
            dispositivo_tipo=body["dispositivo_tipo"],
            dispositivo_ativo=body["dispositivo_ativo"],
            dispositivo_descricao=body["dispositivo_descricao"],
            data_criacao=body["data_criacao"],
            hora_criacao=body["hora_criacao"],
            data_atualizacao=["data_atualizacao"],
            hora_atualizacao=["hora_atualizacao"],
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
    try:
        if "dispositivo_nome" in body:
            dispositivos.dispositivo_nome = body["dispositivo_nome"]

        if "dispositivo_tipo" in body:
            dispositivos.dispositivo_tipo = body["dispositivo_tipo"]

        if "dispositivo_ativo" in body:
            dispositivos.dispositivo_ativo = body["dispositivo_ativo"]

        if "dispositivo_descricao" in body:
            dispositivos.dispositivo_descricao = body["dispositivo_descricao"]

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