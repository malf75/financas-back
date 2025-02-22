from sqlmodel import select, Session
from database.models import ContaBancaria
from fastapi import HTTPException


def retorna_contas_usuario(user, db: Session):
    query = select(ContaBancaria).where(ContaBancaria.usuario_id == user['id'])
    print(query)
    results = db.exec(query).all()
    if not results:
        raise HTTPException(status_code=404, detail="Usuário não possui contas bancárias")
    return results

def cria_conta_usuario(nome, saldo_conta, user, db: Session):
    cria_conta = ContaBancaria(
        usuario_id=user['id'],
        nome=nome,
        saldo_conta=saldo_conta
    )
    query = select(ContaBancaria).where(ContaBancaria.nome == cria_conta.nome, ContaBancaria.usuario_id == user['id'])
    consulta = db.exec(query).first()
    if consulta:
        raise HTTPException(status_code=400, detail="Conta Bancária Já Registrada")
    else:
        db.add(cria_conta)
        db.commit()
        return {"201": "Conta Criada"}