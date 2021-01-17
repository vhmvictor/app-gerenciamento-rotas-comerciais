from fastapi import APIRouter, HTTPException, Depends
from db import models, connection_db
from utils import util
from datetime import datetime

router = APIRouter()

# Endpoint Vendedores - Apenas adms podem acessar
@router.get("/vendedores/listar/", tags=["Vendedores"])
def listar_vendedores(current_user: models.UsuarioResposta = Depends(util.get_current_user)):
    ressult = []
    items = []

    cur = connection_db.cur
    query = "SELECT * from vendedor where data_deletacao is null order by vendedor.nome"
    cur.execute(query)
    result = cur.fetchall()
    
    for row in result:
        items.append({'id': row[0], 'nome': row[1], 'email': row[2],'data_criacao': row[3], 'data_atualizacao': row[4], 'data_deletacao': row[5]})
        
    return items

@router.post("/vendedores/criar/", response_model=models.Vendedor, tags=["Vendedores"])
def criar_vendedor(vendedor: models.Vendedor, current_user: models.UsuarioResposta = Depends(util.get_current_user)):
    sellDB = util.findExistedSeller(vendedor.email)
    if sellDB:
        raise HTTPException(status_code=400, detail="Seller already exist!")

    cur = connection_db.cur
    conn = connection_db.conn

    gDate = datetime.now()

    cur.execute("INSERT INTO vendedor (nome, email, data_criacao) VALUES(%s, %s, %s)", (
        vendedor.nome, vendedor.email, gDate))
    conn.commit()

    return {
        **vendedor.dict()
    }

@router.delete("/vendedores/deletar/{id}", tags=["Vendedores"])
def deletar_vendedor(id: int, current_user: models.UsuarioResposta = Depends(util.get_current_user)):
    cur = connection_db.cur
    query = "select * from vendedor where id=%s"
    cur.execute(query,[id])
    result = cur.fetchall()
    
    if not result:
        raise HTTPException(status_code=404, detail="Operation failed. Seller not found!")

    cur = connection_db.cur
    conn = connection_db.conn

    gDate = datetime.now()

    query = "UPDATE vendedor SET data_deletacao=%s WHERE id=%s"

    cur.execute(query,[gDate, id])

    conn.commit()

    return {
        "Successful operation. Delete seller!"
    }