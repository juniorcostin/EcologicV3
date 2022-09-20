from flask import Flask, request
from database import insertdispositivos
app = Flask("Ecologic")

@app.route("/dispositivos/cadastrar", methods=["POST"])
def cadatrar_dispositivos():
    body = request.get_json()
    if "nome" not in body or body["nome"] == "":
        return geraResponse(400, "O parâmetro nome do dispositivo é obrigatório")
    if "tipo" not in body or body["tipo"] == "":
        return geraResponse(400, "O parâmetro tipo do dispositivo é obrigatório")
    if "ativo" not in body or body["ativo"] == "":
        return geraResponse(400, "O parâmetro status ativo do dispositivo é obrigatório")
    if "entidade_id" not in body or body["entidade_id"] == "":
        return geraResponse(400, "O parâmetro id_entidade do dispositivo é obrigatório")
    if "data_criacao" not in body or body["data_criacao"] == "":
        return geraResponse(400, "O parâmetro data_criacao do dispositivo é obrigatório")
    if "data_atualizacao" not in body or body["data_atualizacao"] == "":
        return geraResponse(400, "O parâmetro data_atualizacao do dispositivo é obrigatório")
    if "usuario" not in body or body["usuario"] == "":
        return geraResponse(400, "O parâmetro usuario do dispositivo é obrigatório")

    dispositivo = insertdispositivos(body["nome"], body["tipo"], body["descricao"], body["ativo"], body["entidade_id"], body["data_criacao"], body["data_atualizacao"], body["usuario"])

    return geraResponse(200, "Dispositivo Criado", "Dispositivo", dispositivo)

def geraResponse(status, mensagem, nome_conteudo=False, conteudo=False):
    response = {}
    response["Status"] = status
    response["Mensagem"] = mensagem

    if(nome_conteudo and conteudo):
        response[nome_conteudo] = conteudo

    return response

app.run()