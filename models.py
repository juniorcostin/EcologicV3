from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.types import Boolean
from database import base, engine

class dispositivo(base):
    __tablename__ = "dispositivos"
    dispositivo_id = Column(Integer, autoincrement = True, primary_key = True)
    dispositivo_nome = Column(String(40))
    dispositivo_tipo = Column(String(40))
    dispositivo_ativo = Column(Boolean)
    dispositivo_descricao = Column(String(200))
    data_criacao = Column(Date)
    data_atualizacao = Column(Date)
    usuario_criador_id = Column(Integer)
    entidade_id = Column(Integer)

base.metadata.create_all(engine)