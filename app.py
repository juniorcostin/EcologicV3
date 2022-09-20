from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://darkroom9282:v2mzt67cZYDdAq@168.138.150.79:49154/ecologicDEV'

db = SQLAlchemy(app)

class Dispositivos(db.Model):
    dispositivo_id = db.Column(db.Integer, primary_key = True)
    dispositivo_nome = db.Column(db.String(40))
    dispositivo_tipo = db.Column(db.String(40))
    dispositivo_ativo = db.Column(db.Boolean)
    dispositivo_descricao = db.Column(db.String(200))
    data_criacao = db.Column(db.Date)
    data_atualizacao = db.Column(db.Date)
    usuario_criador_id = db.Column(db.Integer)
    entidade_id = db.Column(db.Integer)

    def to_json(self):
        return {"dispositivo_id": self.dispositivo_id, "dispositivo_nome": self.dispositivo_nome, "dispositivo_tipo": self.dispositivo_tipo, "dispositivo_ativo": self.dispositivo_ativo, "dispositivo_descricao": self.dispositivo_descricao, "data_criacao": self.data_criacao, "data_atualizacao": self.data_atualizacao, "usuario_criador_id": self.usuario_criador_id, "entidade_id": self.entidade_id}

@app.route("/dispositivos", methods=["GET"])
def seleciona_dispositivos():
    dispositivos = Dispositivos.query.all()
    dispositivos_json = [dispositivo.to_json() for dispositivo in dispositivos]

    return gera_response(200, "Dispositivos", dispositivos_json, "Dispositivos Listados Corretamente")

@app.route("/dispositivos/<id>", methods=["GET"])
def seleciona_dispositivo(id):
    dispositivos = Dispositivos.query.filter_by(dispositivo_id=id).first()
    dispositivos_json = dispositivos.to_json()

    return gera_response(200, "Dispositivo", dispositivos_json, "Dispositivo Listado Corretamente")

@app.route("/dispositivos", methods=["POST"])
def cria_dispositivo():
    body = request.get_json()
    try:
        dispositivo = Dispositivos(dispositivo_nome=body["dispositivo_nome"], dispositivo_tipo=body["dispositivo_tipo"], dispositivo_ativo=body["dispositivo_ativo"], dispositivo_descricao=body["dispositivo_descricao"], data_criacao=datetime.strptime(body["data_criacao"],'%Y-%m-%d').date(), data_atualizacao=datetime.strptime(body["data_atualizacao"],'%Y-%m-%d').date(), usuario_criador_id=["usuario_criador_id"], entidade_id=body["entidade_id"])
        db.session.add(dispositivo)
        db.session.commit()
        return gera_response(201, "Dispositivo", dispositivo.to_json(), "Dispositivo criado com sucesso")
    except Exception as e:
        print(e)
        return gera_response(400, "Dispositivo", {}, f"Erro ao Cadastrar Dispositivo:{e}")

def gera_response(status, nome_conteudo, conteudo, mensagem = False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body, default=str), status= status, mimetype="application/json")

app.run()