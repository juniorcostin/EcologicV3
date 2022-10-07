from modules.usuarios import Usuarios
from modules.entidades import Entidades
from config.config import db
from datetime import datetime

def data():
    data = datetime.now()
    return data.strftime('%Y-%m-%d')
def hora():
    hora = datetime.now()
    return hora.strftime('%H:%M:%S')

def primeira_entidade():
    try:
        entidade = Entidades(
                entidade_razaosocial="CostinTech Network",
                entidade_ramo="Tecnologia",
                dispositivos_quantidade="1000",
                cpfcnpj="45.787.008/0001-88",
                data_criacao=data(),
                hora_criacao=hora(),
                data_atualizacao=data(),
                hora_atualizacao=hora(),
                usuario_criador_id=0,
                entidade_ativa=True,
                usuario_atualizacao_id=0,
                entidade_nome="Ecologic",
                longitude="",
                latitude="",
                cep="81580-080",
                cidade="Curitiba",
                estado="Paraná"
            )
        db.session.add(entidade)
        db.session.commit()
        return print("Entidade criada com sucesso!")
    except Exception as e:
        return print(f"Falha ao cadastrar entidade! Mensagem:{e}")

def entidade_id():
    try:
        entidade = Entidades.query.filter_by(cpfcnpj="45.787.008/0001-88").first()
        entidade_json = entidade.to_json()
        print(f"Busca do ID realizada com sucesso!")
        return entidade_json["entidade_id"]
    except Exception as e:
        print(f"Falha ao buscar a entidade_id! Mensagem {e}")

def primeiro_usuario():
    try:
        usuario = Usuarios(
                        usuario_primeiro_nome="admin",
                        usuario_segundo_nome="admin",
                        usuario_email="admin@admin.com",
                        usuario_senha="boladegordura",
                        data_criacao=data(),
                        hora_criacao=hora(),
                        data_atualizacao=data(),
                        hora_atualizacao=hora(),
                        usuario_ativo=True,
                        entidade_id=entidade_id(),
                        usuario_criador_id=0,
                        usuario_atualizacao_id=0,
                        admin=True,
                        cadastrar=True,
                        editar=True,
                        deletar=True,
                        visualizar=True
                    )
        db.session.add(usuario)
        db.session.commit()
        print("Usuario criado com sucesso!")
    except Exception as e:
        print(f'Falha ao criar usuário! Mensagem: {e}')

primeira_entidade()
primeiro_usuario()