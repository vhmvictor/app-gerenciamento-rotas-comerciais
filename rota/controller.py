from fastapi import APIRouter, Depends, HTTPException
from db import connection_db, models
from utils import util
from datetime import datetime

router = APIRouter()

# Endpoint Rotas - Apenas adms podem acessar
@router.get("/rotas", tags=["Rotas"])
def listar_rotas(current_user: models.UsuarioResposta = Depends(util.get_current_user)):
    print(current_user)
    items = []

    cur = connection_db.cur
    query = "SELECT * from rota where data_deletacao is null order by rota.nome"
    cur.execute(query)
    result = cur.fetchall()
    
    for row in result:
       items.append({'id': row[0], 'bounds': row[1], 'nome': row[2], 'vendedor_id': row[3], 'data_criacao': row[4], 'data_atualizacao': row[5], 'data_deletacao': row[6]})
        
    return items

@router.post("/rotas", response_model=models.Rota, tags=["Rotas"])
def criar_rota(rota: models.Rota, current_user: models.UsuarioResposta = Depends(util.get_current_user)):
    util.findRouteIntersection(rota.bounds, [])
    
    cur = connection_db.cur
    conn = connection_db.conn

    gDate = datetime.now()

    cur.execute("INSERT INTO rota (bounds, nome, data_criacao) VALUES(%s, %s, %s)", (
        rota.bounds, rota.nome, gDate))
    conn.commit()

    util.create_log("Criação", "rota", current_user.id , current_user.email, rota.nome)

    return {
        **rota.dict()
    }

@router.put("/rotas/{id}", tags=["Rotas"])
def editar_rota(id: int, rota: models.Rota, current_user: models.UsuarioResposta = Depends(util.get_current_user)):
    routeDB = util.findExistedRoute(id)
    if not routeDB:
        raise HTTPException(status_code=404, detail="Operation failed. Route not found!")

    util.findRouteIntersection(rota.bounds, routeDB[0].get('bounds'))

    cur = connection_db.cur
    conn = connection_db.conn

    gDate = datetime.now()

    query = "UPDATE rota SET bounds=%s, nome=%s, data_atualizacao=%s WHERE id=%s"

    cur.execute(query,[rota.bounds, rota.nome, gDate, id])
    conn.commit()

    util.create_log("Edição", "rota", current_user.id , current_user.email, rota.nome)

    return {
        **rota.dict()
    }

@router.delete("/rotas/{id}", tags=["Rotas"]) 
def deletar_rota(id: int, current_user: models.UsuarioResposta = Depends(util.get_current_user)):
    routeDB = util.findExistedRoute(id)
    if not routeDB:
        raise HTTPException(status_code=404, detail="Operation failed. Route not found!")
    
    seller_route = routeDB[0].get('vendedor_id')

    if seller_route:
        raise HTTPException(status_code=400, detail="Operation failed. Exist a seller associated with this route!")

    cur = connection_db.cur
    conn = connection_db.conn

    gDate = datetime.now()

    query = "UPDATE rota SET data_deletacao=%s WHERE id=%s and vendedor_id is null"
    cur.execute(query,[gDate, id])
    result = conn.commit()

    util.create_log("Edição", "rota", current_user.id , current_user.email, routeDB[0].get('nome'))

    return {
        "Successful operation. Delete route!"
    }

@router.put("/rotas/{rota_id}/associar_vendedor/{vendedor_id}", tags=["Rotas"])
def associar_vendedor_rota(rota_id: int, vendedor_id: int, current_user: models.UsuarioResposta = Depends(util.get_current_user)):
    routeDB = util.findExistedRoute(rota_id)
    
    if not routeDB:
        raise HTTPException(status_code=404, detail="Operation failed. Route not found!")

    sellerDB = util.findExistedSellerById(vendedor_id)

    if not sellerDB:
        raise HTTPException(status_code=404, detail="Operation failed. Seller not found!")

    cur = connection_db.cur
    conn = connection_db.conn

    gDate = datetime.now()

    try:
        query = "UPDATE rota SET vendedor_id=%s, data_atualizacao=%s WHERE id=%s and data_deletacao is null"   
        cur.execute(query,[vendedor_id, gDate, rota_id])
        conn.commit()

    except:
        raise HTTPException(status_code=404, detail=("Operation failed. Key (vendedor_id)=(" + str(vendedor_id) + ") is not present in table vendedor"))

    query = "UPDATE cliente SET vendedor_id=%s, data_atualizacao=%s WHERE rota_id=%s and data_deletacao is null"   
    cur.execute(query,[vendedor_id, gDate, rota_id])
    conn.commit()

    util.create_log("Associação Vendedor", "rota", current_user.id , current_user.email, routeDB[0].get('nome'))

    return {
        "Successful operation. Seller associated with route!"
    }

@router.put("/rotas/{rota_id}/desassociar_vendedor/{vendedor_id}", tags=["Rotas"])
def desassociar_vendedor_rota(rota_id: int, vendedor_id: int, current_user: models.UsuarioResposta = Depends(util.get_current_user)):
    routeDB = util.findExistedRoute(rota_id)
    
    if not routeDB:
        raise HTTPException(status_code=404, detail="Operation failed. Route not found!")

    sellerDB = util.findExistedSellerById(vendedor_id)

    if not sellerDB:
        raise HTTPException(status_code=404, detail="Operation failed. Seller not found!")

    cur = connection_db.cur
    conn = connection_db.conn

    query = "SELECT * from rota where id=%s and vendedor_id=%s and data_deletacao is null"
    cur.execute(query,[rota_id, vendedor_id])
    result = cur.fetchall()

    if not result:
        raise HTTPException(status_code=404, detail="Operation failed. Not exist association between the route and the seller!")

    gDate = datetime.now()

    try:
        query = "UPDATE rota SET vendedor_id=%s, data_atualizacao=%s WHERE id=%s and data_deletacao is null"   
        cur.execute(query,[None, gDate, rota_id])
        conn.commit()

    except:
        raise HTTPException(status_code=404, detail=("Operation failed! Not desassociated seller"))

    util.create_log("Desassociação Vendedor", "rota", current_user.id , current_user.email, routeDB[0].get('nome'))

    return {
        "Successful operation. Seller desassociated with route!"
    }
