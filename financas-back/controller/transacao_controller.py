from sqlmodel import select, Session
from database.models import ContaBancaria, Usuario, Transacao, Categoria
from fastapi import HTTPException

async def cria_transacao(valor, tipo, categoria, user, db:Session, conta):
    try:
        int(categoria)
        return categoria_final
    except ValueError:
        query_igualdade = select(Categoria).where(Categoria.categoria == categoria, Categoria.usuario_id == user['id'])
        result_igualdade = db.exec(query_igualdade).first()
        if result_igualdade:
            categoria_final = result_igualdade.id
        else:
            cria_categoria = Categoria(
                usuario_id=user['id'],
                categoria=categoria
            )
            db.add(cria_categoria)
            db.commit()
            query = select(Categoria).where(Categoria.categoria == categoria, Categoria.usuario_id == user['id'])
            result = db.exec(query).first()
            categoria_final = result.id

    cria_transacao = Transacao(
        usuario_id=user['id'], 
        conta_bancaria_id=conta, 
        tipo_id=tipo, 
        valor=valor, 
        categoria_id=categoria_final
        )
    
    db.add(cria_transacao)

    if tipo == 1:
        query = select(Usuario).where(Usuario.id == user['id'])
        usuario = db.exec(query).first()
        usuario.saldo_usuario += valor
        if conta:
            query = select(ContaBancaria).where(ContaBancaria.id == conta)
            conta = db.exec(query).first()
            conta.saldo_conta += valor
    if tipo == 2:
        query = select(Usuario).where(Usuario.id == user['id'])
        usuario = db.exec(query).first()
        usuario.saldo_usuario -= valor
        if conta:
            query = select(ContaBancaria).where(ContaBancaria.id == conta)
            conta = db.exec(query).first()
            conta.saldo_conta -= valor

    db.commit()

    return {"201": "Transação criada com sucesso!"}