import numpy as np

from fastapi import APIRouter, HTTPException, Depends, Query
from db import models, connection_db
from utils import util
from datetime import datetime
from typing import List

router = APIRouter()

# Endpoint Clientes - Todos podem acessar, exceto listar todos clientes (só adms)
@router.post("/clientes/filtrar", tags=["Clientes"]) #só adms acessam
def listar_clientes(filtro: models.ClienteFiltro = None, current_user: models.UsuarioResposta = Depends(util.get_current_user)):
    array_concated = []
    array_result = []

    cur = connection_db.cur

    if len(filtro.rota_id) == 0 and filtro.rota_nome == [""] and len(filtro.vendedor_id) == 0 and filtro.vendedor_nome == [""] and filtro.vendedor_email == [""]:
        print("vazio")
        query = "SELECT * FROM v_cliente where data_deletacao is null"
        cur.execute(query)
        result = cur.fetchall()

        array_result = result

    if len(filtro.rota_id) != 0:
        for row in filtro.rota_id:
            query = "SELECT * FROM v_cliente where rota_id=%s and data_deletacao is null"
            cur.execute(query,[row])
            result = cur.fetchall()

            for item in result:
                if item in array_result:
                    array_result.remove(item)

            array_result += result
    
    if filtro.rota_nome != [""]:
        for row in filtro.rota_nome:
            query = "SELECT * FROM v_cliente where rota_nome~*%s and data_deletacao is null"
            cur.execute(query,[row])
            result = cur.fetchall()

            for item in result:
                if item in array_result:
                    array_result.remove(item)

            array_result += result

    if len(filtro.vendedor_id) != 0:
        for row in filtro.vendedor_id:
            query = "SELECT * FROM v_cliente where vendedor_id=%s and data_deletacao is null"
            cur.execute(query,[row])
            result = cur.fetchall()

            for item in result:
                if item in array_result:
                    array_result.remove(item)

            array_result += result

    if filtro.vendedor_nome != [""]:
        for row in filtro.vendedor_nome:
            query = "SELECT * FROM v_cliente where vendedor_nome~*%s and data_deletacao is null"
            cur.execute(query,[row])
            result = cur.fetchall()

            for item in result:
                if item in array_result:
                    array_result.remove(item)
            
            array_result += result

    if filtro.vendedor_email != [""]:
        for row in filtro.vendedor_email:
            query = "SELECT * FROM v_cliente where vendedor_email~*%s and data_deletacao is null"
            cur.execute(query,[row])
            result = cur.fetchall()

            for item in result:
                if item in array_result:
                    array_result.remove(item)

            array_result += result
            
    for row in array_result:
                array_concated.append({'id': row[0], 'nome': row[1], 'geolocalizacao': row[2], 'rota_id': row[3], 'rota_nome': row[4], 'vendedor_id': row[5], 'vendedor_nome': row[6], 'vendedor_email': row[7], 'data_criacao': row[8], 'data_atualizacao': row[9], 'data_deletacao': row[10]})

    return array_concated

@router.get("/clientes/{vendedor_id}", tags=["Clientes"]) #listar somentes os clientes de um vendedor específico
def listar_clientes_vendedor_id(vendedor_id: int):
    items = []

    sellerDB = util.findExistedSellerById(vendedor_id)

    if not sellerDB:
        raise HTTPException(status_code=404, detail="Operation failed. Seller not found!")

    cur = connection_db.cur
    query = "SELECT * FROM cliente INNER JOIN vendedor ON (cliente.vendedor_id = vendedor.id) where cliente.vendedor_id=%s and cliente.data_deletacao is null order by cliente.nome"
    cur.execute(query,[vendedor_id])
    result = cur.fetchall()
    
    for row in result:
        items.append({'id': row[0], 'nome': row[1], 'geolocalizacao': row[2], 'rota_id': row[3], 'vendedor_id': row[4], 'data_criacao': row[5], 'data_atualizacao': row[6], 'data_deletacao': row[7]})
        
    return items

@router.post("/clientes", response_model=models.Cliente, tags=["Clientes"]) #esse endpoint deve usar estratégias geométricas para conseguir dizer a qual rota o cliente pertence
def criar_cliente(cliente: models.Cliente):
    clientDb = util.findExistedClient(cliente.geolocalização, None)
    if clientDb:
        raise HTTPException(status_code=400, detail="Client already exist!")

    result = util.findClientContainsRoute(cliente.geolocalização)

    cur = connection_db.cur
    conn = connection_db.conn
    gDate = datetime.now()

    if result.get('is_contains') == True:
        cur.execute("INSERT INTO cliente (nome, geolocalizacao, rota_id, vendedor_id, data_criacao) VALUES(%s, %s, %s, %s, %s)", (
        cliente.nome, cliente.geolocalização, result.get('rota_id'), result.get('vendedor_id'), gDate))
        conn.commit()
    else:
        cur.execute("INSERT INTO cliente (nome, geolocalizacao, rota_id, vendedor_id, data_criacao) VALUES(%s, %s, %s, %s, %s)", (
        cliente.nome, cliente.geolocalização, 1, None, gDate))
        conn.commit()

    return {
        **cliente.dict(),
    }

@router.put("/clientes/{id}", tags=["Clientes"])
def editar_cliente(id: int, cliente: models.Cliente):
    clientDb = util.findExistedClient(cliente.geolocalização, id)

    result = util.findClientContainsRoute(cliente.geolocalização)

    cur = connection_db.cur
    conn = connection_db.conn
    gDate = datetime.now()

    if result.get('is_contains') == True:

        query = "UPDATE cliente SET nome=%s, geolocalizacao=%s, rota_id=%s, vendedor_id=%s, data_atualizacao=%s WHERE id=%s"

        cur.execute(query, [cliente.nome, cliente.geolocalização, result.get('rota_id'), result.get('vendedor_id'), gDate, id])
        conn.commit()
    else:
        query = "UPDATE cliente SET nome=%s, geolocalizacao=%s, rota_id=%s, vendedor_id=%s, data_atualizacao=%s WHERE id=%s"

        cur.execute(query, [cliente.nome, cliente.geolocalização, 1, None, gDate, id])
        conn.commit()

    return {
        **cliente.dict(),
    }

@router.delete("/clientes{id}", tags=["Clientes"])
def deletar_cliente(id: int):
    clientDB = util.findExistedClient([], id)

    if not clientDB:
        raise HTTPException(status_code=404, detail="Operation failed. Client not found!")

    cur = connection_db.cur
    conn = connection_db.conn

    gDate = datetime.now()

    query = "UPDATE cliente SET data_deletacao=%s WHERE id=%s"

    cur.execute(query,[gDate, id])

    conn.commit()

    return {
        "Successful operation. Delete client!"
    }