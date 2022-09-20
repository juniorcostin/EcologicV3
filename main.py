from flask import Flask, request, jsonify
from database import session, engine
from models import dispositivo
session = session()
app = Flask("Ecologic")

@app.route("/dispositivos/cadastrar", methods=["POST"])
def cadatrar_dispositivos():
    body = request.get_json()
    with engine.connect() as con:
        novo_dispositivo = dispositivo(body)
        session.add(novo_dispositivo)
        session.commit()
    return jsonify("Teste")

def geraResponse(status, mensagem, nome_conteudo=False, conteudo=False):
    response = {}
    response["Status"] = status
    response["Mensagem"] = mensagem

    if(nome_conteudo and conteudo):
        response[nome_conteudo] = conteudo

    return response

app.run()