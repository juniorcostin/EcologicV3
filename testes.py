import json
from requests.exceptions import HTTPError
import requests
from datetime import datetime

body = {
        "dispositivo_nome": "Teste API",
        "dispositivo_tipo": "rele API",
        "dispositivo_ativo": True,
        "dispositivo_descricao": "Teste Inserção API",
        "data_criacao": "2022-02-02",
        "data_atualizacao": "2022-02-02",
        "usuario_criador_id": 1,
        "entidade_id": 1,
        "teste": "teste"
}
body_json = json.dumps(body, default=str)

teste = requests.post("http://localhost:5000/dispositivos", data=body_json)
print(teste.status_code)
print(teste)