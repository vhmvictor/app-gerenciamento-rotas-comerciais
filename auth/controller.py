import os
import dotenv

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from db import models, connection_db
from utils import util
from datetime import datetime

from fastapi.security import OAuth2PasswordRequestForm

dotenv.load_dotenv()

router = APIRouter()

# Home

@router.get("/")
def index():
    return {"REST API"}

# Endpoint Login - Todos podem acessar
@router.post("/login", response_model=models.Token, tags=["Login"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    userDB = util.findExistedUser(form_data.username)
    if not userDB:
        raise HTTPException(status_code=404, detail="User not found")

    user = models.UsuarioSenha(**userDB[0])
    authorized = util.verify_password(form_data.password, user.senha)
    if not authorized:
        raise HTTPException(status_code=404, detail="E-mail or password invalid!")

    access_token_expires = util.timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = util.create_access_token(
        data={"sub": form_data.username, "is_adm": user.is_adm},
        expires_delta=access_token_expires,
    )

    util.create_log("Login", "login", int(userDB[0].get('id')), userDB[0].get('email'), "")

    results = {
        "access_token": access_token,
        "token_type": "bearer",
        "expired_in": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))*120,
        "user_info": user
    }

    return results

# Endponit Listar usuários
@router.get("/usuarios", tags=["Usuarios"])
def listar_usuarios():
    items = []

    cur = connection_db.cur
    query = "SELECT * from usuario order by usuario.id"
    cur.execute(query)
    result = cur.fetchall()

    for row in result:
        items.append({'id': row[0], 'email': row[1], 'senha': row[2], 'nome': row[3], 'is_adm': row[4],  'status': row[5], 'data_criacao': row[6], 'data_atualizacao': row[7]})
        
    return items
  
@router.post("/usuarios", tags=["Usuarios"])
def criar_usuario(usuario: models.Usuario, current_user: models.UsuarioResposta = Depends(util.get_current_user)):
    userDB = util.findExistedUser(usuario.email)
    if userDB:
        raise HTTPException(status_code=400, detail="User email already exist!")

    cur = connection_db.cur
    conn = connection_db.conn

    gDate = datetime.now()
    
    cur.execute("INSERT INTO usuario (email, senha, nome, is_adm, status, data_criacao) VALUES(%s, %s, %s, %s, %s, %s)", (
        usuario.email, util.hashed_password(usuario.senha), usuario.nome, usuario.is_adm, usuario.status, gDate))
    conn.commit()

    util.create_log("Criação", "usuario", current_user.id , current_user.email, usuario.email)

    return {
        **usuario.dict(),
    }