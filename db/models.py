import datetime

from pydantic import BaseModel
from typing import Optional, Any

# Modal Usuário
class Usuario(BaseModel):
    email: str
    senha: str
    is_adm: bool
    nome: str
    status: int

class UsuarioResposta(Usuario):
    id: int
    data_criacao:  Optional[datetime.datetime]
    data_atualizacao: Optional[datetime.datetime]

# Modal Rota
class Rota(BaseModel):
    bounds: list = []
    nome: str

class RotaResposta(Rota):
    id: int
    data_criacao: Optional[datetime.datetime]
    data_atualizacao: Optional[datetime.datetime]
    data_deletacao: Optional[datetime.datetime]

class RotaAssociarVendedor(Rota):
    vendedor_id: Optional[int]

# Modal Vendedor
class Vendedor(BaseModel):
    nome: str
    email: str

class VendedorResposta(Vendedor):
    id: int
    data_criacao: Optional[datetime.datetime]
    data_atualizacao: Optional[datetime.datetime]
    data_deletacao: Optional[datetime.datetime]

#Modal Cliente
class Cliente(BaseModel):
    nome: str
    geolocalização: list = []

class ClienteResposta(Cliente):
    id: int
    data_criacao: Optional[datetime.datetime]
    data_atualizacao: Optional[datetime.datetime]
    data_deletacao: Optional[datetime.datetime]

class ClienteFiltro(BaseModel):
    rota_id: list = []
    rota_nome: list = [""]
    vendedor_id: list = []
    vendedor_nome: list = [""]
    vendedor_email: list = [""]

# Modal Histórico

class Log(BaseModel):
    id: int
    acao: str
    entidade: str
    usuario_id: int
    usuario_nome: str
    registro: str
    data_criacao: Optional[datetime.datetime]

# Modal Token
class UsuarioSenha(UsuarioResposta):
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expired_in: str
    user_info: UsuarioResposta

class TokenData(BaseModel):
    username: str = None