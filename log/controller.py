from fastapi import APIRouter, HTTPException, Depends
from db import models, connection_db
from utils import util
from datetime import datetime

router = APIRouter()

# Endpoint Vendedores - Apenas adms podem acessar
@router.get("/log", tags=["Logs"])
def listar_log(current_user: models.UsuarioResposta = Depends(util.get_current_user)):
    items = []

    cur = connection_db.cur
    query = "SELECT * from log order by log.data_criacao"
    cur.execute(query)
    result = cur.fetchall()
    
    for row in result:
        items.append({'id': row[0], 'acao': row[1], 'entidade': row[2],'usuario_id': row[3], 'usuario_nome': row[4], 'registro': row[5], 'data_criacao': row[6]})
        
    return items