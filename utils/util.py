import os
import dotenv
import jwt

from db import models, connection_db
from passlib.context import CryptContext
from datetime import datetime, timedelta
from shapely.geometry import Point, Polygon, LineString

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from pydantic import ValidationError
from pydantic import types

dotenv.load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)

pwd_bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

# USER FUNCTIONS
def findExistedUser(email: str):
    items = []

    cur = connection_db.cur
    query = "select id, email, senha, nome, is_adm, status from usuario where status='1' and email=%s"
    cur.execute(query,[email])
    result = cur.fetchall()

    for row in result:
        items.append({'id': row[0], 'email': row[1], 'senha': row[2], 'nome': row[3], 'is_adm': row[4], 'status': row[5]})

    return items

# SELLER FUNCTIONS
def findExistedSeller(email: str):
    items = []

    cur = connection_db.cur
    query = "select nome, email from vendedor where email=%s and data_deletacao is null"
    cur.execute(query,[email])
    result = cur.fetchall()

    for row in result:
        items.append({'nome': row[0], 'email': row[1]})

    return items

def findExistedSellerById(id: int):
    items = []

    cur = connection_db.cur
    query = "select id, nome, email from vendedor where id=%s and data_deletacao is null"
    cur.execute(query,[id])
    result = cur.fetchall()

    for row in result:
        items.append({'id':row[0], 'nome': row[1], 'email': row[2]})

    return items

# ROUTE FUNCTIONS
def findExistedRoute(id: int):
    items = []

    cur = connection_db.cur
    query = "select id, bounds, nome, vendedor_id from rota where id=%s and data_deletacao is null"
    cur.execute(query,[id])
    result = cur.fetchall()

    for row in result:
        items.append({'id': row[0], 'bounds': row[1], 'nome': row[2], 'vendedor_id': row[3]})

    return items

def findRouteIntersection(bounds: list, bounds_id: list):
    is_intersect = False

    if not bounds:
        raise HTTPException(status_code=400, detail="Operation failed. Bounds array is empty!")
    
    # Edit Route
    if bounds_id:
        result = getAllBounds()
        result.remove(bounds_id)
        for item in result:
                try:
                    if LineString(item).intersects(LineString(bounds)) == True:
                        is_intersect = True
                except:
                    raise HTTPException(status_code=400, detail="Operation failed. Invalid coordinate!")
    else:
        # Create Route
        cur = connection_db.cur
        query = "select bounds from rota"
        cur.execute(query)
        result = cur.fetchall()
        for row in result:
            for item in row:
                try:
                    if LineString(item).intersects(LineString(bounds)) == True:
                        is_intersect = True
                except:
                    raise HTTPException(status_code=400, detail="Operation failed. Invalid coordinate!")
    
    if is_intersect == True:
        raise HTTPException(status_code=400, detail="Operation failed. There was an intersection between the inserted route and one already registered!")

    return is_intersect

def getAllRoutes():
    coord_result =[]

    cur = connection_db.cur
    query = "select id, bounds, nome, vendedor_id from rota where data_deletacao is null"
    cur.execute(query)
    result = cur.fetchall()

    for row in result:
        coord_result.append({'id': row[0], 'bounds': row[1], 'nome': row[2], 'vendedor_id': row[3]})

    return coord_result

def getAllBounds():
    bounds_result =[]

    cur = connection_db.cur
    query = "select bounds from rota where data_deletacao is null"
    cur.execute(query)
    result = cur.fetchall()

    for row in result:
        bounds_result.append(row[0])

    return bounds_result

# CLIENT FUNCTIONS
def findExistedClient(geo: types.List[float], client_id: int):
    items = []

    cur = connection_db.cur

    # Edit
    if client_id:
        query = "select id, nome, geolocalizacao, rota_id from cliente where id=%s and data_deletacao is null"
        cur.execute(query,[client_id])
        items = cur.fetchall()
        
        if not items:
             raise HTTPException(status_code=400, detail="Operation failed. Client not found!!")
    else:
        query = "select id, nome, geolocalizacao, rota_id from cliente where geolocalizacao='{%s, %s}' and data_deletacao is null"
        cur.execute(query,[geo[0], geo[1]])
        result = cur.fetchall()

        for row in result:
            items.append({'id': row[0], 'nome': row[1], 'geolocalizacao': row[2], 'rota_id': row[3]})

    return items

def findClientContainsRoute(geo: types.List[float]):
    is_contains = False
    rota_id = 0
    vendedor_id = None

    if not geo:
        raise HTTPException(status_code=400, detail="Operation failed. Geolocalization array is empty!")
    
    else:
        routes = getAllRoutes()

        for row in routes:
            try:
                if Polygon(row.get('bounds')).contains(Point(geo)) == True:
                    is_contains = True
                    rota_id = row.get('id')
                    vendedor_id = row.get('vendedor_id')
            except:
                raise HTTPException(status_code=400, detail="Operation failed. Invalid coordinate!")
    
    return {
        "is_contains": is_contains,
         "rota_id": rota_id,
         "vendedor_id": vendedor_id
    }

# UTILS FUNCTIONS 
def hashed_password(password):
    return pwd_bcrypt.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_bcrypt.verify(plain_password, hashed_password)

def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, os.getenv("SECRET_KET"), algorithm=os.getenv("ALGORITHM"))
    return encode_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, os.getenv("SECRET_KET"), algorithms=[os.getenv("ALGORITHM")])
        username: str = payload.get("sub")
        is_adm: bool = payload.get("is_adm")
        if is_adm is False: 
            raise credentials_exception
        token_data = models.TokenData(username=username)
    except (PyJWTError, ValidationError):
        raise credentials_exception
    
    user = findExistedUser(token_data.username)
    if user is None:
        raise credentials_exception

    return models.UsuarioResposta(**user[0])