def insertdispositivos(nome, tipo, ativo, entidade_id, data_criacao, data_atualizacao, usuario, descricao = False):
    return {
        "nome": nome,
        "tipo": tipo,
        "descrição": descricao,
        "ativo": ativo,
        "ID da entidade": entidade_id,
        "data da criação": data_criacao,
        "data da atualização": data_atualizacao,
        "usuario": usuario
    }